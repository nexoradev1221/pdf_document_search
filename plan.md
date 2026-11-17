# PDF Document Search — implementation plan

## Status and schedule

- Planning date: 2026-11-14. Foundation implementation began 2026-11-16; see the execution log.
- Duration: 14 daily sessions, 2026-11-15 through 2026-11-28 inclusive.
- Daily start: 10:00 Asia/Vladivostok (UTC+10).
- Scheduler status: ACTIVE. App task `implement-pdf-document-search-14-days` is attached to this conversation, daily at 10:00 Asia/Vladivostok, with a Nov 28 end date and a Nov 15 start guard. See `scheduled-task.md`.
- Source of scope: `requirements.md`, DEMO-SRS-03 v1.0.
- Repository: `nexoradev1221/pdf_document_search`.
- This is a fictional portfolio demonstration; never describe it as a paid client delivery or deployed production service.

## Requirements analysis

The core outcome is accurate, offline retrieval of passages by part code or fault term, with reliable links to the exact PDF page. Keyword search is mandatory; OCR and local semantic retrieval are optional capabilities that must not break it. The product must be independent of every other portfolio project.

| Requirement | Planned behavior | Verification |
| --- | --- | --- |
| FR-01 | Import multiple PDFs or recursively scan an explicitly selected folder; constrain traversal to that collection and avoid symlink loops. | Nested folders, duplicate imports, inaccessible paths and selected-root boundary tests. |
| FR-02 | Store document metadata, original filename, physical 1-based PDF page number, page text and per-page OCR status. | Multi-page and mixed text/image PDF fixtures; metadata and exact page assertions. |
| FR-03 | Extract native text without OCR; optionally OCR image-only pages locally. | Native-only operation without Tesseract, mixed-page behavior, OCR success and actionable missing-dependency errors. |
| FR-04 | Maintain a local SQLite FTS5 index; identify added, modified and missing files. | Repeat indexing is idempotent; replacements and deletions remove stale passages atomically. |
| FR-05 | Keyword, phrase and part-number search, ranked and filterable by document or collection/folder. | Phrase boundaries, punctuation in codes, Cyrillic, empty queries, invalid query syntax and filter isolation. |
| FR-06 | Show snippets, filename and physical PDF page; open that page in the bundled local viewer. | Reference corpus assertions and UI verification on multiple pages, including paths with spaces/Cyrillic. |
| FR-07 | Provide a separately enabled local semantic mode with a downloadable/pre-provisioned local model. | Default keyword mode needs no model; offline semantic operation after explicit setup; missing-model explanation. |
| FR-08 | Status, indexing failures, retry and removal controls. | Counts and state transitions; failures do not abort unrelated files; removal persists until explicit reimport. |

### Acceptance and delivery gates

- AT-01: An explicit fixture manifest maps known part codes to documents and 1-based pages; end-to-end searches return those exact pages.
- AT-02: Delete a source PDF and refresh its collection; all its passages disappear. Also test explicit removal while its source remains present, without silent reimport on routine refresh.
- AT-03: Enable OCR and index the synthetic scanned example; a known scanned code is searchable on the correct page. Run a real Tesseract integration test, not just a mock.
- AT-04: After dependencies, viewer assets and any opted-in model are installed locally, disable network access and demonstrate import, indexing, search and page opening.
- Deliver runnable source, pinned compatible dependencies, sample configuration, automated tests, at least 15 synthetic/redistributable PDFs including a scan, real application screenshots and a concise English README.
- Provide Russian end-user text and useful Russian error/status messages throughout the customer-facing UI.

## Proposed technical design

These are planning decisions to validate on day 1, not implemented components.

- Python application using PyMuPDF for extraction, SQLite FTS5 for lexical search, and a local FastAPI server with server-rendered pages and minimal JavaScript. Bind to loopback by default. No cloud service is needed.
- A locally bundled PDF.js viewer supports reliable physical-page navigation; avoid depending on external viewer behavior or CDN assets. Review and include relevant asset licenses.
- Optional Tesseract adapter works per image-only page with timeouts and explicit availability checks. Keep native PDF extraction usable when OCR is disabled or unavailable.
- Optional local embedding adapter uses a small locally provisioned model and cosine similarity suitable for the demo corpus; do not download models implicitly. Model redistribution/license and local memory use must be reviewed before choosing a model.
- Use standard-library SQLite access and versioned migrations. Separate PDF/OCR adapters, indexing, search and presentation so the business logic is testable without the UI.
- Suggested layout: `src/pdf_document_search/`, `tests/`, `scripts/`, `sample_data/`, `docs/`, `config.example.toml`, `pyproject.toml`, dependency lock file, `.github/workflows/`.
- Collections reference explicit roots. Documents track canonical path, fingerprint, metadata, indexing state and exclusion state. Pages retain unique document/page keys, native or OCR text, OCR status and failure details. FTS rows map to durable page IDs. Semantic vectors are optional and invalidated when text changes.
- Use size/mtime for quick detection plus content hashes for changed candidates; provide an explicit full validation refresh for timestamp-preserving changes. Replace a document's indexed pages transactionally. Clean lexical and semantic records together on removal.
- Keep original text for snippets and a normalized search representation for part numbers. Specify punctuation and case behavior with fixtures before implementing tokenization. Parameterize SQL and parse user search syntax instead of passing arbitrary input directly to FTS MATCH.
- Index in a serialized background worker with persistent run status; support cancellation and restart recovery. Do not run overlapping index writers.
- Resolve document IDs to known indexed paths; never expose an arbitrary file-serving path. Bound file sizes, rendered page sizes and OCR time. Escape snippets and metadata in HTML.
- Keep private corpora, local databases, model caches, logs, credentials and machine-specific configuration outside Git. Generate synthetic manuals rather than copying supplier manuals.
- Administrator denotes local maintenance controls; multiuser authentication/roles and internet hosting are outside the baseline local demo. Document this assumption clearly.

