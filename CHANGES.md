### 1.1.1, 1.1.2 (2026-10-21)

No code changes. This release only refreshes CI and development tooling.

- Update `astral-sh/setup-uv` to v10.3.0 in the GitHub Actions workflows.
- Refresh `uv.lock`, updating `certifi` to pick up the bundled CA certificate
  changes.
- Fix the auto-release workflow so that it no longer bundles a stale PSL file.

### 1.1.0 (2026-10-10)

This version drops support for Python 3.5, 3.6 and 3.7, and now requires
Python 3.8 or later.

Packaging has been migrated to PEP 621 metadata in `pyproject.toml` using
hatchling, replacing `setup.py`, `setup.cfg` and `MANIFEST.in`. The version is
now read from `publicsuffixlist.__version__`, and development dependencies are
locked with uv.

- Add PEP 561 `py.typed` marker and complete type annotations for the public
  API, including `compat` and the update script.
- Add an `accept_unknown` keyword argument to `is_private()` and `is_public()`.
- Fix `subdomain()` to honor the per-call `accept_unknown` argument, and to
  return `None` for invalid domains instead of raising `TypeError`.
- Correct the `subdomain()` and `privateparts()` overload signatures.
- Handle a malformed `Last-Modified` response header in the update script.
- Run tests with uv on Python 3.8 and 3.14, and update CI actions.

### 1.0.2 (2024-07-13)
- Use @typing.overload to indicate str-to-str domain input/output. #32.
- Address deprecation of ByteString in python 3.14.

### 1.0.1 (2024-06-22)
Fix internal logic where domain name passed as a tuple of bytes, that contains
UTF-8 encoded non-ascii chars, unintentionally matched PSL. Fixes #31.

### 1.0.0 (2024-06-20)

This version drops support for Python 2.x and 3.4.

The internal logic has been slightly changed to address conflicting evaluation
rules between the PSL wiki and the test data.
As with versions before 1.0.0, this module assumes that wildcards have
implicit public declarations on the wildcard root.

With the minimum Python version changed to 3.5, type annotations have
been added to exposed API methods to clarify expected input types.
For example, psl.publicsuffix() now accepts `str` or `Tuple[bytes, ...]`.

- Add tuple of bytes style input
- Add keep_case keyword argument
- Accept trailing dot
- Migrate CI to GitHub Actions


### 0.10.0 (2023-04-29)

The last version works on Python 2.7


