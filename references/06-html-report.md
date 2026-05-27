# HTML Product Planning Report Output

Triggered when the user says "produce a report" or confirms the last stage content is correct.

## Design Specifications

Use a **modern design style** — a single HTML file (CSS and JS fully inlined), ensuring it's readable offline.

**Overall Style:**
- Gradient background Hero section (with mode, audience, date labels)
- Card-based layout (rounded corners + shadows), each section like an independent information card
- Clear typography hierarchy and comfortable reading spacing
- Responsive design, smooth reading on mobile

**Color Scheme:**
- Primary: Deep blue `#1a1a2e` → `#16213e` → `#0f3460`
- Accent: `#e94560` or `#533483`
- Content area background: `#f8f9fa`, cards: white with `box-shadow`

**Font:** Load Inter from Google Fonts CDN first, fall back to system fonts:
```css
/* In <head> */
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">

/* In CSS */
font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
```
> This is the only permitted external CDN dependency. If Google Fonts is unavailable, the page will still render correctly.

## Page Structure (Dynamically rendered based on completed stages)

```
┌──────────────────────────────────────────────────────────────┐
│  Hero Section (Product name, one-liner, mode, audience, date)│
├──────────────────────────────────────────────────────────────┤
│  Table of Contents Navigation (Sticky, only shows completed) │
├──────────────────────────────────────────────────────────────┤
│  🧭 Strategy Section (if completed)                          │
│     ├─ Strategy Blocks hierarchy diagram                     │
│     ├─ Rumelt's Kernel of Good Strategy (Diagnosis/Policy/   │
│     │  Actions)                                              │
│     └─ Shreyas' Three Levels of Product Work                 │
│  ✅ Opportunity Check Section (if completed)                  │
│  🔍 Discovery Section (if completed)                         │
│     ├─ Persona Table (card-style table)                      │
│     ├─ Persona Cards (one per persona)                       │
│     ├─ JTBD Analysis Table (four types)                      │
│     ├─ Opportunity Solution Tree (visual tree)               │
│     └─ User Journey Map (overview + accordion detail)        │
│  🎯 Define Section (if completed)                            │
│     ├─ Pain Point Summary Table                              │
│     ├─ April Dunford Positioning Framework Card              │
│     ├─ HMW Question Cards (with JTBD type tags)             │
│     └─ Opportunity Assessment Table (opportunity cost view)  │
│  💡 Develop Section (if completed)                           │
│     ├─ PR-FAQ Card (simulated press release format)          │
│     ├─ Solution Ideation (three-column parallel cards)       │
│     ├─ Pre-mortem Risk Table (color-coded High/Med risk)     │
│     ├─ GEM Matrix + Impact/Effort Quadrant Chart             │
│     ├─ RICE Prioritization Table (if completed)              │
│     ├─ User Story Table (if completed)                       │
│     └─ MVP Scope (three-column cards + Not Doing List)       │
│  🚀 Deliver Section (if completed)                           │
│     ├─ Aha Moment Definition Card (prominently displayed)    │
│     ├─ North Star Metric Card                                │
│     ├─ Three-Layer Signal Metrics Table                      │
│     ├─ PMF Level Assessment (four-level visual + current     │
│     │  position marker)                                      │
│     ├─ GTM Strategy (channel selection + first 100 users     │
│     │  plan, if completed)                                   │
│     ├─ Business Model & Pricing (revenue model + pricing     │
│     │  strategy, if completed)                               │
│     ├─ Hypothesis Validation Plan Table (if completed)       │
│     └─ Product Spec Summary (three-section structure:        │
│        Decision Summary / Execution Boundaries / Deep Ref)   │
│  ⭐ Best Entry Point Analysis (full logic chain visual)       │
├──────────────────────────────────────────────────────────────┤
│  Footer: Output date + mode + framework attribution          │
└──────────────────────────────────────────────────────────────┘
```

## Section Design Details

**Table Styling:** Zebra stripes, dark header, rounded corners, hover highlight

**Persona Cards:** One card per Persona, pain points with red left border, JTBD emphasized with blue/purple color blocks

**Opportunity Solution Tree:** Use CSS or lightweight SVG to draw the tree structure, clearly showing the Goal → Opportunity → Solution hierarchy

**PMF Level Chart:** Use a progress bar or step diagram showing four levels, marking the user's current position

**PR-FAQ Card:** Simulated press release format with headline, subtitle, lead paragraph — visually resembling a real document

**Pre-mortem Risk Table:** High-risk items in red alert, medium-risk in yellow

**Best Entry Point Logic Chain:** Visualize the full reasoning chain, each node as a small card, connected by arrows

## Interactive Effects

- `scroll-behavior: smooth` — Smooth scrolling on TOC click
- Intersection Observer — Highlight current section in TOC while scrolling
- Card hover micro-lift (`transform: translateY(-2px)` + `transition`)
- Accordion expand/collapse (User Journey Map stages, `<details>/<summary>`)
- `@media print` — Hide interactive elements when printing, ensure tables aren't truncated

## Important Notes

- All CSS and JS inlined in HTML — no external dependencies except Google Fonts CDN for Inter
- If a stage was not completed, don't render an empty section — just skip it
- The Hero section displays the "Mode" and "Audience" so readers immediately understand the document's context
- The page can be very long — TOC navigation is critical for quick jumping

## Framework Attribution & Further Reading (in footer)

| Thinker | Key Contribution | Source |
|---------|-----------------|--------|
| Teresa Torres | Continuous Discovery, Opportunity Solution Tree | Lenny's Podcast + *Continuous Discovery Habits* |
| Shreyas Doshi | LNO Framework, Pre-mortem, Three Levels of Product Work, Opportunity Cost Thinking | Lenny's Podcast Ep.3 |
| Gibson Biddle | DHM Model, GEM Prioritization | Lenny's Podcast |
| April Dunford | Positioning Framework | Lenny's Podcast + *Obviously Awesome* |
| Todd Jackson | Four-Level PMF Framework, Four P's | Lenny's Podcast (First Round Capital) |
| Richard Rumelt | Good Strategy / Bad Strategy, Kernel of Good Strategy | Lenny's Podcast + *Good Strategy Bad Strategy* |
| Marty Cagan | Empowered Teams, Product Discovery | Lenny's Podcast + *Inspired*, *Empowered* |
| Chandra Janakiraman | Strategy Blocks | Lenny's Newsletter (Headspace / Meta) |
| Clayton Christensen | Jobs to Be Done | *Competing Against Luck* |
| Amazon | Working Backwards / PR-FAQ | *Working Backwards* |
| Sean Ellis | Sean Ellis Score, ICE Scoring | *Hacking Growth* |
| Lenny Rachitsky | Shape / Ship / Synchronize, North Star Thinking | Lenny's Newsletter + Podcast |
