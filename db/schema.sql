PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS scrape_runs (
  id INTEGER PRIMARY KEY,
  started_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  finished_at TEXT,
  source TEXT NOT NULL DEFAULT 'github',
  status TEXT NOT NULL DEFAULT 'running',
  error TEXT
);

CREATE TABLE IF NOT EXISTS search_queries (
  id INTEGER PRIMARY KEY,
  query TEXT NOT NULL UNIQUE,
  kind TEXT NOT NULL CHECK (kind IN ('repositories', 'code')),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  last_scraped_at TEXT
);

CREATE TABLE IF NOT EXISTS repositories (
  id INTEGER PRIMARY KEY,
  github_id INTEGER UNIQUE,
  full_name TEXT NOT NULL UNIQUE,
  owner TEXT NOT NULL,
  name TEXT NOT NULL,
  html_url TEXT NOT NULL,
  description TEXT,
  default_branch TEXT,
  stars INTEGER NOT NULL DEFAULT 0,
  forks INTEGER NOT NULL DEFAULT 0,
  open_issues INTEGER NOT NULL DEFAULT 0,
  archived INTEGER NOT NULL DEFAULT 0,
  disabled INTEGER NOT NULL DEFAULT 0,
  private INTEGER NOT NULL DEFAULT 0,
  license_spdx_id TEXT,
  pushed_at TEXT,
  updated_at TEXT,
  scraped_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE TABLE IF NOT EXISTS repository_search_hits (
  query_id INTEGER NOT NULL REFERENCES search_queries(id) ON DELETE CASCADE,
  repository_id INTEGER NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
  run_id INTEGER NOT NULL REFERENCES scrape_runs(id) ON DELETE CASCADE,
  rank INTEGER NOT NULL,
  matched_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  PRIMARY KEY (query_id, repository_id, run_id)
);

CREATE TABLE IF NOT EXISTS skill_files (
  id INTEGER PRIMARY KEY,
  repository_id INTEGER NOT NULL REFERENCES repositories(id) ON DELETE CASCADE,
  path TEXT NOT NULL,
  html_url TEXT NOT NULL,
  raw_url TEXT NOT NULL,
  sha TEXT,
  skill_name TEXT,
  description TEXT,
  frontmatter_json TEXT,
  content TEXT NOT NULL,
  content_sha256 TEXT NOT NULL,
  discovered_by TEXT NOT NULL CHECK (discovered_by IN ('repository_tree', 'code_search')),
  scraped_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  UNIQUE (repository_id, path)
);

CREATE TABLE IF NOT EXISTS skill_file_findings (
  id INTEGER PRIMARY KEY,
  skill_file_id INTEGER NOT NULL REFERENCES skill_files(id) ON DELETE CASCADE,
  kind TEXT NOT NULL CHECK (kind IN ('hidden_unicode', 'bidi_override', 'emoji_variation', 'unicode_tag_injection')),
  codepoint TEXT NOT NULL,
  character_name TEXT NOT NULL,
  byte_offset INTEGER NOT NULL,
  line INTEGER NOT NULL,
  column INTEGER NOT NULL,
  context TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE VIRTUAL TABLE IF NOT EXISTS skill_files_fts USING fts5(
  skill_name,
  description,
  content,
  repository_full_name UNINDEXED,
  path UNINDEXED,
);

CREATE TRIGGER IF NOT EXISTS skill_files_ai AFTER INSERT ON skill_files BEGIN
  INSERT INTO skill_files_fts(rowid, skill_name, description, content, repository_full_name, path)
  SELECT new.id, new.skill_name, new.description, new.content, repositories.full_name, new.path
  FROM repositories
  WHERE repositories.id = new.repository_id;
END;

CREATE TRIGGER IF NOT EXISTS skill_files_ad AFTER DELETE ON skill_files BEGIN
  INSERT INTO skill_files_fts(skill_files_fts, rowid, skill_name, description, content, repository_full_name, path)
  VALUES('delete', old.id, old.skill_name, old.description, old.content, '', old.path);
END;

CREATE TRIGGER IF NOT EXISTS skill_files_au AFTER UPDATE ON skill_files BEGIN
  INSERT INTO skill_files_fts(skill_files_fts, rowid, skill_name, description, content, repository_full_name, path)
  VALUES('delete', old.id, old.skill_name, old.description, old.content, '', old.path);
  INSERT INTO skill_files_fts(rowid, skill_name, description, content, repository_full_name, path)
  SELECT new.id, new.skill_name, new.description, new.content, repositories.full_name, new.path
  FROM repositories
  WHERE repositories.id = new.repository_id;
END;

CREATE INDEX IF NOT EXISTS idx_repositories_owner ON repositories(owner);
CREATE INDEX IF NOT EXISTS idx_repositories_stars ON repositories(stars DESC);
CREATE INDEX IF NOT EXISTS idx_skill_files_repository ON skill_files(repository_id);
CREATE INDEX IF NOT EXISTS idx_skill_files_name ON skill_files(skill_name);
CREATE INDEX IF NOT EXISTS idx_skill_files_content_sha ON skill_files(content_sha256);
CREATE INDEX IF NOT EXISTS idx_skill_file_findings_file ON skill_file_findings(skill_file_id);
CREATE INDEX IF NOT EXISTS idx_skill_file_findings_kind ON skill_file_findings(kind);
