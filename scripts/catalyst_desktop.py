#!/usr/bin/env python3
"""
FourTwenty • The Catalyst — Desktop Buttons
- New Ticket → generates YAML (for seeds/tickets.yml)
- New Broadcast → generates JSON (for signals/latest.json)
- Copy to clipboard or Save to file in ./exports

Requires: Python 3.9+; pip install pyyaml
"""

import json
import os
import re
import sys
import datetime as dt
from pathlib import Path
from tkinter import (
    Tk, Toplevel, StringVar, BooleanVar, Text, END, BOTH, LEFT, RIGHT,
    N, S, E, W, X, Y, Label, Entry, OptionMenu, Button, Frame, Checkbutton,
    filedialog, messagebox
)

try:
    import yaml  # pip install pyyaml
except Exception:
    yaml = None

APP_TITLE = "FourTwenty • The Catalyst"
EXPORTS_DIR = Path(__file__).resolve().parent / "exports"
SEQ_FILE = Path(__file__).resolve().parent / ".ticket_seq.json"

STATUS_ENUM = ["open", "in_progress", "blocked", "on_hold", "review", "complete", "canceled"]
PRIORITY_ENUM = ["low", "medium", "high", "critical"]
SEVERITY_ENUM = ["minor", "moderate", "major", "critical"]
BROADCAST_RATING = ["info", "warning", "critical"]
BROADCAST_EVENT = ["ticket_created", "pulse_inactivity", "ticket_completed", "note"]

DEFAULT_ORIGIN = {
    "name": "FourTwenty • The Catalyst",
    "module": "catalyst-model",
    "emoji": "⚙️",
    "url": "https://zbreeden.github.io/catalyst-model/"
}

# ---------- Helpers ----------

def iso_utc_now():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def utc_date():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

def ensure_exports():
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return EXPORTS_DIR

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
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "unknown"

def copy_to_clipboard(root: Tk, text: str):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Keeps clipboard after app closes

def save_dialog(default_name: str, content: str):
    ensure_exports()
    path = filedialog.asksaveasfilename(
        initialdir=str(EXPORTS_DIR),
        initialfile=default_name,
        defaultextension="",
        filetypes=[("All Files", "*.*")]
    )
    if path:
        Path(path).write_text(content, encoding="utf-8")
        messagebox.showinfo("Saved", f"Saved to:\n{path}")

# ---------- Ticket Form ----------

