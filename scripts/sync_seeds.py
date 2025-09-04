import os, subprocess, tempfile, shutil, json, datetime, textwrap
from pathlib import Path
import yaml, requests

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "seeds" / "registry.yml"
SEEDSET  = ROOT / "seeds" / "seedset.yml"

API = "https://api.github.com"
TOKEN = os.environ.get("GH_TOKEN","")
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)

def load_yaml(p: Path):
    return yaml.safe_load(p.read_text()) if p.exists() else {}

def create_pr(owner, repo, head_branch, base, title, body):
    url = f"{API}/repos/{owner}/{repo}/pulls"
    r = requests.post(url, headers=HEADERS, json={
        "title": title, "head": head_branch, "base": base, "body": body, "maintainer_can_modify": True
    })
    if r.status_code in (200, 201):
        print(f"PR opened for {owner}/{repo}")
    elif r.status_code == 422 and "A pull request already exists" in r.text:
        print(f"PR already exists for {owner}/{repo}")
    else:
        print(f"PR create failed for {owner}/{repo}: {r.status_code} {r.text}")

def get_default_branch(owner, repo):
    r = requests.get(f"{API}/repos/{owner}/{repo}", headers=HEADERS)
    r.raise_for_status()
    return r.json()["default_branch"]

def copy_files(src_root: Path, dst_root: Path, files):
    changed = []
    for rel in files:
        src = src_root / rel
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            print(f"WARNING: source missing {rel}, skipping")
            continue
        old = dst.read_bytes() if dst.exists() else None
        new = src.read_bytes()
        if old != new:
            shutil.copy2(src, dst)
            changed.append(rel)
    return changed

def main():
    registry = load_yaml(REGISTRY).get("repos", [])
    files = load_yaml(SEEDSET).get("files", [])
    if not files:
        print("No files in seedset.yml; nothing to sync.")
        return

    ts = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    branch_name = f"seeds/sync-{ts}"
    hub_seed_source = ROOT

    for item in registry:
        owner, repo = item["owner"], item["name"]
        default_branch = get_default_branch(owner, repo)
        with tempfile.TemporaryDirectory() as td:
            repo_dir = Path(td) / repo
            run(["git", "clone", f"https://x-access-token:{TOKEN}@github.com/{owner}/{repo}.git", str(repo_dir)])
            run(["git", "checkout", "-b", branch_name, default_branch], cwd=repo_dir)

            changed = copy_files(hub_seed_source, repo_dir, files)
            if not changed:
                print(f"{owner}/{repo}: no changes.")
                continue

            run(["git", "add"] + changed, cwd=repo_dir)
            msg = f"chore(seeds): sync from hub\n\nUpdated:\n" + "\n".join(f"- {c}" for c in changed)
            run(["git", "commit", "-m", msg], cwd=repo_dir)
            run(["git", "push", "--set-upstream", "origin", branch_name], cwd=repo_dir)

            body = textwrap.dedent(f"""
            Syncing seed files from hub (FourTwentyAnalytics).

            Files updated:
            {chr(10).join(f"- `{c}`" for c in changed)}

            Generated: {ts} UTC
            """).strip()
            create_pr(owner, repo, branch_name, default_branch, "chore(seeds): sync from hub", body)

    print("Seed sync complete.")

if __name__ == "__main__":
    main()

