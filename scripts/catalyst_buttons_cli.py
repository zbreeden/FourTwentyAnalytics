#!/usr/bin/env python3
"""
FourTwenty • The Catalyst — CLI Buttons (no GUI)
- New Ticket → generates YAML (for seeds/tickets.yml)
- New Broadcast → generates JSON (for signals/latest.json)
- Saves to ./exports and also prints to terminal
- Optional clipboard copy on macOS via pbcopy (no extra deps)

Run:
  python3 catalyst_buttons_cli.py
Or direct:
  python3 catalyst_buttons_cli.py --mode ticket
  python3 catalyst_buttons_cli.py --mode broadcast
"""

import os, sys, re, json, argparse, datetime as dt, subprocess
from pathlib import Path

try:
    import yaml  # optional; if missing we'll emit YAML manually
except Exception:
    yaml = None

APP_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = APP_DIR / "exports"
SEQ_FILE = APP_DIR / ".ticket_seq.json"

STATUS_ENUM   = ["open", "in_progress", "blocked", "on_hold", "review", "complete", "canceled"]
PRIORITY_ENUM = ["low", "medium", "high", "critical"]
SEVERITY_ENUM = ["minor", "moderate", "major", "critical"]
BROADCAST_RATING = ["info", "warning", "critical"]
BROADCAST_EVENT  = ["ticket_created", "pulse_inactivity", "ticket_completed", "note"]

DEFAULT_ORIGIN = {
    "name": "FourTwenty • The Catalyst",
    "module": "catalyst-model",
    "emoji": "⚡",
    "url": "https://zbreeden.github.io/catalyst-model/"
}

def ensure_exports():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

def iso_utc_now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def utc_date():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

def load_seq():
    if SEQ_FILE.exists():
        try:
            return json.loads(SEQ_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"year": dt.datetime.now().year, "seq": 0}

def save_seq(data):
    SEQ_FILE.write_text(json.dumps(data), encoding="utf-8")

def next_ticket_id():
    data = load_seq()
    year = dt.datetime.now().year
    if data.get("year") != year:
        data["year"] = year
        data["seq"] = 0
    data["seq"] += 1
    save_seq(data)
    return f"TKT-{year}-{data['seq']:03d}"

