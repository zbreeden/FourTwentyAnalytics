# FourTwenty Analytics — Modular Dashboard Sandbox

- My portfolio is structured as a modular sandbox I call FourTwenty Analytics.
- Each repository is a model within an orbit — 🚀 The Launch, 🫀 The Archive, 📡 The Signal, 🏦 The Bank, and others — that together simulate the systems a data analyst navigates in the real world.
- This lets me practice end-to-end craft: framing problems in YAML specs, validating with QA rules, pulsing with daily signals, and archiving immutable evidence.
- It's not just code; it's a living ecosystem where I sharpen analysis, consistency, and storytelling — the same skills I bring into a role.
- **Scrollkeeper Note** → My suns can wander all they want as long as 4/20 is seeded.

## Scaffolding

### Seeding

- `index.html`: portfolio website
- `README.md`: this scroll meant to be a running broadcast of how FourTwenty Analytics is built
- `hub_pat.md`: The constellation API token; while this is generally a secret, this portfolio is public facing, so there is no PII
- `assets/`: a set of images specific to FourTwenty Analytics
- `schema/`: even living seeds need machine genetics; these .yml files define the seeds in machine language
- `seeds/`: a collection of data seeds meant to create a living system of modules; these seeds all maintain home repo genetics as the constellation grows
- `signals/`: a collection of constellation signals picked up by The Signal for broadcasting portfolio development
- `scripts/`: a collection of Python scripts intended to facilitate constellation processes
- `scrubs/`: a collection of QA scripts meant to periodically clean constellation data
- `.github/workflows/validate_seeds.yml`: validates seed structures against schemas

### Developmental Funnels

- `scrolls/`: A collection of creative writing scrolls meant for ideation

## Orbitals

### ☀️ Elemental System Creed

> The Elemental System is the epicenter of the constellation — the force that keeps every star aligned.

- 🔘 **The Barycenter** → presents **gravity**
  - All data seeds emanate from the hub

> This center exists so that all other stars exist.

### 🪐 Core System Creed

> The Core System consists of the stars that support metaphorical life for the constellation — the foundation that keeps every other orbit aligned.
> Each star has a distinct mission:

- 🫀 **The Archive** → promotes **longevity**
  - Breathes life into the constellation by maintaining memory, seeds, and history. Think master of the scrolls.

- 📡 **The Signal** → promotes **opportunity**
  - Acts as the nervous system — scanning outward and broadcasting inward to find value. Think curiosity.

- 🚀 **The Launch** → promotes **consistency**
  - Ensures new suns are seeded with repeatable, reliable foundations. Think genetic normalization.

- 🛡️ **The Protector** → promotes **integrity**
  - Safeguards the constellation by hardening workflows, monitoring health, and shortening recovery time. Think fortification and adaptability.

- ✨ **The Developer** → promotes **ideation**
  - Sparks new creations by shaping raw concepts into working modules, tools, and systems. Think genesis and invention.

> These Core stars work together so the constellation remains consistent, long-lived, opportunistic, and trustworthy.

### 📈 Delivery & Insight Creed

> The Delivery & Insight system consists of stars that translate data into meaning and action — the storytellers of the constellation.
> Each system has a distinct mission:

- 🎨 **The Visualizer** → promotes **clarity**
  - Paints data into patterns stakeholders can immediately grasp. Think canvas and gallery.

- ⚡ **The Catalyst** → promotes **transformation**
  - Accelerates change by turning insights into operational improvements. Think spark that ignites.

- 🏦 **The Bank** → promotes **stewardship**
  - Safeguards outputs and provides dashboards of record. Think vault of truth.

- 🧠 **The Evaluator** → promotes **judgment**
  - Weighs outcomes, models, and assumptions for sound decision-making. Think wisdom keeper.

- 📖 **The Story** → promotes **narrative**
  - Threads insights into human language that compels and convinces. Think bard of the constellation.

> These Delivery & Insight stars work together so the constellation always communicates clearly, acts decisively, and preserves trusted outcomes.

### 🧪 Growth & Experiment Creed

> The Growth & Experiment system consists of stars that push boundaries — where the constellation tests, plays, and evolves.
> Each system has a distinct mission:

- 🌱 **The Grower** → promotes **cultivation**
  - Nurtures seeds and modules to maturity. Think gardener's hand.

- 🎮 **The Player** → promotes **immersion**
  - Creates interactive spaces for experimentation. Think simulation and play.

- 🎲 **The Gambler** → promotes **risk & probability**
  - Models chance, odds, and uncertainty to explore outcomes. Think dice on the table.

- 🧭 **The Trainer** → promotes **discipline**
  - Sharpens skills and tracks progress across learning journeys. Think compass for growth.

