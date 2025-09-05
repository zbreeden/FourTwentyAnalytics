##FourTwenty Analytics — Modular Dashboard Sandbox

*My portfolio is structured as a modular sandbox I call FourTwenty Analytics. 
*Each repository is a model within an orbit — 🚀 The Launch, 🫀 The Archive, 📡 The Signal, 🏦 The Bank, and others — that together 
simulate the systems a data analyst navigates in the real world. 
*This lets me practice end-to-end craft: framing problems in YAML specs, validating with QA rules, pulsing with daily signals, 
and archiving immutable evidence. 
*It’s not just code; it’s a living ecosystem where I sharpen analysis, consistency, and storytelling — the same skills I bring into a role.
*Scrollkeeper Note --> My suns can wander all they want as long as 4/20 is seeded.

Scaffolding -
index.html:  portfolio website.
readme.md:  this scroll meant to be a running broadcasting of how FourTwenty Analytics is built.
assets/:  a set of images specific to FourTwenty Analytics.
seeds/: a collection of data seeds meant to create a living system of modules.

--> seeds/glossary.yml <--

key: Stable, machine-friendly identifier in snake_case. Must be unique and should never change (other files may reference it).
term: Human-readable label (usually Title Case). Safe to tweak for wording, since references should point to key, not term.
definition: Plain-language explanation for humans. Use > (folded block) so it reads as one paragraph. Start with a crisp one-sentence summary; add a second line for nuance if needed.
examples: Short, real uses (1–3 items). Each item is a concise string that shows the term in context—an action, artifact, or sentence fragment.
see_also: List of related keys (not terms). Helps cross-link concepts within your docs.

- key: your_snake_case_key
  term: "Your Term"
  definition: >
    One-sentence summary.
    Optional second sentence with context or scope.
  examples:
    - "Short example showing use"
  see_also: ["related_key_1", "related_key_2"]

- key: portfolio
  term: "Portfolio"
  definition: >
    Content intended for external viewing (landing pages, demos, docs).
    Aggregates public entry points across modules.
  examples:
    - "Launch Model GitHub Pages site"
  see_also: ["launch", "entry"]

--> seeds/tags.yml <--

key: Stable, machine-friendly identifier in snake_case. Must be unique and should not change (dashboards and docs may reference it).
label: Human-readable display name (Title Case). Safe to tweak without breaking references (consumers should point to key).
description: Plain-language summary for humans. Use > (folded block) so it reads as one paragraph. Start with a crisp one-sentence summary; add an optional second line for nuance.
kind: Category for grouping/filters. Choose one from the allowed set:
audience, navigation, discipline, standard, framework, role, analytics_type, repository, pipeline, streaming, platform, knowledge, technique, process, language, format, credential, organization, capability, governance, requirements, practice, planning, source, concept, skills
gloss_ref: The key of a related entry in seeds/glossary.yml. Validates cross-linking and keeps tags fewer than glossary terms.
deprecated: Boolean flag. Set to true to retire a tag without breaking older artifacts; prefer introducing a replacement tag and updating references over time.

- key: your_snake_case_tag
  label: "Your Label"
  description: >
    One-sentence summary of how this tag is used across modules or docs.
    Optional second sentence with scope or examples of where it applies.
  kind: analytics_type
  gloss_ref: your_glossary_key
  deprecated: false

- key: portfolio
  label: "Portfolio"
  description: >
    Public-facing entry artifacts across the constellation.
  kind: audience
  gloss_ref: portfolio
  deprecated: false

Notes: Keep tags.yml intentionally smaller than glossary.yml; use it as the cross-module “integration surface.” When in doubt, put specifics in the glossary and map them to a broader tag via gloss_ref.

<!-- SIGNAL:START
id: 2025-09-04-hub-learns-workflows
ts_utc: 2025-09-04T20:00:00Z
title: "Learned GitHub Workflows — hub now syncs seeds"
summary: >
  I learned GitHub Actions and wired a hub → constellation seed sync.
  Editing anything under `seeds/**` in the hub now opens PRs across module repos
  with updated seeds. The Archive pulses read the merged changes, and The Signal
  can harvest these broadcasts into a feed.
tags: [learning, github-actions, workflows, seeds, sync, ci, hub]
links:
  - label: "Sync Seeds workflow (hub)"
    url: "https://github.com/zbreeden/FourTwentyAnalytics/actions/workflows/sync_seeds.yml"
  - label: "seedset.yml"
    url: "https://github.com/zbreeden/FourTwentyAnalytics/blob/main/seeds/seedset.yml"
  - label: "registry.yml"
    url: "https://github.com/zbreeden/FourTwentyAnalytics/blob/main/seeds/registry.yml"
  - label: "sync_seeds.py"
    url: "https://github.com/zbreeden/FourTwentyAnalytics/blob/main/scripts/sync_seeds.py"
SIGNAL:END -->

## License

MIT — See `LICENSE`. Use freely; please don’t send PII to the sandbox.
