#!/usr/bin/env python3
"""
Lightweight HTTP server to accept broadcast JSON and append rows to data/internal/broadcast.csv

Usage:
  python3 scripts/broadcast_server.py

The server listens on 127.0.0.1:5000 and exposes POST /api/broadcast which accepts a JSON payload
matching the form fields. It will ensure the CSV file exists and append a row using the canonical
header defined in this repo's scripts/broadcast.py.
"""
import http.server
import socketserver
import json
import os
import csv
from datetime import datetime, timedelta, timezone
try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

# Optional YAML support for seed validations
try:
    import yaml
except Exception:
    yaml = None

PORT = 5002
HOST = '127.0.0.1'
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, 'data', 'internal')
CSV_PATH = os.path.join(DATA_DIR, 'broadcast.csv')
SEEDS_DIR = os.path.join(REPO_ROOT, 'seeds')
MODULES_YML = os.path.join(SEEDS_DIR, 'modules.yml')
STATUSES_YML = os.path.join(SEEDS_DIR, 'statuses.yml')
EMOJI_YML = os.path.join(SEEDS_DIR, 'emoji_palette.yml')

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


def ensure_csv():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)


def load_seeds():
    modules = {}
    statuses = {}
    emoji = {}
    if yaml is None:
        return None, None, None
    try:
        if os.path.exists(MODULES_YML):
            with open(MODULES_YML, 'r', encoding='utf-8') as f:
                raw = yaml.safe_load(f) or {}
                # modules.yml in this repo is a YAML list of mappings with `id` keys
                if isinstance(raw, list):
                    for item in raw:
                        if isinstance(item, dict) and 'id' in item:
                            modules[item['id']] = item
                elif isinstance(raw, dict):
                    modules = raw
        if os.path.exists(STATUSES_YML):
            with open(STATUSES_YML, 'r', encoding='utf-8') as f:
                raw = yaml.safe_load(f) or {}
                if isinstance(raw, list):
                    for item in raw:
                        if isinstance(item, dict) and 'id' in item:
                            statuses[item['id']] = item
                elif isinstance(raw, dict):
                    statuses = raw
        if os.path.exists(EMOJI_YML):
            with open(EMOJI_YML, 'r', encoding='utf-8') as f:
                emoji = yaml.safe_load(f) or {}
    except Exception:
        # On any YAML parse error, return empty dicts to avoid crashing
        return {}, {}, {}
    return modules, statuses, emoji


def utc5_now_iso():
    # Fallback: return UTC timestamp if timezone handling isn't required
    now = datetime.now(timezone.utc)
    return now.isoformat(timespec='seconds')