- 💪 **The Coach** → promotes **resilience**
  - Builds habits, routines, and accountability. Think steady motivator.

> These Growth & Experiment stars work together so the constellation continuously learns, adapts, and expands its horizons.

### 🧩 Ancillary Operations Creed

> The Ancillary Operations system consists of stars that provide structure and support — the quiet strength beneath the constellation.
> Each system has a distinct mission:

- 🛰️ **The Orbiter** → promotes **perspective**
  - Circles the constellation, observing from distance and relaying balance. Think satellite eye.

- ⚓ **The Anchor** → promotes **stability**
  - Grounds the constellation when drift threatens alignment. Think ballast in the deep.

- 🏢 **The Firm** → promotes **governance**
  - Establishes rules, policies, and accountability. Think law of the land.

- 🪞 **The Mirror** → promotes **inner awareness**
  - Reflects strengths and weaknesses to guide improvement. Think honest reflection.

- 💰 **The Accountant** → promotes **fiscal responsibility**
  - Tracks resources, costs, and returns. Think ledger of sustainability.

> These Ancillary Operation stars work together so the constellation remains stable, governed, and sustainable across every orbit.

## Schemas

### schema/glossary.schema.yml

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: "glossary.yml schema"
type: array
description: "An array of glossary entry objects."
minItems: 1

items:
  type: object
  additionalProperties: false
  required: [key, term, definition]
  properties:
    key:
      type: string
      pattern: "^[a-z0-9_]+$"
      description: "Stable snake_case identifier"
    term:
      type: string
      minLength: 1
      description: "Human-readable label (usually Title Case)"
    definition:
      type: string
      minLength: 1
      description: "Plain-language explanation. Folded (>) YAML is fine."
    examples:
      type: array
      description: "Short, real uses (1–3 items)"
      items:
        type: string
        minLength: 1
    see_also:
      type: array
      description: "Related keys for cross-linking"
      items:
        type: string
        pattern: "^[a-z0-9_]+$"
```

### schema/tags.schema.yml

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: "tags seed"
type: array
items:
  type: object
  additionalProperties: false
  required: [key, label, description, kind, gloss_ref, deprecated]
  properties:
    key:
      type: string
      pattern: "^[a-z0-9_]+$"
      description: "Stable snake_case key"
    label:
      type: string
      minLength: 1
    description:
      type: string
      minLength: 1
    kind:
      type: string
      enum: ["analytics_type","audience","capability","concept","credential","discipline","format","framework","governance","knowledge","language","nav","navigation","organization","pipeline","planning","platform","practice","process","quality","repository","requirements","role","skills","source","standard","streaming","technique","module","topic","kpi","status","orbit","tech"]
    gloss_ref:
      type: string
      pattern: "^[a-z0-9_]+$"
    deprecated:
      type: boolean
```

### schema/orbits.schema.yml

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: "orbits.yml schema"
type: array
items:
  type: object
  additionalProperties: false
  required: [id, label, emoji, order]
  properties:
    id:
      type: string
      pattern: "^[a-z0-9_]+$"
    label:
      type: string
      minLength: 1
    emoji:
      type: string
      minLength: 1
    order:
      type: integer
      minimum: 0
    meaning:
      type: string
      description: "Purpose and high-level description of the orbital system"
    scope:
      type: array
      description: "Specific responsibilities and boundaries"
      items:
        type: string
        minLength: 1
    includes:
      type: array
      description: "Repositories or components within this orbital system"
      items:
        type: object
        properties:
          repo:
            type: string
            minLength: 1
        required: [repo]
    kpis:
      type: array
      description: "Key performance indicators for measuring orbital health"
      items:
        type: string
        minLength: 1
    policies:
      type: array
      description: "Governance rules and operational guidelines"
      items:
        type: string
        minLength: 1
    see_also:
      type: array
      description: "Related orbital systems for cross-reference"
      items:
        type: string
        pattern: "^[a-z0-9_-]+$"
```

### schema/emoji_palette.schema.yml

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: "emoji_palette.yml schema"
type: object
additionalProperties: false

# require at least status_icons; allow other icon groups as optional
required: [status_icons]
properties:
  status_icons:
    $ref: "#/$defs/iconMap"
  orbit_icons:
    $ref: "#/$defs/iconMap"
  module_icons:
    $ref: "#/$defs/iconMap"
  tech_icons:
    $ref: "#/$defs/iconMap"

$defs:
  # Generic map of snake_case keys -> emoji (string).
  # We don't regex-match emoji here because cross-platform emoji regex is brittle;
  # validators can enforce stricter checks separately if desired.
  iconMap:
    type: object
    minProperties: 1
    additionalProperties: false
    patternProperties:
      "^[a-z0-9_]+$":
        type: string
        minLength: 1
```

