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
