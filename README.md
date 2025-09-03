##FourTwenty Analytics — Modular Dashboard Sandbox

*My portfolio is structured as a modular sandbox I call FourTwenty Analytics. 
*Each repository is a model within an orbit — 🚀 The Launch, 🫀 The Archive, 📡 The Signal, 🏦 The Bank, and others — that together 
simulate the systems a data analyst navigates in the real world. 
*This lets me practice end-to-end craft: framing problems in YAML specs, validating with QA rules, pulsing with daily signals, 
and archiving immutable evidence. 
*It’s not just code; it’s a living ecosystem where I sharpen analysis, consistency, and storytelling — the same skills I bring into a role.

Scaffolding -
index.html:  portfolio website.
readme.md:  this scroll meant to be a running broadcasting of how FourTwenty Analytics is built.
assets/:  a set of images specific to FourTwenty Analytics.
seeds/: a collection of data seeds meant to create a living system of modules.

--> seed/glossary.yml <--

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

## License

MIT — See `LICENSE`. Use freely; please don’t send PII to the sandbox.
