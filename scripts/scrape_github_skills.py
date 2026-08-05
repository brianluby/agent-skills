#!/usr/bin/env python3
"""Scrape GitHub skills into a Turso/SQLite DB.

This is a bounded, read-only scraper. It discovers repositories with the
GitHub search API, walks their Git trees for SKILL.md files, fetches file
contents, extracts frontmatter, scans every SKILL.md for hidden Unicode, and
persists everything to a SQLite database compatible with Turso (libSQL).

It does not clone, push, or modify any repository. It only reads public data
through the GitHub API and tokens already available to `gh`.

Usage:
  ./scripts/scrape_github_skills.py --db db/skills.db
  ./scripts/scrape_github_skills.py --db db/skills.db --per-query 25 --max-repos 20
  ./scripts/scrape_github_skills.py --db db/skills.db --no-hidden-unicode-scan

Environment:
  GITHUB_TOKEN  optional, used automatically if set
  GH_TOKEN      optional, used automatically if set

The script uses `gh api` when authenticated (respects rate limits and your
login) and falls back to unauthenticated curl otherwise.
"""
from __future__ import annotations
import argparse
import base64
import json
import hashlib
import os
import sqlite3
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from typing import Any
from collections import Counter
from pathlib import Path
from urllib.parse import quote

DB_PATH = Path("db/skills.db")
# Source searches supplied by the user.
SEARCH_QUERIES = {
    "claude+skills+marketplace": "repositories",
    "agent+skills": "repositories",
    "SKILL.md": "code",
    "claude+code+skills": "repositories",
}

# Unicode categories that are normally invisible or suspicious inside source
# text. We deliberately ignore common whitespace and formatting that is normal
# in Markdown/code.
SUSPICIOUS_CATEGORIES = {
    "Cc": "control character",
    "Cf": "format character",
    "Cs": "surrogate",
    "Co": "private use",
    "Mn": "non-spacing mark",
    "Me": "enclosing mark",
    "Zl": "line separator",
    "Zp": "paragraph separator",
    "Zs": "space separator (non-ASCII)",
}

# Explicit high-signal codepoints that are common prompt-injection / spoofing
# vehicles even though their category might otherwise look benign.
EXTRA_SUSPICIOUS = {
    0x200B: "zero width space",
    0x200C: "zero width non-joiner",
    0x200D: "zero width joiner",
    0xFEFF: "byte order mark / zero width no-break space",
    0x2060: "word joiner",
    0x202E: "right-to-left override",
    0x202D: "left-to-right override",
    0x202A: "left-to-right embedding",
    0x202B: "right-to-left embedding",
    0x202C: "pop directional formatting",
    0x00A0: "non-breaking space",
    0x2028: "line separator",
    0x2029: "paragraph separator",
    0x2000: "en quad",
    0x2001: "em quad",
    0x2002: "en space",
    0x2003: "em space",
    0x2004: "three-per-em space",
    0x2005: "four-per-em space",
    0x2006: "six-per-em space",
    0x2007: "figure space",
    0x2008: "punctuation space",
    0x2009: "thin space",
    0x200A: "hair space",
    0x1680: "ogham space mark",
    0x180E: "mongolian vowel separator",
    0x034F: "combining grapheme joiner",
    0x061C: "arabic letter mark",
    0x2061: "function application",
    0x2062: "invisible times",
    0x2063: "invisible separator",
    0x2064: "invisible plus",
    0x2066: "left-to-right isolate",
    0x2067: "right-to-left isolate",
    0x2068: "first strong isolate",
    0x2069: "pop directional isolate",
    0x206A: "inhibit symmetric swapping",
    0x206B: "activate symmetric swapping",
    0x206C: "inhibit arabic form shaping",
    0x206D: "activate arabic form shaping",
    0x206E: "national digit shapes",
    0x206F: "nominal digit shapes",
    0x115F: "hangul choseong filler",
    0x1160: "hangul jungseong filler",
    0x3164: "hangul filler",
    0xFFA0: "halfwidth hangul filler",
    0x1D173: "musical symbol start tag",
    0x1D174: "musical symbol end tag",
    0x1D175: "musical symbol loop limit",
    0x1D176: "musical symbol short phrase",
    0x1D177: "musical symbol long phrase",
    0xE0000: "tag space",
    0xE0001: "language tag",
    0xE0002: "tag exclamation mark",
}

# Bidirectional overrides are especially dangerous for source spoofing.
BIDI_OVERRIDES = {0x202A, 0x202B, 0x202C, 0x202D, 0x202E, 0x2066, 0x2067, 0x2068, 0x2069}

