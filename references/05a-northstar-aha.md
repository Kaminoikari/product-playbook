# Phase 4: Deliver — North Star + Aha Moment

## 4.1 Marty Cagan's Empowered Teams Principles

**Applicable when: high completeness / deliverable audience is leadership or cross-functional teams**

> 4.1 Empowered Teams is only shown when the deliverable audience is leadership or cross-functional teams; otherwise skip.

```
| Dimension | Feature Team (Avoid) | Empowered Team (Goal) |
|-----------|---------------------|----------------------|
| Assigned | Feature list (Output) | Problem to solve (Outcome) |
| Success defined as | Delivering features on time | Achieving user and business metrics |
| PM's role | Requirements gatherer and project manager | Problem explorer and solution validator |
| Engineers' role | Execute specs | Participate in problem exploration and solution design |
```

> "True product discovery is done **together** with engineers and designers, not by the PM alone handing off completed work." — Marty Cagan

**Lenny's Three PM Responsibilities:**
- **Shape**: Synthesize user insights, data, and market intelligence to decide what to build
- **Ship**: Ensure a high-quality product launches on time, with no surprises
- **Synchronize**: Keep all stakeholders aligned on vision, strategy, goals, and roadmap

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
Why this metric: [Explain why it represents real user value, not just a business outcome]
```

### 📝 North Star Quality Checklist
- ✅ Does it reflect the value users receive? (Not revenue, not DAU)
- ✅ Can it grow continuously? (Doesn't hit a natural ceiling)
- ✅ Does everyone on the team know what to do when they see this metric?
- ✅ Can it be gamed? (If yes, guardrail metrics are needed)
- ✅ B2B products: Does it reflect value at the organizational level, not just individual users?
- ❌ Common issues: using revenue as the North Star (revenue is an outcome, not a driver), metric is too composite to act on

**Three-Layer Signal System (must be achieved in order):**

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
