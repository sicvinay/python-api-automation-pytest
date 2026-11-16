# From practice scripts to a reusable suite

This project retains the original learning goals while changing the test target
from third-party services to a self-contained documented demo contract.

| Earlier issue | Resolution |
| --- | --- |
| Absolute Windows paths and missing payloads | Committed synthetic JSON loaded relative to the test module |
| Network calls during import | All calls happen inside tests or fixtures |
| Hardcoded student IDs | Per-test API-created records with fixture cleanup |
| POST/PUT form encoding | Shared client uses `json=` |
| Print-only checks | Assertions for status, response fields and readback |
| Global IDs and dependent tests | Fixture dependencies and self-contained workflow |
| Duplicate function names | Unique lowercase discoverable tests |
| Unbounded requests | Explicit configurable client timeout |
| Open file handles and global fixture state | Context managers and yielded session fixtures |
| Fixed external availability assumptions | Isolated reference HTTP server per worker |
| Assertion-free Pytest tutorials | Replaced by meaningful functional tests with markers/fixtures |
| Missing dependencies and CI | Pinned top-level requirements and Actions matrix |
| Environments, reports and IDE files in upload | Excluded from clean source and Git ignore rules |

ReqRes examples are not retained as misleading live integrations. There is no
claim of external service coverage. The original uploaded ZIP remains the
historical source; its Git metadata and generated HTML reports are not imported.
Do not copy its old Git history into this repository without a separate audit.
