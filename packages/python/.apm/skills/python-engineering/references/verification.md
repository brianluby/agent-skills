# Python verification

Use the repository's environment and lock manager (`uv`, Poetry, PDM, Hatch, tox, nox, pip-tools, or a documented virtualenv). Do not create a second environment or update dependencies merely to run tests.

## Focused loop

Invoke configured tools through project scripts where present. Common underlying commands are:

```sh
ruff format --check <paths>
ruff check <paths>
pytest path/to/test_file.py -q
mypy <package>
# or the configured pyright command
```

Use the actual configured formatter, linter, test runner, and type checker rather than adding preferred tools.

## Escalation

- Run the package/full suite when shared fixtures, plugins, models, configuration, or public interfaces changed.
- Use tox/nox/CI matrices for supported Python versions; the current interpreter alone does not establish compatibility.
- Build wheel and sdist for packaging, metadata, package-data, entry-point, or import-layout changes, then inspect their contents. In a clean disposable environment, install the built wheel and smoke-test public imports and CLI entry points; when source-distribution correctness matters, also build a wheel from the sdist and test that artifact.
- Run async tests with the project's event-loop policy and include cancellation/timeout behavior where relevant.
- Test locale, timezone, filesystem, encoding, and platform boundaries only when the code depends on them.
- For database/network code, distinguish unit tests from integration tests and use the repository's provisioned services.
- Run security/dependency checks already configured by the project after dependency or boundary changes.

Keep tests deterministic: control time/randomness, isolate environment variables, close resources, and avoid order dependence. Never report skipped or unavailable checks as passing.
