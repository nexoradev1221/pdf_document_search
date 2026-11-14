# Daily implementation task configuration

**Status: ACTIVE, verified in the app on 2026-11-14.** Task ID: `implement-pdf-document-search-14-days`. A local recurring task is attached to the current conversation.

- Name: Implement PDF Document Search
- Runtime: local, with access to this project folder, Git, Python and GitHub CLI.
- Working directory: `D:\Portfolio\pdf_document_search`
- Time: daily at 10:00, timezone `Asia/Vladivostok` (UTC+10).
- First run: 2026-11-15. Last planned run: 2026-11-28 (14 runs).
- The registered schedule ends on November 28. The prompt also prevents implementation before November 15, after November 28, or after completion. No implementation run was requested during setup.
- Repository: https://github.com/nexoradev1221/pdf_document_search

## Task prompt

Work on the local project at D:\Portfolio\pdf_document_search and its GitHub repository nexoradev1221/pdf_document_search. The user authorizes daily implementation from November 15 through November 28, 2026 inclusive, following plan.md, with frequent meaningful commits and pushes. Use Asia/Vladivostok for calendar dates. Before November 15, do not implement. After November 28, or once the project is complete, do not continue implementation; report current completion/blockers and disable this task if supported.

First read AGENTS.md, requirements.md, plan.md, the execution log, Git status, current branches and remotes. Follow the English correction instruction in AGENTS.md. Resume incomplete prerequisites and the next unchecked milestone, using the day/date as a target rather than permission to skip unfinished work. Make bounded daily progress and record evidence so a fresh session can resume. Never overlap another implementation run; if a run is still active, skip this run and report it.

Use short-lived feature/fix/test/docs branches from current main. Preserve unrelated user changes. Fetch and fast-forward safely. Implement the day's behavior and meaningful tests, commit coherent small completed units with descriptive messages, and push the branch regularly. Do not inflate commit counts with empty commits, artificial changes, or backdated history. Review the diff, run relevant checks, create a PR with validation, and merge passing completed milestones with a merge commit; keep unfinished or failing work on its branch. Never force-push, reset away user work, disclose credentials, or commit private documents/caches/local configuration. The user has authorized the project repository creation, project commits, pushes, PRs and merges for completed passing milestones.

Deliver a standalone offline local PDF search app with Russian customer-facing wording, native keyword search, optional OCR and optional local semantic search, at least 15 synthetic/redistributable PDF examples, exact-page results, status/removal controls, automated acceptance evidence, English README and real screenshots. Use only the baseline requirements and plan; no production hosting, paid services or dependencies on other portfolio projects. Validate optional dependencies and licenses before adopting them.

At each run's end, update plan.md with checked completed milestones, a dated execution-log entry, tests actually run/results, branch/commit/PR references, push/merge outcome and the next concrete action. Distinguish skipped tests and local-only commits from successful validation and pushes. If a permission, missing dependency, authentication issue or capacity limit blocks progress, record it and continue independent safe work; report what input is needed without inventing success. Stop after completing the final milestone and provide the delivery/acceptance summary.
