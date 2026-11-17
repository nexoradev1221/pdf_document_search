# PDF Document Search

A fictional maintenance-document search portfolio demonstration. This is not a paid client delivery or a deployed production service.

**Current state:** project foundation and read-only runtime diagnostics. PDF import, search, OCR, viewer and sample corpus are scheduled in [plan.md](plan.md); they are not implemented yet.

Python 3.12, including SQLite FTS5, is required. In PowerShell:

```powershell
py -3.12 -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements-dev.lock
.venv/Scripts/python.exe -m pip install --no-build-isolation --no-deps -e .
.venv/Scripts/python.exe -m pdf_document_search --config config.example.toml
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m ruff check .
```

The diagnostic probes FTS5 in memory and reads configuration without creating application data or contacting services. Relative data paths resolve beside the config file. Only loopback IP addresses are accepted. OCR and semantic modes default to disabled.

The lock file pins the Python 3.12 foundation environment; first installation needs package access. Offline installation from a prepared wheelhouse and actual offline application acceptance remain later milestones. Optional OCR/model packages are not installed implicitly. Keep private PDFs and local state out of Git.

See [technical decisions](docs/technical-decisions.md) for component licensing and delivery constraints. Project code is licensed under AGPL-3.0-only; see LICENSE. Dependencies retain their own licenses.
