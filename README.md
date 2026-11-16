# Python API Automation with Pytest

A runnable API testing portfolio project covering CRUD, validation, fixtures,
request chaining, reporting and parallel execution with Python and Requests.
Refactored from my earlier API automation practice scripts.

## Quick start

Requires Python 3.12 or newer. From the repository root:

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate on macOS/Linux:

```bash
source .venv/bin/activate
```

Then install and run:

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m pytest -n 2 --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in a browser. Logs are written to
`reports/test_execution.log`; with parallel execution, prefer the per-test
captured logs in the HTML report because file output may interleave.

## What the suite demonstrates

- Create, read, update and delete a student, with status and body assertions.
- Build student → technical skills → address → full-details workflows.
- Reject invalid fields, incorrect payload encoding and missing resources.
- Use function-scoped fixtures for unique data, cleanup and HTTP sessions.
- Run individual tests or multiple workers without global IDs or ordering.
- Use a shared client with explicit JSON encoding, timeouts and bounded logging.
- Generate HTML/JUnit reports and run the suite in GitHub Actions.

## A repeatable demo API

By default, tests start an in-process HTTP server on a random loopback port.
Requests still travel over HTTP through `requests.Session`; no request methods
are mocked. Each Pytest worker owns an isolated server. The server is a reference
implementation for demonstrating automation, **not validation of an independent
production API**. Its state is discarded after the run.

The original scripts used ReqRes and Testing World endpoints and local payload
files that were not included. Those service dependencies have been replaced
with the documented local contract so a fresh clone is runnable. The optional
external mode requires an API implementing this project's contract; this is
not a drop-in suite for the original services.

## Useful commands

```bash
python -m pytest -m smoke
python -m pytest -m negative
python -m pytest tests/test_students.py::test_student_skills_address_workflow
python -m pytest --collect-only -q
```

## Optional external test environment

Only use a disposable environment you control, implementing
[the API contract](docs/API_CONTRACT.md). This mode creates, updates and deletes
records. Cleanup only targets records created by the current test.

```bash
python -m pytest --base-url https://your-test-api.example --allow-external-writes
```

No external environment is needed for normal execution. Never commit API tokens
or personal/production data. Authentication for another service must be added
in the client using environment-provided credentials; it is not configured here.

## Layout

| Path | Responsibility |
| --- | --- |
| `api/client.py` | HTTP session, timeout and request logging |
| `api/students.py` | Resource operations |
| `data/student.json` | Portable synthetic payload template |
| `tests/conftest.py` | Server, client, data and cleanup fixtures |
| `tests/test_students.py` | Functional and negative API tests |
| `tests/test_client.py` | Client transport and timeout checks |
| `tests/support/demo_api.py` | Local reference API |
| `.github/workflows/tests.yml` | Python 3.12–3.14 CI and report artifacts |

## Refactoring notes

See [the migration notes](docs/REFACTORING.md) for how the earlier learning scripts
map to this implementation and which assumptions changed.
