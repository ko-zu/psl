Regarding Development Branches in this Repository
=============

- The `dev` branch may contain code that has not yet been released.
- The `master` branch tracks the versions that have been released.
- The `autorelease` branch is used for GitHub automation.

Dependencies are managed with uv and pinned in `uv.lock`. Run the tests with
`uv run python -m publicsuffixlist.test`.

To release new code:
- Push the code to the dev branch and confirm that the commit passes the tests.
- Update the PSL file.
- Change the `__version__` value in the `publicsuffixlist/__init__.py` file to
  X.Y.Z. (The date should not be included.)
- Push the changes to the master branch.

Once the new commit has been successfully verified by GitHub actions, it will be tagged as `vX.Y.Z`.
GitHub actions will create a new package with a version number like `X.Y.Z.YYYYmmdd`.