class TicketForm(Toplevel):
    def __init__(self, master: Tk):
        super().__init__(master)
        self.title("New Ticket • The Catalyst")
        self.resizable(True, True)

        # Vars
        self.v_title = StringVar()
        self.v_owner = StringVar(value="suitekeeper")
        self.v_collab = StringVar()  # comma-separated
        self.v_orbit = StringVar(value="growth_experience")
        self.v_module = StringVar(value=DEFAULT_ORIGIN["module"])
        self.v_tags = StringVar()  # comma-separated
        self.v_status = StringVar(value="open")
        self.v_priority = StringVar(value="high")
        self.v_severity = StringVar(value="moderate")
        self.v_inactivity_days = StringVar(value="3")
        self.v_experiment = BooleanVar(value=True)
        self.v_baseline = StringVar(value="0")
        self.v_target = StringVar(value="1")
        self.v_conf = StringVar(value="0.9")

        # Layout
        pad = {"padx": 8, "pady": 6}

        def row(label, widget):
            r = Frame(self); r.pack(fill=X, **pad)
            Label(r, text=label, width=16, anchor="e").pack(side=LEFT)
            widget.pack(side=LEFT, fill=X, expand=True)
            return r

        row("Title*", Entry(self, textvariable=self.v_title))
        row("Description", self._multiline())
        row("Owner*", Entry(self, textvariable=self.v_owner))
        row("Collaborators", Entry(self, textvariable=self.v_collab))
        row("Orbit", Entry(self, textvariable=self.v_orbit))
        row("Module", Entry(self, textvariable=self.v_module))
        row("Tags", Entry(self, textvariable=self.v_tags))

        r = Frame(self); r.pack(fill=X, **pad)
        Label(r, text="Status*", width=16, anchor="e").pack(side=LEFT)
        OptionMenu(r, self.v_status, *STATUS_ENUM).pack(side=LEFT)
        Label(r, text="Priority*", width=12, anchor="e").pack(side=LEFT)
        OptionMenu(r, self.v_priority, *PRIORITY_ENUM).pack(side=LEFT)
        Label(r, text="Severity*", width=12, anchor="e").pack(side=LEFT)
        OptionMenu(r, self.v_severity, *SEVERITY_ENUM).pack(side=LEFT)

        r = Frame(self); r.pack(fill=X, **pad)
        Label(r, text="Inactivity days", width=16, anchor="e").pack(side=LEFT)
        Entry(r, textvariable=self.v_inactivity_days, width=8).pack(side=LEFT)
        Checkbutton(r, text="Experiment", variable=self.v_experiment).pack(side=LEFT, padx=12)
        Label(r, text="Baseline", width=10, anchor="e").pack(side=LEFT)
        Entry(r, textvariable=self.v_baseline, width=8).pack(side=LEFT)
        Label(r, text="Target", width=8, anchor="e").pack(side=LEFT)
        Entry(r, textvariable=self.v_target, width=8).pack(side=LEFT)
        Label(r, text="Conf (0-1)", width=12, anchor="e").pack(side=LEFT)
        Entry(r, textvariable=self.v_conf, width=8).pack(side=LEFT)

        # Output
        self.out = Text(self, height=14, wrap="word")
        self.out.pack(fill=BOTH, expand=True, **pad)

        # Buttons
        b = Frame(self); b.pack(fill=X, **pad)
        Button(b, text="Generate YAML", command=self.generate).pack(side=LEFT)
        Button(b, text="Copy YAML", command=self.copy).pack(side=LEFT, padx=6)
        Button(b, text="Save as…", command=self.save).pack(side=LEFT)
        Button(b, text="Close", command=self.destroy).pack(side=RIGHT)

    def _multiline(self):
        self.desc = Text(self, height=4, wrap="word")
        return self.desc

    def generate(self):
        if not self.v_title.get().strip():
            messagebox.showerror("Missing field", "Title is required.")
            return
        owner = snakeify(self.v_owner.get() or "suitekeeper")
        collab = [snakeify(x) for x in self.v_collab.get().split(",") if x.strip()]
        tags = [snakeify(x) for x in self.v_tags.get().split(",") if x.strip()]
        now = iso_utc_now()
        tid = next_ticket_id()

        try:
            inactivity = int(self.v_inactivity_days.get() or "0")
        except ValueError:
            inactivity = 0

        ticket = {
            "id": tid,
            "title": self.v_title.get().strip(),
            "description": self.desc.get("1.0", END).strip() or "—",
            "owner": owner,
            "collaborators": collab or None,
            "orbit": snakeify(self.v_orbit.get() or "growth_experience"),
            "module": snakeify(self.v_module.get() or DEFAULT_ORIGIN["module"]),
            "tags": tags or None,
            "status": self.v_status.get(),
            "priority": self.v_priority.get(),
            "severity": self.v_severity.get(),
            "created_at": now,
            "updated_at": now,
            "inactivity_threshold_days": inactivity if inactivity > 0 else None,
            "experiment_flag": bool(self.v_experiment.get()),
            "baseline_metric": float(self.v_baseline.get() or 0),
            "target_metric": float(self.v_target.get() or 0),
            "confidence_goal": float(self.v_conf.get() or 0.9),
            "history": [
                {"ts_utc": now, "event": "status_change", "note": "Ticket created", "actor": owner}
            ],
        }

        # Remove Nones for minimal clean YAML
        ticket = {k: v for k, v in ticket.items() if v not in (None, [], "")}

        # YAML list item ready to append to seeds/tickets.yml
        if yaml:
            yaml_block = yaml.dump([ticket], sort_keys=False, allow_unicode=True)
        else:
            # Fallback: minimal JSON-as-YAML-ish
            yaml_block = "- " + json.dumps(ticket, ensure_ascii=False, indent=2) + "\n"

        self.out.delete("1.0", END)
        self.out.insert("1.0", yaml_block)

    def copy(self):
        copy_to_clipboard(self, self.out.get("1.0", END))

    def save(self):
        ensure_exports()
        default = f"{iso_utc_now().replace(':','').replace('-','').replace('T','_').replace('Z','Z')}-ticket.yml"
        save_dialog(default, self.out.get("1.0", END))

# ---------- Broadcast Form ----------

