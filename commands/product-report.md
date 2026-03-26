---
description: Generate HTML Planning Report — Compile all product planning content into a single offline-readable HTML report
---

Invoke the product-playbook skill. Then read references/06-html-report.md.

Based on the product planning content completed in the current conversation, generate a full HTML planning report following the design specs in 06-html-report.md:
- Single HTML file (CSS + JS inline, Google Fonts CDN loading Noto Sans TC)
- Dynamically render completed stages; skip any stages not yet completed
- Include sticky table-of-contents navigation, card-based layout, and interactive effects

If no product planning content exists in the conversation, prompt the user to run a product planning flow first.