### schema/statuses.schema.yml

```yaml
$schema: "https://json-schema.org/draft/2020-12/schema"
title: "statuses seed"
type: array
items:
  type: object
  additionalProperties: false
  required: [id, label, emoji, order, meaning, criteria, allowed_next]
  properties:
    id:
      type: string
      pattern: "^[a-z0-9_]+$"
    label:
      type: string
      minLength: 1
    emoji:
      type: string
      minLength: 1
    order:
      type: integer
      minimum: 0
    meaning:
      type: string
      minLength: 1
    criteria:
      type: array
      items: { type: string }
    allowed_next:
      type: array
      items: { type: string }
```

## Seeds

### seeds/glossary.yml

```yaml
# Field descriptions:
# - key: Stable, machine-friendly identifier in snake_case. Must be unique and should never change (other files may reference it).
# - term: Human-readable label (usually Title Case). Safe to tweak for wording, since references should point to key, not term.
# - definition: Plain-language explanation for humans. Use > (folded block) so it reads as one paragraph. Start with a crisp one-sentence summary; add a second line for nuance if needed.
# - examples: Short, real uses (1–3 items). Each item is a concise string that shows the term in context—an action, artifact, or sentence fragment.
# - see_also: List of related keys (not terms). Helps cross-link concepts within your docs.

- key: portfolio
  term: "Portfolio"
  definition: >
    Content intended for external viewing (landing pages, demos, docs).
    Aggregates public entry points across modules.
  examples:
    - "Launch Model GitHub Pages site"
  see_also: ["launch", "entry"]
```

### seeds/tags.yml

```yaml
# Field descriptions:
# - key: Stable, machine-friendly identifier in snake_case. Must be unique and should not change (dashboards and docs may reference it).
# - label: Human-readable display name (Title Case). Safe to tweak without breaking references (consumers should point to key).
# - description: Plain-language summary for humans. Use > (folded block) so it reads as one paragraph. Start with a crisp one-sentence summary; add an optional second line for nuance.
# - kind: Category for grouping/filters. Choose one from the allowed set: ["analytics_type","audience","capability","concept","credential","discipline","format","framework","governance","knowledge","language","nav","navigation","organization","pipeline","planning","platform","practice","process","quality","repository","requirements","role","skills","source","standard","streaming","technique","module","topic","kpi","status","orbit","tech"]
# - gloss_ref: The key of a related entry in seeds/glossary.yml. Validates cross-linking and keeps tags fewer than glossary terms.
# - deprecated: Boolean flag. Set to true to retire a tag without breaking older artifacts; prefer introducing a replacement tag and updating references over time.

- key: portfolio
  label: "Portfolio"
  description: >
    Public-facing entry artifacts across the constellation.
  kind: orbit
  gloss_ref: portfolio
  deprecated: false
```

**Notes:** Keep tags.yml intentionally smaller than glossary.yml; use it as the cross-module "integration surface." When in doubt, put specifics in the glossary and map them to a broader tag via gloss_ref.

### seeds/orbits.yml

```yaml
# Field descriptions:
# - id: Unique identifier in snake_case. Stable reference for cross-linking and validation. [REQUIRED]
# - label: Human-readable name (Title Case). Display-friendly orbital system name. [REQUIRED]
# - emoji: Visual identifier. Single Unicode character for UI representation. [REQUIRED]
# - order: Sort order. Integer for consistent constellation arrangement. [REQUIRED]
# - meaning: Purpose and high-level description of the orbital system. One-sentence summary of the orbit's role. [STRONGLY RECOMMENDED]
# - scope: Specific responsibilities and boundaries. Array of operational focus areas within this orbit. [STRONGLY RECOMMENDED]
# - includes: Repositories or components within this orbital system. Array of objects with repo property for constellation mapping. [STRONGLY RECOMMENDED]
# - kpis: Key performance indicators for measuring orbital health. Array of metrics for tracking system effectiveness. [STRONGLY RECOMMENDED]
# - policies: Governance rules and operational guidelines. Array of standards and procedures for orbit management. [STRONGLY RECOMMENDED]
# - see_also: Related orbital systems for cross-reference. Array of orbit IDs for navigation and context. [OPTIONAL]

- id: elemental-system
  label: "Elemental System"
  emoji: "☀️"
  order: 0
  meaning: "The hub repo housing primitives—seeds, artifacts, README, and public index."
  scope:
    - "Hub README.md and index.html (portfolio entry)"
    - "Canonical seed definitions (glossary.yml, tags.yml, statuses.yml, orbits.yml, registry.yml)"
    - "Shared assets, scaffolds, and templates"
    - "Governance notes and contribution guidelines"
  includes:
    - repo: "FourTwentyAnalytics"  # 🔘 barycenter & suitekeeper
  kpis:
    - "Seed schema validity (lint/CI passing)"
    - "Cross-repo seed compliance rate"
    - "Hub uptime and README freshness"
    - "Index render health (README/Pages load without errors)"
  policies:
    - "Schema changes require version bump and migration notes"
    - "Hub remains public; CI must pass before merge"
    - "Backwards-compatible deprecations for seed keys"
  see_also: ["core", "delivery-insight", "growth-experiment", "ancillary-operations"]
```

