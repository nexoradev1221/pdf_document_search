# Client Software Requirements — Searchable Maintenance Document Library

**Brief ID:** DEMO-SRS-03  
**Target Git repository:** `pdf_document_search`  
**Illustrative client:** Harbor Equipment Services (fictional)  
**Document status:** Initial client-facing requirements / portfolio simulation  
**Version:** 1.0 — 2026-11-14  

> **Portfolio scenario notice:** This is a fictional but realistic client brief written for a demonstration portfolio. It is not evidence of a real customer contract, completed paid work, or a deployed production system.


## 1. Client Background and Business Problem

A repair workshop maintains hundreds of supplier PDF manuals and internal service notes. Technicians regularly search the wrong manual or spend too long scrolling through scanned and text-based PDFs to locate a repair procedure.

## 2. Requested Business Outcome

A technician enters a part number or fault term and immediately sees relevant document passages with correct page references.

## 3. Expected Users

Office personnel and an administrator.

## 4. Functional Requirements

- **FR-01:** Import multiple PDFs and recursively index an explicitly selected document folder.
- **FR-02:** Extract text, filename, page number and document metadata; show OCR status for scanned pages.
- **FR-03:** Offer optional OCR for image-only pages, with ability to process already-text PDFs without OCR.
- **FR-04:** Build and update a local full-text index; detect modified/deleted files and refresh results.
- **FR-05:** Search by phrase, keyword and part number; allow filters by document or folder.
- **FR-06:** Display snippets, source filename and exact page; open the PDF on that page.
- **FR-07:** Allow an optional local semantic retrieval mode without replacing basic keyword search.
- **FR-08:** Provide an index status page, failure log and document removal action.

## 5. Input Data and Expected Outputs

- Input: a demo corpus of at least 15 synthetic/publicly redistributable PDFs including a scanned example.
- Output: ranked search results linked to exact source pages.

## 6. Acceptance Tests / Definition of Done

- **AT-01:** A query for a known part code returns the prepared reference document and correct page.
- **AT-02:** Removing a document from the selected collection removes it from subsequent search results after reindexing.
- **AT-03:** A scanned example is searchable after OCR is enabled.
- **AT-04:** Search remains functional offline after initial local setup.

## 7. Delivery Scope and Constraints

- **Suggested implementation:** Python/PyMuPDF, SQLite FTS5; optional Tesseract and embeddings. No third-party copyrighted manuals distributed without permission.
- Deliver a runnable application, complete source code, dependency files, sample configuration, automated tests, sample dataset, and real screenshots of the running application.
- Include a concise English README with setup, test, usage, and limitations; provide Russian end-user wording where the application is customer-facing.
- Operate as its own product with its own repository, data and configuration. It must never require any of the other nine portfolio projects.
- Avoid paid third-party services for the core demo; where a platform account or external credentials are required, provide a local simulator or clearly documented sample mode.
- Do not place secrets, confidential documents, genuine personal records, or copyrighted customer assets in the public repository.
- Deliver only the listed baseline features; production hosting, ongoing maintenance, advanced integrations, and additional scope require separate agreement.

## 8. Final Deliverables

1. Public-ready source repository named `pdf_document_search`.
2. Runnable demonstration with synthetic or properly licensed sample data.
3. Installation and operating instructions, screenshots and automated tests.
4. Demonstration of all acceptance tests listed in Section 6.

## 9. Assumptions and Open Points

- The client scenarios and example volumes are illustrative and should be validated before real commercial development.
- UI layout, detailed database schema, security hardening, deployment targets and deadlines will be specified during technical design.
- Any expansion beyond the basic scope is subject to a new estimate and a revised requirements version.