def snakeify(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "unknown"

def prompt(label, default=None, required=False, choices=None):
    while True:
        d = f" [{default}]" if default not in (None, "") else ""
        c = f" ({'/'.join(choices)})" if choices else ""
        val = input(f"{label}{c}{d}: ").strip()
        if not val and default is not None:
            val = str(default)
        if required and not val:
            print("  -> required")
            continue
        if choices and val not in choices:
            print(f"  -> choose one of: {choices}")
            continue
        return val

def yesno(label, default=True):
    d = "Y/n" if default else "y/N"
    while True:
        val = input(f"{label} [{d}]: ").strip().lower()
        if not val:
            return default
        if val in ("y", "yes"): return True
        if val in ("n", "no"):  return False

def mac_copy(text):
    if sys.platform == "darwin":
        try:
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(input=text.encode("utf-8"))
            return True
        except Exception:
            return False
    return False

def to_yaml_list_block(items):
    """Emit a YAML list with minimal dependencies if PyYAML isn't installed."""
    def emit_scalar(v):
        if isinstance(v, bool):   return "true" if v else "false"
        if isinstance(v, (int, float)): return str(v)
        if v is None:            return "null"
        s = str(v)
        if re.search(r'[:\-\[\]\{\}\n\r\t#]', s):
            s = s.replace('"', '\\"')
            return f'"{s}"'
        return s

    lines = []
    for obj in items:
        lines.append("-")
        for k, v in obj.items():
            if isinstance(v, list):
                if not v:
                    lines.append(f"  {k}: []")
                else:
                    lines.append(f"  {k}:")
                    for x in v:
                        if isinstance(x, dict):
                            lines.append("    -")
                            for kk, vv in x.items():
                                lines.append(f"      {kk}: {emit_scalar(vv)}")
                        else:
                            lines.append(f"    - {emit_scalar(x)}")
            elif isinstance(v, dict):
                lines.append(f"  {k}:")
                for kk, vv in v.items():
                    lines.append(f"    {kk}: {emit_scalar(vv)}")
            else:
                lines.append(f"  {k}: {emit_scalar(v)}")
    return "\n".join(lines) + "\n"

def new_ticket():
    print("\n=== New Ticket ===")
    title = prompt("Title", required=True)
    description = prompt("Description", default="—")
    owner = snakeify(prompt("Owner", default="suitekeeper"))
    collaborators = [snakeify(x) for x in prompt("Collaborators (comma)", default="").split(",") if x.strip()]
    orbit = snakeify(prompt("Orbit", default="growth_experience"))
    module = snakeify(prompt("Module", default=DEFAULT_ORIGIN["module"]))
    tags = [snakeify(x) for x in prompt("Tags (comma)", default="").split(",") if x.strip()]
    status = prompt("Status", default="open", choices=STATUS_ENUM)
    priority = prompt("Priority", default="high", choices=PRIORITY_ENUM)
    severity = prompt("Severity", default="moderate", choices=SEVERITY_ENUM)
    inactivity_str = prompt("Inactivity threshold days (empty=none)", default="")
    try:
        inactivity = int(inactivity_str) if inactivity_str else None
    except ValueError:
        inactivity = None
    experiment = yesno("Experiment ticket?", True)
    baseline = float(prompt("Baseline metric", default="0"))
    target   = float(prompt("Target metric", default="1"))
    conf     = float(prompt("Confidence goal (0–1)", default="0.9"))

    now = iso_utc_now()
    tid = next_ticket_id()

    ticket = {
        "id": tid,
        "title": title,
        "description": description,
        "owner": owner,
        "collaborators": collaborators or None,
        "orbit": orbit,
        "module": module,
        "tags": tags or None,
        "status": status,
        "priority": priority,
        "severity": severity,
        "created_at": now,
        "updated_at": now,
        "inactivity_threshold_days": inactivity,
        "experiment_flag": bool(experiment),
        "baseline_metric": baseline,
        "target_metric": target,
        "confidence_goal": conf,
        "history": [
            {"ts_utc": now, "event": "status_change", "note": "Ticket created", "actor": owner}
        ],
    }
    # remove Nones
    ticket = {k: v for k, v in ticket.items() if v not in (None, [], "")}

    if yaml:
        content = yaml.dump([ticket], sort_keys=False, allow_unicode=True)
    else:
        content = to_yaml_list_block([ticket])

    ensure_exports()
    fname = f"{iso_utc_now().replace(':','').replace('-','').replace('T','_').replace('Z','Z')}-{tid}-ticket.yml"
    outpath = EXPORTS_DIR / fname
    outpath.write_text(content, encoding="utf-8")

    print("\n--- YAML (also saved to exports) ---\n")
    print(content)
    if mac_copy(content):
        print("(Copied to clipboard ✅)")
    print(f"Saved: {outpath}\n")
    return 0

def new_broadcast():
    print("\n=== New Broadcast ===")
    event = prompt("Event", default="ticket_created", choices=BROADCAST_EVENT)
    rating = prompt("Rating", default="info", choices=BROADCAST_RATING)
    title = prompt("Title", required=True)
    summary = prompt("Summary", default="—")
    module = snakeify(prompt("Module", default=DEFAULT_ORIGIN["module"]))
    ticket_id = prompt("Ticket ID (optional)", default="")
    tags = [snakeify(x) for x in prompt("Tags (comma)", default="").split(",") if x.strip()]

    obj = {
        "id": f"{utc_date()}-catalyst-broadcast",
        "ts_utc": iso_utc_now(),
        "event": event,
        "rating": rating,
        "title": title,
        "summary": summary,
        "origin": {
            "name": DEFAULT_ORIGIN["name"],
            "module": module,
            "emoji": DEFAULT_ORIGIN["emoji"],
            "url": DEFAULT_ORIGIN["url"],
        },
        "tags": tags,
    }
    if ticket_id:
        obj["ticket_id"] = ticket_id  # <-- fixed line

    content = json.dumps(obj, ensure_ascii=False, indent=2)

    ensure_exports()
    fname = f"{iso_utc_now().replace(':','').replace('-','').replace('T','_').replace('Z','Z')}-broadcast.json"
    outpath = EXPORTS_DIR / fname
    outpath.write_text(content + "\n", encoding="utf-8")

    print("\n--- JSON (also saved to exports) ---\n")
    print(content)
    if mac_copy(content):
        print("(Copied to clipboard ✅)")
    print(f"Saved: {outpath}\n")
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["menu", "ticket", "broadcast"], default="menu")
    args = ap.parse_args()

    if args.mode == "ticket":    return new_ticket()
    if args.mode == "broadcast": return new_broadcast()

    print("\n⚡  The Catalyst — CLI Buttons")
    print("1) New Ticket")
    print("2) New Broadcast")
    print("q) Quit")
    while True:
        choice = input("> ").strip().lower()
        if choice == "1": new_ticket()
        elif choice == "2": new_broadcast()
        elif choice in ("q", "quit", "exit"): break
        else: print("Choose 1, 2, or q")
    return 0

if __name__ == "__main__":
    sys.exit(main())

