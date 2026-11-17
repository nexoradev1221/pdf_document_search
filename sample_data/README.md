# Synthetic maintenance corpus

All 15 valid PDFs are original fictional examples generated locally by
`scripts/generate_corpus.py`. No supplier manuals, client records, external
images or real repair procedures are included. The content is distributed
under the project's AGPL-3.0-only license; embedded font resources retain
their upstream Artifex/URW notices (see FONT-NOTICE.md and FONT-LICENSE.txt).

The corpus includes 12 native-text manuals, one fully image-only scan, one
mixed native/image document and one Russian manual with a Cyrillic filename.
Each has three physical pages. `corpus/manifest.json` records file hashes,
page types and a unique part-code/fault-term reference on physical page 2.
Scanned pages deliberately contain no text layer. Actual OCR/search acceptance
is pending its implementation; a manifest reference is not proof of retrieval.

Recreate into a **new or empty** directory with the pinned environment:

```powershell
.venv/Scripts/python.exe scripts/generate_corpus.py path/to/new-corpus
```

Existing nonempty output directories are rejected to protect user files.
With the pinned PyMuPDF build, repeated generation is byte-for-byte stable.
Changing the renderer/library version may change hashes and requires explicit
fixture regeneration/review. Use a temporary output for regeneration, review
the diff, and replace tracked fixtures deliberately.

The intentionally invalid `tests/fixtures/corrupt.pdf` is separate from the
15 valid demo PDFs. Tests verify exact native-text pages, image-only/mixed
structure, metadata, hashes, Cyrillic extraction and deterministic generation.
