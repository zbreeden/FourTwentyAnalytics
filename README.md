 FourTwenty Analytics — Modular Dashboard Sandbox

A public, hands-on sandbox for sharpening **data analytics** skills through modular dashboards, semantic event tracking, and iterative optimization. This repo is the hub for my FourTwenty models (Firm, Story, Player, Signal, Catalyst, Anchor, Orbiter, Gambler, Grower, Evaluator) and a UX telemetry playground that powers real instrumentation and analysis.

> TL;DR: Clone, run the local playground, instrument a few events, and analyze them. The modules give you a repeatable way to practice BI, SQL, Python, and GA4+GTM.

---

## Goals

- Build and demo **production-like analytics habits**: event design, data modeling, BI visuals, and iteration.
- Keep everything **sandboxed**, reproducible, and portfolio‑ready.
- Show how modules coordinate via a **semantic telemetry layer** (GTM → GA4 → BigQuery/Power BI).

---

## Modules (high level)

- **Firm Model** – strategic knowledge base & governance.
- **Story Model** – narrative sequencing and context.
- **Player Model** – decision & outcome simulation.
- **Signal Model** – semantic trigger layer (glossary-driven events).
- **Catalyst Model** – transformation & experimentation.
- **Anchor Model** – grounding framework for repeatable metrics.
- **Orbiter Model** – auxiliary/adjacent analyses.
- **Gambler Model** – risk, odds, and lift framing.
- **Grower Model** – optimization & maturity tracking.
- **Evaluator Model** - assessment & support tagging.

Each model has a one‑pager and artifacts (screenshots/GIFs, exports) to keep it concrete.

---

## Quick Start (local)

```bash
# 1) Clone the repo
git clone https://github.com/<your-username>/FourTwentyAnalytics.git
cd FourTwentyAnalytics

# 2) Run the playground (serves /playground at http://localhost:5500)
python3 -m http.server 5500
# or: ruby -run -e httpd . -p 5500
# or: npx http-server -p 5500
```

Open http://localhost:5500/playground/ux_playground.html in Chrome.

### Practice flow
1. In **Google Tag Manager (GTM)**, create a Web container and a **GA4 Configuration** tag for your GA4 Measurement ID.
2. Replace `GTM-XXXXXXX` in `/playground/ux_playground.html` with your container ID.
3. Click **Preview** in GTM, attach to your `localhost` URL, and exercise the page: CTA click, outbound link, file download, form submit, site search, video.
4. In **GA4 → DebugView**, verify events arrive.
5. Export data to **BigQuery** (or pull via GA4 API) and analyze in **Power BI** / **Python**.

> All example events are **PII‑free** and intended for a sandbox property only.

---

## Skills You’ll Exercise

- **BI & Storytelling:** Power BI (models, DAX, bookmarks), clear visuals & documentation.
- **Data Engineering Lite:** event schema, naming conventions, custom dimensions/metrics, exports.
- **Measurement & QA:** GTM preview, GA4 DebugView, reproducible test pages, no double‑install.
- **Experimentation Thinking:** define success metrics, guardrails, and basic test notation.
- **Python/SQL:** scoring, transformation, and checks before visualization.

---

## Repo Structure

```
FourTwentyAnalytics/
├─ playground/             # Local demo pages & sample assets
│  ├─ ux_playground.html   # Rich interactions (CTA, links, form, search, video)
│  ├─ gtm_starter.html     # Minimal base-install page
│  └─ sample.csv           # File download for tagging practice
├─ gtm/                    # Export your GTM container JSONs here
├─ ga4/
│  └─ custom-dimensions-template.csv  # Track the GA4 fields you register
├─ powerbi/                # PBIX or PDF/screenshots
├─ artifacts/              # One-pagers, Tag Assistant/DebugView, GIFs
└─ README.md
```

---

## One‑Pagers (what’s included)

- **The Signal — Semantic Trigger Module:** glossary‑aligned events (`signal_initiated`, params like `semantic_tag`, `chamber`, `action`).
- **The Grower — Optimization & Maturity Model:** behavioral signals to compute a maturity score and track progression.

> See `/artifacts` for PDFs/MD summaries, plus screenshots that prove the wiring (Tag Assistant, DebugView).

---

## Roadmap

- [ ] Publish a **GitHub Pages** site that links to modules and the playground.
- [ ] Add **Power BI** sample PBIX with maturity scoring visuals.
- [ ] Provide **BigQuery schema** + Python notebook for lightweight ETL.
- [ ] Add **A/B flags** (`experiment_view` / `experiment_convert`) to the playground.
- [ ] Ship a consistent **naming convention** & lint checklist for GTM/GA4.

---

## License

MIT — See `LICENSE`. Use freely; please don’t send PII to the sandbox.
