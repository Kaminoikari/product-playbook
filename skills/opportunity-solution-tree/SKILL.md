---
name: opportunity-solution-tree
description: Use when the user wants to connect a desired outcome to opportunities and candidate solutions in a structured tree. Triggers on "opportunity solution tree", "OST", "map opportunities", "outcome to solutions", "Teresa Torres", and the same intent in any language.
---

# Opportunity Solution Tree

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce opportunity solution tree output, contribute the framework tag `OST` to the meta-skill's provenance line (`— Frameworks: … · OST · …`).

## Framework

<!-- migrated verbatim from references/02c-ost-journey.md §1.4 (lines 3-25; deprecated-mode Applicable gating line dropped) -->

## 1.4 Opportunity Solution Tree (OST)

The OST starts from the product goal and systematically connects opportunities to solutions:

```
[Product Goal / Desired Outcome]
    │
    ├── [Opportunity 1: User pain point or need]
    │       ├── [Solution 1a]
    │       └── [Solution 1b]
    ├── [Opportunity 2: User pain point or need]
    │       └── [Solution 2a]
    └── [Opportunity 3: User pain point or need]
            └── [Solution 3a]
```

Core principles:
- The goal (Outcome) is a measurable result, not a feature or output
- Opportunities come from user research, not internal brainstorming
- Solutions map to opportunities — don't skip opportunities and jump straight to solutions
- Go broad, then deep: list all opportunities first, then explore solutions one by one