# Unicode "Tag" characters (U+E0000..U+E007F) render invisibly but can encode
# arbitrary ASCII text. This is the primary vector used in skills prompt-
# injection (see mmassime/skills-injection-workshop). When present, we decode
# the run to recover the hidden instruction.
TAG_MIN = 0xE0000
TAG_MAX = 0xE007F
# Tag chars U+E0020 (space) .. U+E007E (tilde) map to ASCII 0x20..0x7E.


def _decode_tag_run(chars: list[str]) -> str:
    """Decode a run of Unicode tag characters into the embedded ASCII text."""
    out = []
    for ch in chars:
        delta = ord(ch) - TAG_MIN  # U+E0020 -> 0x20 (space), U+E0041 -> 0x41 ('A')
        # U+E0020..U+E007E map directly to ASCII 0x20..0x7E. U+E0001 (language
        # tag) and U+E007F (cancel tag) bracket the run and have no printable form.
        if 0x20 <= delta <= 0x7E:
            out.append(chr(delta))
        elif delta == 0x01:
            out.append("<TAG START>")
        elif delta == 0x7F:
            out.append("<TAG END>")
    return "".join(out)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
NAME_RE = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
DESC_RE = re.compile(r"^description:\s*(.+)$", re.MULTILINE)


def gh_api(path: str, params: dict | None = None) -> Any:
    """Call the GitHub API via `gh` when available, else curl."""
    # Accept either an API path ("/repos/...") or a full GitHub API URL
    # (returned by trees/blobs/search results). Do not double-prefix a full URL.
    if path.startswith("https://api.github.com"):
        url = path
    else:
        url = "https://api.github.com" + path
    if params:
        url += "?" + "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    if shutil.which("gh"):
        cmd = ["gh", "api", url]
    else:
        cmd = ["curl", "-fsSL", url]
        token = (
            subprocess.run(
                ["gh", "auth", "token"], capture_output=True, text=True
            ).stdout.strip()
            or ""
        )
        if not token:
            token = os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GH_TOKEN", "")
        if token:
            cmd += ["-H", f"Authorization: Bearer {token}"]
    for attempt in range(4):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
            return json.loads(out)
        except subprocess.CalledProcessError as exc:
            msg = exc.stderr or exc.stdout
            if "rate limit" in msg.lower() or exc.returncode == 403:
                wait = min(30, 3 * (attempt + 1))
                print(f"[warn] rate limited, sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"gh api failed for {url}")


def scan_hidden_unicode(text: str) -> list[dict]:
    """Return a list of suspicious codepoints and decoded tag-injection runs."""
    findings: list[dict] = []
    lines = text.splitlines(keepends=True)
    byte_offset = 0
    for line_no, line in enumerate(lines, start=1):
        col = 0
        chars = list(line)
        i = 0
        n = len(chars)
        # First pass: detect contiguous runs of Unicode Tag characters and
        # emit a single high-severity injection finding per run.
        while i < n:
            cp = ord(chars[i])
            if TAG_MIN <= cp <= TAG_MAX:
                run_start_col = i
                run_bytes = 0
                tag_chars = []
                while i < n and TAG_MIN <= ord(chars[i]) <= TAG_MAX:
                    run_bytes += len(chars[i].encode("utf-8"))
                    tag_chars.append(chars[i])
                    i += 1
                decoded = _decode_tag_run(tag_chars)
                findings.append(
                    {
                        "kind": "unicode_tag_injection",
                        "codepoint": f"U+{ord(tag_chars[0]):04X}..U+{ord(tag_chars[-1]):04X}",
                        "character_name": f"unicode tag run ({len(tag_chars)} chars)",
                        "byte_offset": byte_offset,
                        "line": line_no,
                        "column": run_start_col + 1,
                        "context": decoded[:200],
                    }
                )
                byte_offset += run_bytes
                col = i
                continue
            i += 1
            col += 1
            byte_offset += len(chars[i - 1].encode("utf-8"))

    # Second pass: per-character scan for other hidden/suspicious codepoints,
    # collapsing contiguous same-kind runs into a single row to avoid noise.
    for line_no, line in enumerate(lines, start=1):
        col = 0
        for ch in line:
            cp = ord(ch)
            # Skip visible ASCII / common printable characters.
            if cp == 0x0A or cp == 0x0D or cp == 0x09:
                byte_offset += len(ch.encode("utf-8"))
                col += 1
                continue
            if cp < 0x80:
                byte_offset += 1
                col += 1
                continue
            if TAG_MIN <= cp <= TAG_MAX:
                # Already reported as a consolidated injection run above.
                byte_offset += len(ch.encode("utf-8"))
                col += 1
                continue
            name = EXTRA_SUSPICIOUS.get(cp)
            if name is None:
                cat = unicodedata.category(ch)
                if cat in SUSPICIOUS_CATEGORIES:
                    name = SUSPICIOUS_CATEGORIES[cat]
                else:
                    byte_offset += len(ch.encode("utf-8"))
                    col += 1
                    continue
            kind = "bidi_override" if cp in BIDI_OVERRIDES else "hidden_unicode"
            # U+FE0F after an emoji is a normal variation selector.
            if cp == 0xFE0F and col > 0 and ord(line[col - 1]) > 0x2000:
                kind = "emoji_variation"
            # Collapse a run of the same kind into one finding row.
            prev = findings[-1] if findings else None
            if (
                prev
                and prev.get("kind") == kind
                and prev.get("line") == line_no
                and prev.get("codepoint") == f"U+{cp:04X}"
            ):
                byte_offset += len(ch.encode("utf-8"))
                col += 1
                continue
            start = max(0, col - 12)
            context = line[max(0, start - 1): col + 12].strip()
            findings.append(
                {
                    "kind": kind,
                    "codepoint": f"U+{cp:04X}",
                    "character_name": name,
                    "byte_offset": byte_offset,
                    "line": line_no,
                    "column": col + 1,
                    "context": context,
                }
            )
            byte_offset += len(ch.encode("utf-8"))
            col += 1
    return findings


def parse_frontmatter(content: str) -> tuple[str | None, str | None, dict]:
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None, None, {}
    fm_text = m.group(1)
    meta: dict = {}
    name = NAME_RE.search(fm_text)
    desc = DESC_RE.search(fm_text)
    skill_name = name.group(1).strip().strip('"').strip("'") if name else None
    description = desc.group(1).strip().strip('"').strip("'") if desc else None
    for line in fm_text.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip()
    return skill_name, description, meta


def ensure_db(conn):
    schema = Path(__file__).resolve().parent.parent / "db" / "schema.sql"
    conn.executescript(schema.read_text())
    conn.commit()


def upsert_repository(conn, repo: dict) -> int:
    cur = conn.execute(
        """
        INSERT INTO repositories (
            github_id, full_name, owner, name, html_url, description,
            default_branch, stars, forks, open_issues, archived, disabled,
            private, license_spdx_id, pushed_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(full_name) DO UPDATE SET
            stars=excluded.stars,
            forks=excluded.forks,
            open_issues=excluded.open_issues,
            archived=excluded.archived,
            disabled=excluded.disabled,
            private=excluded.private,
            description=excluded.description,
            pushed_at=excluded.pushed_at,
            updated_at=excluded.updated_at
        RETURNING id
        """,
        (
            repo.get("id"),
            repo["full_name"],
            repo["owner"]["login"],
            repo["name"],
            repo["html_url"],
            repo.get("description"),
            repo.get("default_branch"),
            repo.get("stargazers_count", 0),
            repo.get("forks_count", 0),
            repo.get("open_issues_count", 0),
            1 if repo.get("archived") else 0,
            1 if repo.get("disabled") else 0,
            1 if repo.get("private") else 0,
            (repo.get("license") or {}).get("spdx_id"),
            repo.get("pushed_at"),
            repo.get("updated_at"),
        ),
    )
    return cur.fetchone()[0]


def fetch_tree(repo_full_name: str, branch: str) -> list[dict]:
    """Walk the Git tree recursively to find SKILL.md files."""
    data = gh_api(f"/repos/{repo_full_name}/git/trees/{branch}", {"recursive": "1"})
    return [t for t in data.get("tree", []) if t.get("type") == "blob" and t["path"].endswith("SKILL.md")]


def insert_skill_file(conn, repo_id: int, path: str, blob: dict, discovered_by: str, scan: bool) -> int | None:
    raw_url = blob["url"]
    try:
        file_meta = gh_api(raw_url)
    except Exception as exc:
        print(f"[warn] could not fetch blob {path}: {exc}", file=sys.stderr)
        return None
    content_b64 = file_meta.get("content")
    if not content_b64:
        return None
    content = base64.b64decode(content_b64).decode("utf-8", "replace")
    sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
    skill_name, description, meta = parse_frontmatter(content)
    cur = conn.execute(
        """
        INSERT INTO skill_files (
            repository_id, path, html_url, raw_url, sha, skill_name,
            description, frontmatter_json, content, content_sha256, discovered_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(repository_id, path) DO UPDATE SET
            sha=excluded.sha,
            skill_name=excluded.skill_name,
            description=excluded.description,
            frontmatter_json=excluded.frontmatter_json,
            content=excluded.content,
            content_sha256=excluded.content_sha256
        RETURNING id
        """,
        (
            repo_id,
            path,
            file_meta.get("html_url") or raw_url,
            raw_url,
            blob.get("sha"),
            skill_name,
            description,
            json.dumps(meta, ensure_ascii=False),
            content,
            sha256,
            discovered_by,
        ),
    )
    skill_file_id = cur.fetchone()[0]
    if scan:
        findings = scan_hidden_unicode(content)
        for f in findings:
            conn.execute(
                """
                INSERT INTO skill_file_findings (
                    skill_file_id, kind, codepoint, character_name,
                    byte_offset, line, column, context
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    skill_file_id,
                    f["kind"],
                    f["codepoint"],
                    f["character_name"],
                    f["byte_offset"],
                    f["line"],
                    f["column"],
                    f["context"],
                ),
            )
    return skill_file_id


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=str(DB_PATH), help="SQLite/Turso database path")
    ap.add_argument("--per-query", type=int, default=20, help="repos per search query")
    ap.add_argument("--max-repos", type=int, default=40, help="max repos to process")
    ap.add_argument("--max-skills-per-repo", type=int, default=100,
                    help="cap SKILL.md files fetched per repository")
    ap.add_argument("--no-hidden-unicode-scan", action="store_true")
    args = ap.parse_args()

    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    ensure_db(conn)

    run = conn.execute(
        "INSERT INTO scrape_runs (source) VALUES ('github')"
    ).lastrowid
    conn.commit()

    try:
        repo_ids_seen: set[int] = set()
        processed = 0
        for query, kind in SEARCH_QUERIES.items():
            q_row = conn.execute(
                "INSERT INTO search_queries (query, kind) VALUES (?, ?) "
                "ON CONFLICT(query) DO UPDATE SET query=excluded.query RETURNING id",
                (query.replace("+", " "), kind),
            ).fetchone()
            query_id = q_row[0]
            if kind == "repositories":
                data = gh_api("/search/repositories", {"q": query, "per_page": args.per_query})
                for rank, repo in enumerate(data.get("items", []), start=1):
                    if processed >= args.max_repos:
                        break
                    repo_id = upsert_repository(conn, repo)
                    conn.execute(
                        "INSERT OR IGNORE INTO repository_search_hits (query_id, repository_id, run_id, rank) VALUES (?, ?, ?, ?)",
                        (query_id, repo_id, run, rank),
                    )
                    if repo_id in repo_ids_seen:
                        continue
                    repo_ids_seen.add(repo_id)
                    processed += 1
                    branch = repo.get("default_branch") or "main"
                    try:
                        files = fetch_tree(repo["full_name"], branch)
                    except Exception as exc:
                        print(f"[warn] tree failed for {repo['full_name']}: {exc}", file=sys.stderr)
                        continue
                    for blob in files[: args.max_skills_per_repo]:
                        insert_skill_file(
                            conn, repo_id, blob["path"], blob, "repository_tree",
                            not args.no_hidden_unicode_scan,
                        )
                    conn.commit()
            else:
                data = gh_api("/search/code", {"q": query, "per_page": min(args.per_query, 30)})
                for rank, item in enumerate(data.get("items", []), start=1):
                    repo = item["repository"]
                    repo_id = upsert_repository(conn, repo)
                    conn.execute(
                        "INSERT OR IGNORE INTO repository_search_hits (query_id, repository_id, run_id, rank) VALUES (?, ?, ?, ?)",
                        (query_id, repo_id, run, rank),
                    )
                    if repo_id in repo_ids_seen:
                        continue
                    repo_ids_seen.add(repo_id)
                    processed += 1
                    branch = repo.get("default_branch") or "main"
                    try:
                        files = fetch_tree(repo["full_name"], branch)
                    except Exception as exc:
                        print(f"[warn] tree failed for {repo['full_name']}: {exc}", file=sys.stderr)
                        continue
                    for blob in files[: args.max_skills_per_repo]:
                        insert_skill_file(
                            conn, repo_id, blob["path"], blob, "code_search",
                            not args.no_hidden_unicode_scan,
                        )
                    conn.commit()

        conn.execute("UPDATE scrape_runs SET status='completed', finished_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE id=?", (run,))
        conn.commit()
    except Exception as exc:
        conn.execute("UPDATE scrape_runs SET status='failed', error=? WHERE id=?", (str(exc), run))
        conn.commit()
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    finally:
        conn.close()

    print(f"[done] run {run}: processed repos={len(repo_ids_seen)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
