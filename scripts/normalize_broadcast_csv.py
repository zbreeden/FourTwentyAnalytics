#!/usr/bin/env python3
"""Normalize data/internal/broadcast.csv

Creates a timestamped backup, then rewrites the CSV with the canonical header and
one clean row per record. This is defensive: it will attempt to parse malformed
CSV using the csv module and fall back to line-based parsing.

Usage:
  python3 scripts/normalize_broadcast_csv.py
"""
import csv
import os
import shutil
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, 'data', 'internal')
CSV_PATH = os.path.join(DATA_DIR, 'broadcast.csv')

HEADER = [
    "broadcast.id",
    "ts.utc5",
    "date",
    "module.id",
    "broadcast.rating",
    "broadcast.name",
    "broadcast.summary",
    "status.id",
    "artifact.git.link",
    "tags.keys",
    "glyph_icons",
    "status_icons",
]


def backup(src):
    if not os.path.exists(src):
        print(f"No CSV at {src} to back up")
        return None
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    dst = src + f'.bak.{ts}'
    shutil.copy2(src, dst)
    return dst


def read_rows(path):
    rows = []
    if not os.path.exists(path):
        return rows
    # First attempt: use csv.DictReader which can handle quoted newlines
    try:
        with open(path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                # Normalize keys to canonical header where possible
                if any(k in r for k in HEADER):
                    rows.append(r)
    except Exception as e:
        print('csv.DictReader failed:', e)

    # If no rows parsed, try a simpler line-by-line fallback
    if not rows:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip('\n')
                    if not line:
                        continue
                    try:
                        # parse single CSV line
                        parsed = next(csv.reader([line]))
                        # If it's header-like, skip
                        if 'broadcast.id' in parsed:
                            continue
                        # Map by position into header (best-effort)
                        d = {HEADER[i]: parsed[i] if i < len(parsed) else '' for i in range(len(HEADER))}
                        rows.append(d)
                    except Exception:
                        # as a last resort, put the whole line in broadcast.summary
                        d = {h: '' for h in HEADER}
                        d['broadcast.summary'] = line
                        rows.append(d)
        except Exception as e:
            print('line-based fallback failed:', e)

    return rows


def write_rows(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for r in rows:
            row = [r.get(h, '') for h in HEADER]
            writer.writerow(row)


def main():
    print('Backing up current CSV...')
    bak = backup(CSV_PATH)
    if bak:
        print('Backup created:', bak)
    rows = read_rows(CSV_PATH)
    print(f'Parsed {len(rows)} data rows')
    # best-effort: ensure each row is a dict with HEADER keys
    clean = []
    for r in rows:
        d = {h: (r.get(h) if isinstance(r.get(h), str) else (','.join(r.get(h)) if isinstance(r.get(h), list) else str(r.get(h) or ''))) for h in HEADER}
        clean.append(d)

    write_rows(CSV_PATH, clean)
    print('Wrote normalized CSV to', CSV_PATH)


if __name__ == '__main__':
    main()
