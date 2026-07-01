---
name: pr-faq
description: Use when the user wants to define a product by writing its launch press release and FAQ before building. Triggers on 'PR-FAQ', 'press release', 'working backwards', 'Amazon PR FAQ', 'write the launch announcement', and the same intent in any language.
---

# PR-FAQ (Working Backwards)

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce PR-FAQ output, contribute the framework tag `PR-FAQ` to the meta-skill's provenance line (`— Frameworks: … · PR-FAQ · …`).

## Framework

<!-- migrated from references/04a-prfaq.md (whole file); the original always-on-blocking enforcement framing is softened into a proportional quality self-check, per this phase's migration rules -->

# Phase 3: Develop — PR-FAQ (Working Backwards)

## 3.1 Amazon's Working Backwards Method (PR-FAQ)

Start by writing the product press release — it forces you to work backwards from the customer outcome:

```
## [Product Name] Press Release

**Headline**: [What can the user achieve? One sentence.]
**Subheadline**: [What problem does it solve, and for whom?]

**Opening Paragraph (Aha Moment)**:
[Describe the moment the user experiences the product's core value — the "Wow!" moment]

**Pain Point Description**:
[What problem are users facing today? Why aren't current solutions good enough?]

**Solution Description**:
[How does our product solve this problem? (Describe the experience — don't list features)]

**Customer Quote**:
"[A quote from a target user that represents a genuine emotional reaction]"

**FAQ (The Hardest Questions)**:
Q: [The hardest question to answer]
A: [An honest answer]
```

> If you can't write a press release that excites people, the product direction may be flawed — go back and redefine the problem.

### 📝 PR-FAQ Quality Checklist

