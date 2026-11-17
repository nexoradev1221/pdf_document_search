# Foundation decisions — 2026-11-16

Python 3.12 is the supported baseline. The local Windows runtime is CPython 3.12.10 (64 bit), SQLite 3.49.1; the FTS5 create/insert/query probe succeeds. CI also targets Linux with Python 3.12; its results must be verified independently.

Use the proposed PyMuPDF / SQLite FTS5 / FastAPI architecture. The foundation does not index documents or serve a UI yet. Configuration is strict, defaults to loopback, resolves data paths beside its file, and never enables optional services implicitly.

## Licenses and distribution

- PyMuPDF/MuPDF offers AGPL or a commercial license: https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright . Use the open-source AGPL path for this public source demonstration; project code is AGPL-3.0-only and includes the license text. Preserve dependency notices and provide corresponding source for shipped components as required. No closed-source distribution or commercial license is assumed.
- FastAPI is MIT: https://fastapi.tiangolo.com/ . SQLite is public domain: https://sqlite.org/copyright.html .
- PDF.js is Apache-2.0: https://github.com/mozilla/pdf.js/blob/master/LICENSE . It has not been bundled yet; when selected, pin assets and preserve its license/notice files.
- Tesseract and any model require their own pinned provenance, notices and setup verification at their milestones. No model has been selected or downloaded. Do not assume all model weights share the library's license.
- Review the resolved package metadata/notices before distribution; this document is an engineering decision, not a promise of legal review.

The package install is pinned in requirements-dev.lock, including build/test tools. No dependency on another portfolio project is permitted. OCR and semantic acceptance, corpus generation, production packaging and screenshots are pending.
