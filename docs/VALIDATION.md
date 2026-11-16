# Validation

Validated on Python 3.12 on Linux, 16 November 2026.

| Check | Result |
| --- | --- |
| Full suite, serial | 22 passed |
| Full suite, two xdist workers | 22 passed |
| Chained workflow by itself | 1 passed |
| Smoke marker selection | 2 passed, 20 deselected |

HTML and JUnit generation succeeded. All tests used the local reference API; no
third-party API was contacted. Python 3.13/3.14 and Windows execution remain for
CI/user validation. CI configuration is included; local results do not imply
that GitHub Actions has run. Generated reports are ignored by Git.
