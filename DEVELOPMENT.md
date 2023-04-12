Regarding Development Branches in this Repository
=============

- The `dev` branch may contain code that has not yet been released.
- The `master` branch tracks the versions that have been released.
- The `autorelease` branch is used for GitHub automation.

To release new code:
- Push the code to the dev branch and confirm that the commit passes the pytest.
- Update the PSL file.
- Change the version number in the setup.py file to X.Y.Z. (The date should not be included.)
- Push the changes to the master branch.

Once the new commit has been successfully verified by GitHub actions, it will be tagged as `vX.Y.Z`.
GitHub actions will create a new package with a version number like `X.Y.Z.YYYYmmdd`.