## Git workflow and commit policy

Use GitHub Flow: stable `main` plus short-lived `feat/...`, `fix/...`, `test/...` and `docs/...` branches. A separate long-lived `develop` branch is unnecessary for this single-contributor project.

1. Read the requirements, this plan, `AGENTS.md` and the execution log before each session. Inspect Git status and remotes; preserve unrelated work.
2. Fetch origin and update a clean `main` using fast-forward only. Create a focused branch from current main, or resume the relevant unfinished branch. Never force-push or rewrite published history.
3. Split a daily milestone into coherent reviewable changes: a behavior and its tests, an independent fix, a fixture addition or useful documentation. Commit after each complete, checked unit and push those commits regularly during the session. Aim for several meaningful commits when the work supports them; do not create empty or cosmetic churn to inflate counts.
4. Use clear messages such as `feat(index): refresh changed documents`, `test(search): cover hyphenated part codes`, or `fix(ocr): report missing executable`. Avoid staging the whole workspace blindly.
5. Push the branch with upstream tracking and create a PR with scope, requirements covered, validation and known limitations. Read the actual diff and run checks. For this project, the user's instruction authorizes merging completed passing milestones: merge with a merge commit after review and passing checks, then push/sync main. Keep failing or incomplete work on its branch with an accurate status.
6. If credentials, permissions or required tools block work, record the error and safe next step; continue independent local work. Never claim a failed push, skipped check or unscheduled run succeeded.
7. Update the execution log and milestone checkbox with evidence after completing work. No application implementation is authorized during the initial planning session.

## Daily milestones

Milestones are checked only after their verification gates complete. Dependencies take precedence over the calendar: resume unfinished prerequisite work before moving on, and record any date slip.

| Done | Day / date | Branch suggestion | Work and completion evidence |
| --- | --- | --- | --- |
| [ ] | 1 / Nov 15 | `chore/project-foundation` | Validate architecture, Windows/Python compatibility, FTS5 availability and dependency licenses (especially PyMuPDF and bundled viewer/model terms); create package, reproducible environment, sample config, lint/test setup and CI. Record technical decisions. |
| [ ] | 2 / Nov 16 | `test/synthetic-corpus` | Generate at least 15 synthetic PDFs, including native, scanned, mixed, multi-page, Cyrillic and known part-code cases. Add generator, provenance, deterministic fixture manifest and a corrupt-file test fixture. |
| [ ] | 3 / Nov 17 | `feat/collection-storage` | Add migrations, collections/documents/pages schema, local data paths and config validation. Test relationships, path identity, migrations and persistence. Then: Implement native text/metadata extraction with 1-based physical pages and image-only detection; isolate malformed/password-protected documents. Test mixed and empty pages. |
| [ ] | 4 / Nov 18 | `feat/collection-import` | Add multi-file import and recursive explicit-root discovery; handle duplicates, exclusions, nested paths, unreadable files and symlinks. Then: Build page-level FTS5 index and serialized job state; transactional updates, progress and cancellation/recovery. Test interrupted indexing and repeated runs. |
| [ ] | 5 / Nov 19 | `feat/index-refresh` | Add fingerprints, refresh, deletion cleanup, explicit document removal/exclusion and reimport. Verify AT-02 and stale-entry cleanup. |
| [ ] | 6 / Nov 20 | `feat/lexical-search` | Keyword/phrase/part-code parsing and normalization, ranking and safe queries. Test punctuation, exact fixture pages and Cyrillic; establish AT-01 at service level. Then: Document/folder filters, snippets, result pagination and structured result records. Test escaped content, scope isolation and deterministic ranking. |
| [ ] | 7 / Nov 21 | `feat/local-ui` | Local server, Russian navigation, collection/import controls and search form/results. Verify error/empty/loading states and keyboard access. |
| [ ] | 8 / Nov 22 | `feat/pdf-viewer` | Bundle local viewer assets, serve only registered PDFs, and open exact source pages. Run end-to-end AT-01 and path/HTML safety checks. Then: Russian status screen, counts, failure log, retry, refresh/removal confirmation and background-job progress. Verify partial failures remain recoverable. |
| [ ] | 9 / Nov 23 | `feat/optional-ocr` | Optional Tesseract setup and per-page adapter, timeout/error statuses and native-text bypass. Verify useful behavior without OCR installed. Then: Real OCR scan/mixed-document tests, scanned-code retrieval, reindex/cleanup and retry handling. Capture AT-03 evidence and document OCR limits. |
| [ ] | 10 / Nov 24 | `feat/local-semantic-search` | Opt-in local model configuration, page embeddings and separate semantic mode; cache invalidation/deletion and missing-model messaging. Keep keyword default. |
| [ ] | 11 / Nov 25 | `test/offline-search` | Verify semantic results and resource behavior on the corpus; execute AT-04 with external network disabled after setup. Check no CDN, telemetry or automatic model dependency. |
| [ ] | 12 / Nov 26 | `fix/reliability` | Investigate extraction/index/search failures, corrupted inputs, recovery, query injection/path traversal/XSS cases and practical performance. Record measured timings, environment and corpus sizes without unsupported speed claims. Then: Run integrated FR-01–08 and AT-01–04 matrix; test fresh install and optional dependencies absent/present. Fix identified behavior regressions in focused commits. |
| [ ] | 13 / Nov 27 | `docs/user-guide` | Write English install/test/usage/limitations README, Russian end-user help, configuration and troubleshooting, data/model licenses and fictional portfolio notice. Then: Run real demo, capture actual screenshots, document each acceptance scenario and expected outputs; verify distribution contains no private PDFs, logs, secrets or caches. |
| [ ] | 14 / Nov 28 | `chore/release-validation` | Reproduce installation and full checks from a clean checkout, reconcile requirements evidence, merge passing changes, tag a versioned demo release and record final deliverables/remaining limitations. Stop further implementation when complete. |