### seeds/emoji_palette.yml

```yaml
# Field descriptions:
# - status_icons: Map of status/state identifiers to emoji representations. Used for progress indicators and workflow states.
# - orbit_icons: Map of orbital system identifiers to emoji representations. Used for constellation navigation and visual organization.
# - module_icons: Map of module/repository identifiers to emoji representations. Used for project identification and branding.
# - tech_icons: Map of technology/tool identifiers to emoji representations. Used for tech stack visualization and documentation.

status_icons:
  seed: "🌱"
  sprout: "🌿"
  active: "🟢"
  pending: "🟡"
  error: "🔴"

orbit_icons:
  elemental_system: "☀️"
  core_system: "🪐"
  delivery_insight: "�"
  growth_experiment: "🧪"
  ancillary_operations: "🧩"
  
module_icons:
  fourtwenty_analytics: "🔘"
  launch_model: "🚀"
  archive_model: "🫀"
  signal_model: "📡"
  protector_model: "🛡️"

tech_icons:
  python: "🐍"
  javascript: "⚡"
  yaml: "📄"
  json: "🔧"
  sql: "🗃️"
  docker: "📦"
  aws: "☁️"
```

### seeds/statuses.yml

```yaml
# Field descriptions:
# - id: Unique identifier in snake_case. Stable reference for cross-linking and validation.
# - label: Human-readable name (Title Case). Display-friendly status name for UI and reports.
# - emoji: Visual identifier. Single Unicode character for status representation in dashboards and workflows.
# - order: Sort order. Integer for consistent status progression and lifecycle visualization.
# - meaning: Purpose and high-level description of the status. One-sentence summary of what this status represents in the module lifecycle.
# - criteria: Specific requirements and conditions. Array of measurable conditions that must be met to achieve this status.
# - allowed_next: Valid status transitions. Array of status IDs that can follow this status in the workflow progression.

- id: seed
  label: "Seed"
  emoji: "🌱"
  order: 01
  meaning: "Idea captured; repo exists; README stub."
  criteria: ["repo_created", "readme_stub"]
  allowed_next: ["sprout"]

- id: sprout
  label: "Sprout"
  emoji: "🌿"
  order: 02
  meaning: "Scaffold working; basic demo or notebook runs."
  criteria: ["scaffold_ready", "seeds_defined", "hello_world_demo"]
  allowed_next: ["budding", "dormant"]
```

## Signals

(Content to be added)

## Scripts

(Content to be added)

## Scrubs

(Content to be added)

## Workflows

(Content to be added)

## Assets

(Content to be added)

## Future Vision: Genesis Machine

The FourTwenty Analytics Genesis Machine represents a revolutionary evolution of this constellation—transforming static documentation into **executable literature**.

### The Executable Book Concept

Traditional books ask you to **read about** something. Technical manuals ask you to **follow steps** to build something.

The Genesis Machine asks you to **experience the creation** while it happens.

- **Chronological**: Sequential cell execution = chapter progression
- **Interactive**: Reader participates in creation  
- **Generative**: Produces artifacts beyond the reading experience
- **Repeatable**: Each "reading" (run) creates fresh genesis
- **Personalized**: Generated content belongs to the reader

### The Vision

When someone opens `FourTwentyGenesis.dib` and hits **"Run All"**, they don't just learn about analytics platforms—they **witness the birth of one** while experiencing the story of Chloe, the AI advisor who emerges from the validated data flows.

**This is computational storytelling at its finest, where the act of running code becomes the act of experiencing narrative, and technical achievement becomes inseparable from human meaning.**

### Perfect Portability

The entire book experience contained in a single `.dib` file:

- **Send via email**: Complete book + runtime environment
- **Demo distribution**: Recipients build the system locally
- **Version control**: Book evolution tracked through Git
- **Community editions**: Collaborative storytelling through code

*See `README.md` for complete Genesis Machine documentation and current development status.*

## License

MIT — See `LICENSE`. Use freely; please don't send PII to the sandbox.
