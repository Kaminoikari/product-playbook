---
description: Feature Extension Mode — Add a single feature to an existing product in 4 streamlined steps
argument-hint: <feature description>
---

Invoke the product-playbook skill.
Then read references/rules-build.md and jump directly to the "🔧 Feature Extension Quick Path" section.
When executing each step, load the corresponding reference files as indicated.

Execution mode: 🔧 Feature Extension Mode
Feature description: $ARGUMENTS

Follow the Feature Extension step sequence (S1 → S4). Load product context first per rules-context.md. Display a progress indicator at each step.

**S0 → S1 sequencing (important)**: If Context Bootstrap (S0) is triggered because `.product-context.md` is missing, you MUST complete Bootstrap and S1 in the **same turn**, then pause **after S1 completion** awaiting user confirmation before S2. Do NOT pause between S0 and S1 — even if some Bootstrap fields are still missing, write a baseline `.product-context.md` with placeholders, enter S1, and ask for the missing fields as part of the S1 confirmation question. See `references/rules-context.md` "Bootstrap → S1 Sequencing" for details.
