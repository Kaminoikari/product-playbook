---
name: success-metrics
description: Use when the user needs to define how success is measured: a North Star, supporting signals, and the activation moment. Triggers on "North Star metric", "success metrics", "signals", "aha moment", "activation", "Sean Ellis", and the same intent in any language.
---

# Success Metrics

Detect the user's language and reply in it; the framework below is authored in English.

**Provenance:** when you produce success-metrics output, contribute the framework tags `North Star`, `Aha Moment`, and `Sean Ellis` to the meta-skill's provenance line (`— Frameworks: … · North Star · Aha Moment · Sean Ellis · …`).

## Framework

<!-- migrated from references/05a-northstar-aha.md lines 25-93 (§4.2 Success Metrics Framework + §4.4 Aha Moment Design); §4.1 is out of scope here, it belongs to the strategy-kernel lens -->

## 4.2 Success Metrics Framework (North Star + Three-Layer Signals)

A North Star metric must satisfy:
- Reflects the real value users receive (not a vanity metric)
- Can grow continuously (doesn't hit a natural ceiling)
- Aligns the entire team around a single objective

```
| Company | North Star Metric | Why This Metric |
|---------|-------------------|-----------------|
| Airbnb | Nights booked | Represents value delivered to both hosts and guests |
| Spotify | Monthly listening hours | Represents users genuinely using and enjoying music |
| Facebook | DAU / MAU ratio | Represents habitual return visits |
| Slack | Messages sent per week | Represents teams genuinely collaborating |
| Salesforce | Active customer ACV (Annual Contract Value) | Represents customers continuously deriving business value (B2B) |
```

**Your North Star Metric:**
```
North Star Metric: [A single number representing the core value created for users and the product]
Definition: [Precise calculation method]
Why this metric: [Explain why it represents real user value beyond a business outcome]
```

### 📝 North Star Quality Checklist
- ✅ Does it reflect the value users receive? (Revenue and DAU fail this test)
- ✅ Can it grow continuously? (Doesn't hit a natural ceiling)
- ✅ Does everyone on the team know what to do when they see this metric?
- ✅ Can it be gamed? (If yes, guardrail metrics are needed)
- ✅ B2B products: Does it reflect value at the organizational level, beyond individual users?

Common pitfalls worth double-checking: using revenue as the North Star (revenue is a lagging business outcome; a North Star metric should track the upstream user behavior that creates that value), or landing on a metric too composite to act on.

**Three-Layer Signal System (the layers build on each other):**

```
| Layer | Metric Type | Definition | B2C Target | B2B Target |
|---|---|---|---|---|
| Layer 1 (Prerequisite) | Core Action Success Rate | Did the user complete the product's core action? | 30–40%+ | 60–80%+ (users are more motivated) |
| Layer 2 (Value Proxy) | D14 / D28 Retention Rate | Do users keep coming back? | Consumer products 15–20%+ | Logo retention 90%+; Net Revenue Retention 100%+ |
| Layer 3 (Passion Signal) | Sean Ellis Score | "If you could no longer use this product, how disappointed would you be?" | 40%+ answer "very disappointed" | 40%+ answer "very disappointed" |
| Guardrail Metrics | Prevent over-optimization | Ensure other important dimensions aren't harmed | Depends on context | Depends on context |
```

Note: Layer 1 is the prerequisite for Layer 2. If the core action success rate is very low, retention data is meaningless because users never had the chance to experience the product's value.

## 4.4 Aha Moment Design

```
Aha Moment Definition:
When a user completes [specific behavior], they have experienced this product's core value.
Goal: Get users to this moment within [X minutes / X steps] of entering the product.

Aha Moment Reach Rate: [target %]
Current Barriers: [What prevents users from reaching the Aha Moment faster?]
Improvement Plan: [How to remove the barriers?]
```

**Examples:**
| Product | Aha Moment | Time Target |
|---------|-----------|-------------|
| Slack | Team sends its 2,000th message | First two weeks |
| Dropbox | First file synced to a second device | Within 10 minutes of first use |
| Zoom | First one-click join with smooth video | First use |

### 📝 Aha Moment Quality Checklist
- ✅ Is it a specific, trackable behavior? (Not "feels like the product is useful")
- ✅ Is it directly tied to the JTBD's functional job?
- ✅ Is the time target reasonable? (B2C should be within first use; B2B may be within the trial period)
- ✅ Can onboarding be designed to help users reach it faster?