## Validation strategy

Use pytest for extraction, storage, query and indexing behavior; integration tests with actual SQLite FTS5 and PyMuPDF; opt-in real Tesseract/model tests; and browser end-to-end tests for import/search/status/page opening. CI must always exercise the native keyword path. Label optional test skips explicitly and execute the real optional acceptance paths locally before marking them done. Run targeted checks per commit and full relevant checks before merge; do not add tests that merely restate documentation or implementation structure.

The final evidence file should map each FR and AT to tests, commands, observed results and screenshots. Record failures honestly. No screenshots, passing tests or performance numbers exist at planning time.

## Risks and scope boundaries

- Exact part-code matching may conflict with FTS tokenization: resolve with explicit examples and dedicated normalization rather than guessing.
- OCR accuracy and language packs vary: use deterministic clear synthetic scans, document installed language data and never promise arbitrary scan accuracy.
- PDF extraction, models and viewer assets have license constraints: choose a compatible distribution approach and record notices before shipping. Change components if necessary.
- Semantic setup can be large: keep it opt-in and maintain a fully working lexical-only installation.
- A local folder chooser through a browser needs an explicit design: support entered local folder paths plus multi-PDF upload, validate paths and document loopback-only operation.
- Daily sessions depend on app scheduling access, available tools, network/authentication for pushes and sufficient run capacity. Leaving the app on alone does not activate a task or guarantee completion. Report blocked milestones and unfinished work at the end of the window rather than silently expanding scope or marking them complete.

## Execution log

| Date | Work | Validation / next step |
| --- | --- | --- |
| 2026-11-14 | Read requirements and prepared this 21-day plan; no application implementation. | GitHub account verified as nexoradev1221. Activate the app task using `scheduled-task.md`; begin day 1 on Nov 15. |

| 2026-11-14 | Revised the daily schedule to 14 sessions (Nov 15–28) at the user's request; combined related milestones without dropping requirements. | App task implement-pdf-document-search-14-days created and verified ACTIVE; no application implementation. |

| 2026-11-16 | Resumed the unfinished day-1 prerequisite on chore/project-foundation (day-2 corpus deferred). Added installable Python package, strict local TOML config, FTS5 diagnostic, pinned environment, AGPL license/component decisions, README and Windows/Linux CI. Fixed observed Russian diagnostic encoding. Commits 89a34a5, 8bab066, 3aaed10 pushed; PR #1: https://github.com/nexoradev1221/pdf_document_search/pull/1 . | Local Windows Python 3.12.10 / SQLite 3.49.1: 12 pytest tests pass, Ruff and pip check pass, FTS5/CLI probe passes. Diff reviewed; hosted checks pending, so milestone remains unchecked and no merge claimed. Next: inspect PR #1 CI, fix any failures and merge when passing; then generate the day-2 synthetic corpus. Read-only sandbox required approved escalations for project writes/network/runtime execution; approvals succeeded. No AT-01–04 completion claimed. |