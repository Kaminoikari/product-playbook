---
name: pre-mortem
description: Use when you need to surface how a product, feature, or plan could fail before committing to it, especially before a go/no-go decision. Triggers on "pre-mortem", "what could go wrong", "failure modes", "risks", "how might this fail", and the same intent in any language.
---

# Pre-mortem

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce pre-mortem output, contribute the framework tag `Pre-mortem` to the meta-skill's provenance line.

## Framework

<!-- adapted from agents/pre-mortem-runner.md, the pre-mortem framework engine; the "at least one security scenario" quality check is folded in from references/04b-solutions.md §3.3 -->

### Premise

Apply this lens by assuming the product, feature, or plan has already shipped, run for twelve months, and failed catastrophically. Then work backwards to enumerate every plausible reason why. The technique originates with Gary Klein and was popularized in product management by Shreyas Doshi.

Asking "what risks do we face" produces sanitized hedging. Declaring the failure as fact and asking "what happened" gives permission to imagine the concrete failure modes that planning optimism normally suppresses.

### Deliverables

Produce:
1. **15+ failure scenarios** spanning all five categories below.
2. For each scenario, a **leading indicator** that warns the team early.
3. **Likelihood and impact** ratings for prioritization.
4. The **top 3 failure modes** to design countermeasures against now.
5. **Pre-launch experiments** that invalidate the highest-risk scenarios cheaply.

### Operating principles

**Diversity over depth on the first pass.** Fifteen scenarios in one category and none in the others is a pre-mortem that missed where the real failure lives. Cover all five categories before deepening any single one.

**Concrete failure stories, not abstract risks.**
- Weak: "Adoption may be low."
- Strong: "Six months post-launch, weekly active users plateau at 8% of registered users because the core JTBD only fires once per quarter for the target persona, so the product never becomes a habit."

A good failure story combines a metric, a timing, a quantity, and a causal mechanism. A weak one is a hedge.

**Leading indicators must move before the failure consummates.**
- Lagging, and therefore too late to act on: "User retention drops."
- Leading, and therefore useful: "In the first 30 days post-launch, fewer than 20% of new users complete the Aha Moment action within 7 days, and the Sean Ellis score on a sample of 50 users is below 30%."

**Architecture-grounded for existing systems.** When the plan extends an existing codebase and architecture context is available (code, schema, CLAUDE.md), ground at least 3 scenarios in the observed technical reality; cite the specific file or fact. Example: "The current monolithic auth layer cannot support per-tenant rate limits, so the planned multi-tenancy feature will create a noisy-neighbor outage within 4 weeks of launch."

**Use WebSearch when domain matters.** Regulated industries (fintech, healthcare, mobility, insurance) carry industry-specific failure patterns; search for prior post-mortems in that industry and cite sources.

### Five failure categories

Cover at least 2 concrete scenarios per category. A clause mentioned inside another category's story does not count toward that other category's coverage; each scenario needs its own story. `External` is the category most often dropped and is non-optional.

**A. Product / UX.** The job is not delivered, or delivered non-habitually:
- Aha Moment too far from first use
- Core flow has too many steps for the target context
- Empty state or cold start makes the product useless until a threshold is reached
- Edge cases dominate support load (10% of cases consume 80% of it)
- Solves a once-per-quarter need but is priced for once-per-week use

**B. Market / Demand.** The job exists, but the market shape was misjudged:
- The segment with the job is smaller than estimated
- Users solve the job well enough with existing tools; switching cost exceeds new-value delta
- B2B: the buyer doesn't feel the user's pain, because who pays is not who benefits
- The job is episodic, so the product can't build a retention loop
- An adjacent player adds the feature for free and standalone value collapses

**C. Team / Execution.** The strategy is reasonable, but the team can't ship it:
- Engineering velocity drops from accumulated MVP tech debt
- Founder or PM bandwidth is the bottleneck, with no delegated decision rights
- Hiring lags adoption, and support quality collapses
- Cross-functional alignment breaks: eng, design, and GTM build to different mental models
- Key-person dependency: one engineer or designer holds critical context and leaves

**D. Operational / Infrastructure.** The product works in demos and breaks at scale:
- Cost-per-user crosses lifetime value before retention flattens
- Latency or reliability degrades as users grow, accelerating churn before product-market fit
- An integration partner changes terms, deprecates an endpoint, or has outages
- Compliance surfaces post-launch (PCI-DSS, GDPR, data residency)
- Data quality decays because real data is messier than test data

Quality check, must consider at least one security scenario for any product handling user data: user data breach (database intrusion, unauthorized API access), mass account takeover (brute force, credential stuffing), API abuse (no rate limiting, mass scraping), XSS/CSRF attacks harming users, and accidental exposure of sensitive data (secrets in version control, passwords in logs). If the product genuinely has no authentication or sensitive-data surface, mark this scenario "not applicable" and state why in one sentence.

**E. External / Environment.** Outside the team's control but foreseeable:
- Platform policy change (App Store, Google Play, browser cookies, OS API)
- A competitor with deeper pockets floods customer acquisition cost
- A macro shift (rates, recession, regional conflict) collapses the budget category
- A new AI capability commoditizes the core value proposition
- A negative press event (data breach, viral complaint, regulatory action) destroys trust before the team earns forgiveness margin
