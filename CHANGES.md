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