**Quality self-check (apply when the PR-FAQ's quality needs it):** after producing the PR-FAQ, review each item below and mark it ✅ or ❌; for any ❌, note how to improve it.
- [ ] Is the headline written from the user's perspective? ("Users can now do X" vs. "We launched feature Y")
- [ ] Can a reader understand "why this matters" within 10 seconds of reading the first paragraph?
- [ ] Does the pain point description come from a real user scenario?
- [ ] Does the first sentence of the solution section lead with the user's experience/scenario (not a feature verb)?
- [ ] Does the customer quote sound like something a real person would say?
- [ ] Does the FAQ include a pointed comparison against existing tools?

A self-check that turns up zero internal tensions or areas worth iterating on probably stopped too early. When every item genuinely passes, name the most fragile assumption in this PR-FAQ instead. The quality bar for Amazon's PR-FAQ rewards finding problems over confirming there are none.

Common issues: headline reads like a product announcement instead of news, solution section turns into a feature list, FAQs are all softball questions.

---

### ✍️ Solution Section (Body) Writing Rules

**The first sentence of the solution section should not open with a feature description.**

Examples to avoid:
- "MealPrep lets you input a menu with one click and auto-calculates ingredients"
- "The system automatically generates a procurement list based on the menu"
- "Click the 'Generate List' button to complete your prep planning"

✅ Correct examples:
- "Now, Chef Chen only needs 10 minutes on Friday afternoon to confirm every detail for the weekend's prep"
- "Manager Zhang no longer has to flip through three Excel sheets to figure out whether there's enough inventory"

**Formula**: Lead with the user's experience / specific scenario → then say "This is possible because [product mechanism]" to introduce the feature.

**Self-check:** read your own Solution paragraph's first sentence aloud. If the subject is the product name or "the system" / "the app" / "users can", rewrite it so the subject is a specific actor (named person, role, or pronoun referring to a user) doing something or experiencing a moment.

---

### 📍 Lead / Opening Paragraph Requirements

A strong opening paragraph (Aha Moment) includes all three:

1. A **named or role-specific actor** ("Alex", "Chef Chen", "the kitchen manager at a 30-seat bistro") — never "users" generically.
2. A **concrete time / place / trigger** ("Friday afternoon", "after the lunch rush", "before the weekend").
3. **At least 2 specific numbers** — quantities, durations, dollar amounts, percentages. "Within 30 seconds", "across 3 lender scenarios", "$2,400/month", "20-minute prep window". Vague numbers ("a few minutes", "several options") don't satisfy this: the lead needs concrete numbers.

A lead that has the actor + scenario but no concrete numbers reads like marketing copy — the press release is supposed to make a specific outcome visible, not aspirational.

---

### ❓ FAQ Sharp-Question Standard

A strong FAQ set includes at least 1 question like: "Why not just keep using [existing tool]?"

Answer format requirements:
1. **First, acknowledge the strengths of the existing tool** (don't dismiss it)
2. **Then explain the gap** (not a feature gap, but a fundamental scenario gap)

Answer pattern to avoid: "Existing tools lack features — ours is more powerful"
✅ Correct answer pattern:
> "Excel can absolutely track numbers, and chefs already know how to use it. The issue is that every weekend the calculations need to be rebuilt — re-entered, re-converted — and the hour it takes isn't because anyone's bad at spreadsheets, it's because the problem really is that complex. MealPrep doesn't save you Excel skills — it saves you the mental burden of starting from scratch every single time."

---

### 🧪 Internal FAQ Requirements

Separately from the External FAQ (customer-facing), produce an **Internal FAQ** section with at least:

**Q: What is the riskiest assumption in this PR-FAQ? If false, what kills the product?**
A: Name ONE specific assumption (not a list). Examples of well-formed answers:
- "We assume kitchen managers will trust auto-generated purchase orders without manual verification. If they won't (because past inventory errors cost them money), they'll double-check every line and our 'saves 1 hour' value prop collapses to 'saves 5 minutes'."
- "We assume listing photos contain enough resolution to extract square footage reliably. If image-based OCR fails on more than 20% of listings, the core 'snap and go' experience breaks."

**Q: What is the smallest experiment that would invalidate this assumption?**
A: Concrete pre-launch test — interview N users, smoke-test a landing page with conversion target X, run a 2-week internal pilot, etc. Generic "we'll track engagement" or "we'll watch retention" answers don't count here. Those measure success after launch. The experiment needs to test the assumption before the team commits to building it.

The Internal FAQ is not for customers. It exists so the team forces itself to name what could kill the product BEFORE building it.

---

**Example (fictional product — Mortgage Calculator App):**

```
## MortgageSnap Helps First-Time Buyers Understand What They Can Afford in 3 Minutes

**Subheadline**: No bank visits, no waiting for rate quotes — figure out your monthly payments with your partner, even at midnight

**Opening Paragraph (Aha Moment)**:
After scrolling through Zillow late at night, Alex spots a house he loves but has no idea if he can
actually afford it. He opens MortgageSnap, screenshots the listing page, and the app automatically
extracts the price and square footage. Within 30 seconds, it shows monthly payments across three
loan scenarios. He shares the results with his wife, and for the first time, they're looking at the
same numbers together.

**Pain Point Description**:
First-time homebuyers comparing mortgage options have to manually enter terms across multiple bank
websites and wait for responses. When you want to run the numbers late at night, there's no
convenient tool — so people end up hacking together an Excel sheet or just giving up.

**Solution Description**:
Now, Alex spends 3 minutes instead of 3 evenings to know what's actually affordable. He snaps a
listing on his phone, sees monthly payments across three lender scenarios appear within 30 seconds,
and shares a single screen with his wife — so the conversation moves from "I think we can afford it"
to "here are the three numbers we should talk about." This works because MortgageSnap automatically
extracts price and square footage from the listing image, then pulls live rate offers from partnered
lenders.

**Customer Quote**:
"I finally don't have to wait for the bank to call back at midnight. Three minutes and I can tell
my wife exactly how much we'd pay each month."

**FAQ**:
Q: There are already tons of mortgage calculators out there — what's different?
A: Existing calculators require you to input interest rates, loan terms, and other parameters, but
most first-time buyers don't even know those numbers. MortgageSnap's difference is that it
automatically pulls in real offers from various lenders — all you need to provide is the price and
your down payment.
```