def to_eastern_iso(ts_str=None):
    """Convert an ISO timestamp string or None to America/New_York-aware ISO string.
    If ts_str is None, use now UTC converted to ET.
    """
    # parse incoming timestamp
    if ts_str:
        try:
            if ts_str.endswith('Z'):
                dt = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(ts_str)
        except Exception:
            # try loose parse
            try:
                dt = datetime.strptime(ts_str, '%Y-%m-%dT%H:%M:%S')
                dt = dt.replace(tzinfo=timezone.utc)
            except Exception:
                raise
    else:
        dt = datetime.now(timezone.utc)

    # ensure timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    if ZoneInfo is None:
        # ZoneInfo unavailable; return UTC iso as fallback
        return dt.astimezone(timezone.utc).replace(tzinfo=None).isoformat(timespec='seconds')

    eastern = dt.astimezone(ZoneInfo('America/New_York'))
    return eastern.isoformat()


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code=200, payload=None):
        self.send_response(code)
        # CORS: allow local dev origins to POST from the static site
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if payload is None:
            payload = {}
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def do_OPTIONS(self):
        # respond to CORS preflight
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            if self.path != '/api/broadcast':
                return self._send(404, {'error': 'not found'})

            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8') if length > 0 else ''

            try:
                data = json.loads(body)
            except Exception as e:
                return self._send(400, {'error': 'invalid json', 'details': str(e)})

            # Normalize common dot-separated keys from signals/latest.json
            # into the flat keys the server expects (moduleId, broadcastName, etc.)
            normalized = {}
            # broadcast id
            if 'broadcast.id' in data:
                normalized['broadcastId'] = data.get('broadcast.id')
            if 'broadcastId' in data:
                normalized['broadcastId'] = normalized.get('broadcastId') or data.get('broadcastId')

            # timestamp variants
            if 'ts.utc5' in data:
                normalized['timestamp'] = data.get('ts.utc5')
            if 'timestamp' in data:
                normalized['timestamp'] = normalized.get('timestamp') or data.get('timestamp')

            # module id
            if 'module.id' in data:
                normalized['moduleId'] = data.get('module.id')
            if 'moduleId' in data:
                normalized['moduleId'] = normalized.get('moduleId') or data.get('moduleId')

            # broadcast fields
            if 'broadcast.name' in data:
                normalized['broadcastName'] = data.get('broadcast.name')
            if 'broadcast.summary' in data:
                normalized['broadcastSummary'] = data.get('broadcast.summary')
            if 'broadcast.rating' in data:
                normalized['broadcastRating'] = data.get('broadcast.rating')

            # status
            if 'status.id' in data:
                normalized['statusId'] = data.get('status.id')

            # artifact link
            if 'artifact.git.link' in data:
                normalized['artifactGitLink'] = data.get('artifact.git.link')

            # tags
            if 'tags.keys' in data:
                normalized['tagsKeys'] = data.get('tags.keys')

            # merge normalized keys back into data (without overwriting existing explicit fields)
            for k, v in normalized.items():
                if k not in data or not data.get(k):
                    data[k] = v

            # load seed data for validation (optional)
            modules, statuses, emoji = load_seeds()

            # Map incoming data to header fields with sensible defaults
            module_id = (data.get('moduleId') or data.get('module_id') or '').strip()
            if not module_id:
                return self._send(400, {'error': 'moduleId is required'})

            # Validate module id if modules loaded
            if modules is not None and modules != {}:
                module_keys = []
                if isinstance(modules, dict):
                    module_keys = list(modules.keys())
                if module_id not in module_keys:
                    return self._send(400, {'error': 'unknown moduleId', 'details': f"{module_id} not found in modules.yml"})

            # Validate broadcast rating
            allowed_ratings = ['critical', 'high', 'normal', 'mundane']
            if emoji and isinstance(emoji, dict):
                for k in ('ratings', 'broadcast_ratings'):
                    if k in emoji and isinstance(emoji[k], dict):
                        allowed_ratings = list(emoji[k].keys())
                        break

            rating = (data.get('broadcastRating') or data.get('broadcast_rating') or '').strip()
            if rating and rating not in allowed_ratings:
                return self._send(400, {'error': 'invalid broadcastRating', 'allowed': allowed_ratings})

            # Validate status if statuses available
            status = (data.get('statusId') or data.get('status_id') or '').strip()
            if statuses and isinstance(statuses, dict):
                status_keys = list(statuses.keys())
                if status and status not in status_keys:
                    return self._send(400, {'error': 'invalid statusId', 'details': f"{status} not in statuses.yml"})

            # Server-authoritative timestamp: ignore any client-supplied timestamp
            try:
                ts_et = to_eastern_iso(None)
            except Exception as e:
                return self._send(500, {'error': 'failed to compute server timestamp', 'details': str(e)})

            # build broadcast id if not provided - canonical UTC Z timestamp + repo + module
            broadcast_id = (data.get('broadcastId') or data.get('broadcast_id') or '').strip()
            if not broadcast_id:
                utc_now = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
                safe_module = module_id.replace(' ', '-').replace('/', '-')
                broadcast_id = f"{utc_now}-FourTwentyAnalytics-{safe_module}"

            # Ensure uniqueness by checking existing CSV
            try:
                ensure_csv()
                existing_ids = set()
                with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        existing_ids.add(r.get('broadcast.id'))
                unique_id = broadcast_id
                suffix = 1
                while unique_id in existing_ids:
                    unique_id = f"{broadcast_id}-{suffix}"
                    suffix += 1
                broadcast_id = unique_id
            except Exception as e:
                return self._send(500, {'error': 'failed to check existing csv', 'details': str(e)})

            date = ts_et.split('T')[0] if 'T' in ts_et else ts_et.split(' ')[0]

            # Enrich glyph_icons from modules.yml and status_icons from emoji palette when available.
            # If the repo-level emoji palette doesn't provide mappings for the module glyph keys,
            # fall back to the module's own `emoji` / icon field where present.
            glyphs_list = []
            status_icons_list = []
            try:
                module_entry = {}
                if modules and isinstance(modules, dict) and module_id in modules:
                    module_entry = modules.get(module_id) or {}
                    # module_entry may have 'glyphs' or variants in YAML
                    glyphs_candidates = module_entry.get('glyphs') or module_entry.get('glyphs:') or module_entry.get('glyphs', [])
                    if isinstance(glyphs_candidates, list):
                        glyphs_list = glyphs_candidates

                # Attempt to map glyph keys to emojis via emoji['glyph_icons']
                glyph_icons_field = ''
                mapped = []
                if emoji and isinstance(emoji, dict) and 'glyph_icons' in emoji and glyphs_list:
                    mapped = [emoji['glyph_icons'].get(g, '') for g in glyphs_list]
                    mapped = [m for m in mapped if m]

                if mapped:
                    glyph_icons_field = ','.join(mapped)
                else:
                    # Fallback 1: use module's own emoji/icon field if present
                    mod_emoji = module_entry.get('emoji') or module_entry.get('icon') or module_entry.get('glyph')
                    if isinstance(mod_emoji, list) and mod_emoji:
                        glyph_icons_field = ','.join(mod_emoji)
                    elif isinstance(mod_emoji, str) and mod_emoji:
                        glyph_icons_field = mod_emoji
                    else:
                        # Final fallback: return the raw glyph keys joined (so something is present)
                        glyph_icons_field = ','.join(glyphs_list)

                status_icons_field = ''
                # Prefer deriving the status icon from the broadcast rating (e.g. critical/high/normal)
                # This allows the icon to reflect the severity/importance of the broadcast.
                try:
                    icon = None
                    if emoji and isinstance(emoji, dict):
                        # 1) Try mapping rating -> status icon (backwards compatible if status_icons keyed by rating)
                        if rating:
                            if 'status_icons' in emoji and isinstance(emoji['status_icons'], dict):
                                icon = emoji['status_icons'].get(rating)
                            # 2) Try explicit ratings mapping (common names: 'ratings' or 'broadcast_ratings')
                            if not icon:
                                for key in ('ratings', 'broadcast_ratings'):
                                    if key in emoji and isinstance(emoji[key], dict):
                                        icon = emoji[key].get(rating)
                                        if icon:
                                            break
                        # 3) Fallback: if no rating-based icon, fall back to status id mapping (legacy behavior)
                        if not icon and status and 'status_icons' in emoji and isinstance(emoji['status_icons'], dict):
                            icon = emoji['status_icons'].get(status)
                    if icon:
                        status_icons_field = icon
                    else:
                        status_icons_field = ''
                except Exception:
                    status_icons_field = ''
            except Exception:
                glyph_icons_field = ''
                status_icons_field = ''

            row = [
                broadcast_id,
                ts_et,
                date,
                module_id,
                rating,
                data.get('broadcastName') or data.get('broadcast_name') or '',
                data.get('broadcastSummary') or data.get('broadcast_summary') or '',
                status,
                data.get('artifactGitLink') or data.get('artifact_git_link') or '',
                ','.join(data.get('tagsKeys') if isinstance(data.get('tagsKeys'), list) else (str(data.get('tagsKeys') or '')).split(',')),
                glyph_icons_field,
                status_icons_field,
            ]

            try:
                with open(CSV_PATH, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
            except Exception as e:
                return self._send(500, {'error': 'failed to write csv', 'details': str(e)})

            # Update signals archive and latest JSON files
            try:
                SIGNALS_DIR = os.path.join(REPO_ROOT, 'signals')
                os.makedirs(SIGNALS_DIR, exist_ok=True)
                latest_path = os.path.join(SIGNALS_DIR, 'latest.json')
                archive_path = os.path.join(SIGNALS_DIR, 'archive.latest.json')

                # load existing latest.json (if present) and append to archive
                old_entry = None
                if os.path.exists(latest_path):
                    try:
                        with open(latest_path, 'r', encoding='utf-8') as lf:
                            loaded = json.load(lf)
                            # latest.json may be an object or a single-item array
                            if isinstance(loaded, list):
                                old_entry = loaded[0] if loaded else None
                            else:
                                old_entry = loaded
                    except Exception:
                        old_entry = None

                archive = []
                if os.path.exists(archive_path):
                    try:
                        with open(archive_path, 'r', encoding='utf-8') as af:
                            archive = json.load(af) or []
                    except Exception:
                        archive = []

                if old_entry:
                    # Prepend so newest entries are first
                    archive = [old_entry] + archive

                # write updated archive atomically
                tmp_archive = archive_path + '.tmp'
                try:
                    with open(tmp_archive, 'w', encoding='utf-8') as af:
                        json.dump(archive, af, indent=2, ensure_ascii=False)
                    os.replace(tmp_archive, archive_path)
                except Exception:
                    # non-fatal; continue
                    try:
                        if os.path.exists(tmp_archive):
                            os.remove(tmp_archive)
                    except Exception:
                        pass

                # build new latest entry object
                new_entry = {
                    'broadcast.id': broadcast_id,
                    'ts.utc5': ts_et,
                    'date': date,
                    'module.id': module_id,
                    'broadcast.rating': rating,
                    'broadcast.name': data.get('broadcastName') or data.get('broadcast_name') or '',
                    'broadcast.summary': data.get('broadcastSummary') or data.get('broadcast_summary') or '',
                    'status.id': status,
                    'artifact.git.link': data.get('artifactGitLink') or data.get('artifact_git_link') or '',
                    'tags.keys': data.get('tagsKeys') if isinstance(data.get('tagsKeys'), list) else (str(data.get('tagsKeys') or '')).split(','),
                    'glyph_icons': glyph_icons_field,
                    'status_icons': status_icons_field,
                }

                # write new latest.json (single entry) atomically
                tmp_latest = latest_path + '.tmp'
                try:
                    with open(tmp_latest, 'w', encoding='utf-8') as lf:
                        json.dump(new_entry, lf, indent=2, ensure_ascii=False)
                    os.replace(tmp_latest, latest_path)
                except Exception:
                    try:
                        if os.path.exists(tmp_latest):
                            os.remove(tmp_latest)
                    except Exception:
                        pass
            except Exception:
                # non-fatal; don't block the main response
                try:
                    with open('/tmp/broadcast_server_debug.log', 'a', encoding='utf-8') as dbg:
                        dbg.write('Failed to update signals/latest/archive.json\n')
                except Exception:
                    pass

            return self._send(200, {'status': 'ok', 'broadcast_id': broadcast_id})
        except Exception as e:
            # write exception details to a temporary log for debugging
            try:
                with open('/tmp/broadcast_server_error.log', 'a', encoding='utf-8') as errf:
                    import traceback
                    errf.write('---\n')
                    traceback.print_exc(file=errf)
            except Exception:
                pass
            return self._send(500, {'error': 'internal server error', 'details': str(e)})

    def do_GET(self):
        if self.path == '/debug':
            modules, statuses, emoji = load_seeds()
            ok = {
                'modules_loaded': modules is not None,
                'statuses_loaded': statuses is not None,
                'emoji_loaded': emoji is not None,
                'yaml_available': yaml is not None,
                'zoneinfo_available': ZoneInfo is not None,
            }
            return self._send(200, ok)
        return self._send(404, {'error': 'not found'})


if __name__ == '__main__':
    ensure_csv()
    # allow overriding port via environment variable for flexibility
    try:
        env_port = int(os.environ.get('BROADCAST_SERVER_PORT') or 0)
        if env_port:
            PORT = env_port
    except Exception:
        pass

    # prevent bind errors when restarting frequently during development
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), Handler) as httpd:
        print(f"Broadcast server listening at http://{HOST}:{PORT}/api/broadcast")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nShutting down')
            httpd.server_close()