class BroadcastForm(Toplevel):
    def __init__(self, master: Tk):
        super().__init__(master)
        self.title("New Broadcast • The Catalyst")
        self.resizable(True, True)

        # Vars
        self.v_event = StringVar(value="ticket_created")
        self.v_rating = StringVar(value="info")
        self.v_title = StringVar()
        self.v_summary = StringVar()
        self.v_module = StringVar(value=DEFAULT_ORIGIN["module"])
        self.v_ticket_id = StringVar()
        self.v_tags = StringVar()  # comma

        pad = {"padx": 8, "pady": 6}

        def row(label, widget):
            r = Frame(self); r.pack(fill=X, **pad)
            Label(r, text=label, width=16, anchor="e").pack(side=LEFT)
            widget.pack(side=LEFT, fill=X, expand=True)
            return r

        row("Event", OptionMenu(self, self.v_event, *BROADCAST_EVENT))
        row("Rating", OptionMenu(self, self.v_rating, *BROADCAST_RATING))
        row("Title*", Entry(self, textvariable=self.v_title))
        row("Summary", Entry(self, textvariable=self.v_summary))
        row("Module", Entry(self, textvariable=self.v_module))
        row("Ticket ID", Entry(self, textvariable=self.v_ticket_id))
        row("Tags", Entry(self, textvariable=self.v_tags))

        self.out = Text(self, height=14, wrap="word")
        self.out.pack(fill=BOTH, expand=True, **pad)

        b = Frame(self); b.pack(fill=X, **pad)
        Button(b, text="Generate JSON", command=self.generate).pack(side=LEFT)
        Button(b, text="Copy JSON", command=self.copy).pack(side=LEFT, padx=6)
        Button(b, text="Save as…", command=self.save).pack(side=LEFT)
        Button(b, text="Close", command=self.destroy).pack(side=RIGHT)

    def generate(self):
        if not self.v_title.get().strip():
            messagebox.showerror("Missing field", "Title is required.")
            return

        now = iso_utc_now()
        tags = [snakeify(x) for x in self.v_tags.get().split(",") if x.strip()]
        obj = {
            "id": f"{utc_date()}-catalyst-broadcast",
            "ts_utc": now,
            "event": self.v_event.get(),
            "rating": self.v_rating.get(),
            "title": self.v_title.get().strip(),
            "summary": self.v_summary.get().strip() or "—",
            "origin": {
                "name": DEFAULT_ORIGIN["name"],
                "module": snakeify(self.v_module.get() or DEFAULT_ORIGIN["module"]),
                "emoji": DEFAULT_ORIGIN["emoji"],
                "url": DEFAULT_ORIGIN["url"],
            },
            "tags": tags or [],
        }
        if self.v_ticket_id.get().strip():
            obj["ticket_id"] = self.v_ticket_id.get().strip()

        text = json.dumps(obj, ensure_ascii=False, indent=2)
        self.out.delete("1.0", END)
        self.out.insert("1.0", text + "\n")

    def copy(self):
        copy_to_clipboard(self, self.out.get("1.0", END))

    def save(self):
        ensure_exports()
        default = f"{iso_utc_now().replace(':','').replace('-','').replace('T','_').replace('Z','Z')}-broadcast.json"
        save_dialog(default, self.out.get("1.0", END))

# ---------- Main Window ----------

def main():
    root = Tk()
    root.title(APP_TITLE)
    root.geometry("680x600")

    # Header
    header = Frame(root); header.pack(fill=X, padx=12, pady=12)
    Label(header, text="⚙️  The Catalyst — Desktop Automations", font=("Helvetica", 16, "bold")).pack(anchor="w")
    Label(header, text="Create ticket YAML or broadcast JSON, then copy or save to import into repos.").pack(anchor="w")

    # Buttons
    actions = Frame(root); actions.pack(fill=X, padx=12, pady=8)
    Button(actions, text="New Ticket", width=20, command=lambda: TicketForm(root)).pack(side=LEFT, padx=6)
    Button(actions, text="New Broadcast", width=20, command=lambda: BroadcastForm(root)).pack(side=LEFT, padx=6)

    # Footer
    footer = Frame(root); footer.pack(fill=X, padx=12, pady=12)
    Label(footer, text=f"Exports folder: {ensure_exports()}", fg="#666").pack(anchor="w")

    root.mainloop()

if __name__ == "__main__":
    if yaml is None:
        print("WARNING: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    main()

