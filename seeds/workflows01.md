How to run it now (manual)
In the hub repo (FourTwentyAnalytics) add a PAT secret first:
Create a fine-grained Personal Access Token with Repository contents: Read/Write for all target repos.
Save it in the hub repo as GH_TOKEN.
(The built-in GITHUB_TOKEN can’t push to other repos; a PAT is required.)
Go to Actions → “Sync Seeds to Modules” → Run workflow.
That opens PRs in each target repo with the seed updates.
How to automate it later
It already auto-runs on push to any file under seeds/** in the hub (so edits to seeds kick off sync automatically).

To also do time-based drift control, add a schedule to the workflow:
-yaml
on:
  push:
    paths:
      - 'seeds/**'
      - 'scripts/sync_seeds.py'
      - '.github/workflows/sync_seeds.yml'
  schedule:
    - cron: '15 10 * * 1,4'   # Mondays & Thursdays 10:15 UTC
  workflow_dispatch: {}

Nice-to-haves
Add concurrency so runs don’t overlap:
-yaml
concurrency:
  group: sync-seeds
  cancel-in-progress: true

Keep branch protections on; the script opens PRs (not force-push), so it’s safe.
When you’re ready, enable auto-merge in each target repo so seed PRs merge once checks pass.
That’s it: manual to seed the first round; then it’s fully automated on seed changes (plus scheduled drift sweeps if you enable the cron).

oh wow.. so, anytime I am working within a specific sun and make changes to the seeds, The Archive will see this and make the run?

Short answer: not yet by default. Right now your Archive pulse runs on a schedule (and manual). But you can make it fire immediately whenever any “sun” (module repo) changes seeds—with one tiny cross-repo trigger.
Option A — Simple & reliable (scheduled)
Bump the Archive’s schedule to something tighter, e.g., every 15 minutes:

# archive-model/.github/workflows/pulse.yml
on:
  schedule:
    - cron: "*/15 * * * *"   # every 15 minutes
  workflow_dispatch: {}

This needs no extra secrets and will pick up merged changes shortly after they land on each repo’s default branch.
Option B — Instant pulses (event-driven)

Let Archive accept a dispatch:

-yaml
# archive-model/.github/workflows/pulse.yml
on:
  repository_dispatch:
    types: [seeds-updated]
  schedule:
    - cron: "20 9 * * *"
  workflow_dispatch: {}

Have each module ping Archive when seeds change:
Add to every module repo:

-yaml
# .github/workflows/notify_archive.yml  (in each “sun” repo)
name: Notify Archive on seed changes
on:
  push:
    paths:
      - 'seeds/**'   # only when seed files change
jobs:
  dispatch:
    runs-on: ubuntu-latest
    steps:
      - uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.ARCHIVE_DISPATCH_TOKEN }}   # PAT with repo:write for archive-model
          repository: zbreeden/archive-model
          event-type: seeds-updated
          client-payload: >-
            { "source": "${{ github.repository }}",
              "ref": "${{ github.ref_name }}",
              "commit": "${{ github.sha }}" }

🔐 Token setup: Create a fine-grained PAT scoped to zbreeden/archive-model (Repo contents: Read/Write). Save it as ARCHIVE_DISPATCH_TOKEN in each module repo (or as an org/repo environment secret shared to them).
Notes
The Archive pulse reads merged state (default branch). It won’t see changes living only in PRs unless you extend it to scan PR heads.
You can keep both: event-driven for instant runs + schedule as a safety net.
Your hub sync still works the same; once seed PRs are merged in modules, the dispatch (or schedule) will trigger Archive to re-index/lint.
