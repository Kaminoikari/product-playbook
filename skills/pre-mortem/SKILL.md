---
name: pre-mortem
description: Use when you need to surface how a product, feature, or plan could fail before committing to it, especially before a go/no-go decision. Triggers on "pre-mortem", "what could go wrong", "failure modes", "risks", "how might this fail", and the same intent in any language.
---

# Pre-mortem

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce pre-mortem output, contribute the framework tag `Pre-mortem` to the meta-skill's provenance line.

## Framework

<!-- migrated verbatim from references/04b-solutions.md §3.3 -->

## 3.3 Shreyas Doshi's Pre-mortem

**Applicable: Medium/high completeness / audience is engineers/internal planning**

Before committing to a solution, assume it has already failed:

```
Assume: We chose Solution X and declared failure after [time period]. Why did it fail?

| Failure Reason | Likelihood (High/Med/Low) | Preventability (High/Med/Low) | Preventive Measure |
|----------------|--------------------------|-------------------------------|-------------------|
| | | | |
```

**Security failure scenarios** (must consider at least one, especially for products handling user data):

```
| Security Risk | Likelihood | Preventability | Preventive Measure |
|---------------|-----------|----------------|-------------------|
| User data breach (database intrusion, unauthorized API access) | | | |
| Mass account takeover (brute force, credential stuffing) | | | |
| API abuse (no rate limiting, mass scraping) | | | |
| XSS / CSRF attacks harming users | | | |
| Accidental exposure of sensitive data (secrets in version control, passwords in logs) | | | |
```

> If the product doesn't involve user authentication or sensitive data, mark as "Not applicable" and explain why.
