# BBCode-to-HTML
A simple Flet app that converts a BBCode document to HTML.

Tags supported:
- `[b]` (bold) -> `<strong>`
- `[i]` (italic) -> `<em>`
- `[quote]` -> `<blockquote>`
- `[hr]` -> `<hr />`

Two modes (will auto-detect which is needed):
- Detects paragraphs by double-linefeed (double-spaced paragraphs), single linefeeds are replaced with `<br />`
- Detects paragraphs by single-linefeed (single-spaced paragraphs).

In both modes a single, blank line will be removed.

—Damaged
