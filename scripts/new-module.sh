#!/usr/bin/env bash
set -euo pipefail

echo "🌌 Create a new FourTwenty Analytics constellation star"
echo "This creates a standalone repository scaffold for a new module."
echo

read -rp "Module title (e.g., 'Signal Model'): " TITLE

# Get and validate module key with retry loop
while :; do
  read -rp "Module key (snake_case, e.g., 'signal_model'): " MODULE_KEY
  if [ -z "$MODULE_KEY" ]; then
    echo "❌ Module key cannot be empty. Please try again."
    continue
  fi
  if ! printf "%s" "$MODULE_KEY" | grep -Eq '^[a-z0-9_]+$'; then
    echo "❌ Invalid module key. Use lowercase letters, digits, and underscores only. Please try again."
    continue
  fi
  # Check if module key already exists in seeds/modules.yml
  if [ -f "seeds/modules.yml" ] && grep -q "key: $MODULE_KEY" "seeds/modules.yml"; then
    echo "❌ Module key '$MODULE_KEY' already exists in seeds/modules.yml. Please choose a different key."
    continue
  fi
  break
done

# Get and validate repo name with retry loop
while :; do
  read -rp "Repository name (kebab-case, e.g., 'signal-model'): " REPO_NAME
  if [ -z "$REPO_NAME" ]; then
    echo "❌ Repository name cannot be empty. Please try again."
    continue
  fi
  if ! printf "%s" "$REPO_NAME" | grep -Eq '^[a-z0-9-]+$'; then
    echo "❌ Invalid repo name. Use lowercase letters, digits, and hyphens only. Please try again."
    continue
  fi
  # Check if directory already exists
  if [ -d "$REPO_NAME" ]; then
    echo "❌ Directory '$REPO_NAME' already exists. Please choose a different name."
    continue
  fi
  break
done

read -rp "Short description: " DESC

# Set BASE directory name
BASE="$REPO_NAME"

# Prompt for orbital classification
echo "Available orbital systems:"
if [ -f "seeds/orbits.yml" ]; then
  # Extract orbit IDs and labels for display
  grep -E "^- id:|^  label:" seeds/orbits.yml | sed 'N;s/\n/ /' | sed 's/^- id: /  /' | sed 's/  label: / -> /'
else
  echo "  core -> Core Systems"
  echo "  delivery-insight -> Delivery & Insight" 
  echo "  growth-experiment -> Growth & Experiment"
  echo "  ancillary-operations -> Ancillary Operations"
fi
echo
read -rp "Orbital classification (e.g., 'core'): " ORBIT

# Prompt for status
echo "Available statuses:"
if [ -f "seeds/statuses.yml" ]; then
  grep -E "^- id:|^  label:" seeds/statuses.yml | sed 'N;s/\n/ /' | sed 's/^- id: /  /' | sed 's/  label: / -> /'
else
  echo "  seed -> Seed"
  echo "  sprout -> Sprout"
  echo "  developing -> Developing"  
  echo "  active -> Active"
fi
echo
read -rp "Status (default: 'seed'): " STATUS
STATUS=${STATUS:-seed}

# Prompt for an emoji and validate against seeds/emoji_palette.yml if present
EMOJI=""
if [ -f "seeds/emoji_palette.yml" ]; then
  echo "Available emoji icons (from seeds/emoji_palette.yml):"
  # Parse module_icons section
  awk '/^module_icons:/{flag=1; next} /^[a-z_]+:/{flag=0} flag && /^  / {gsub(/[": ]/, "", $2); print "  " $1 " -> " $2}' seeds/emoji_palette.yml
  echo

  while :; do
    read -rp "Emoji (paste glyph, e.g. 🔘) [enter to skip]: " EMOJI
    # Allow skip
    if [ -z "$EMOJI" ]; then
      break
    fi
    # Check if glyph already exists in palette - inform but allow
    if grep -Fq -- "$EMOJI" seeds/emoji_palette.yml; then
      echo "ℹ️ Note: '$EMOJI' is already defined in seeds/emoji_palette.yml, but proceeding anyway."
    fi
    break
  done
else
  read -rp "Emoji (paste glyph, e.g. 🔘) [enter to skip]: " EMOJI || true
fi

# If a new emoji was provided, add it to seeds/emoji_palette.yml under module_icons
if [ -n "${EMOJI:-}" ]; then
  if [ ! -f "seeds/emoji_palette.yml" ]; then
    mkdir -p seeds
    cat > seeds/emoji_palette.yml <<YML
module_icons:
  ${MODULE_KEY}: "$EMOJI"

status_icons:
  seed: "🌱"
  sprout: "🌿"
  active: "🟢"
  pending: "🟡" 
  error: "🔴"
YML
    echo "✅ Created seeds/emoji_palette.yml and added ${MODULE_KEY} -> $EMOJI"
  else
    # Add to existing module_icons section
    if grep -q '^module_icons:' seeds/emoji_palette.yml; then
      # Find insertion point (before next section or EOF)
      if grep -q '^status_icons:' seeds/emoji_palette.yml; then
        lineno=$(grep -n '^status_icons:' seeds/emoji_palette.yml | head -1 | cut -d: -f1)
        tmp=$(mktemp)
        head -n $((lineno-1)) seeds/emoji_palette.yml > "$tmp"
        printf '  %s: "%s"\n' "${MODULE_KEY}" "$EMOJI" >> "$tmp"
        tail -n +$lineno seeds/emoji_palette.yml >> "$tmp"
        mv "$tmp" seeds/emoji_palette.yml
      else
        printf '  %s: "%s"\n' "${MODULE_KEY}" "$EMOJI" >> seeds/emoji_palette.yml
      fi
    else
      # Prepend module_icons section
      tmp=$(mktemp)
      printf 'module_icons:\n  %s: "%s"\n\n' "${MODULE_KEY}" "$EMOJI" > "$tmp"
      cat seeds/emoji_palette.yml >> "$tmp"
      mv "$tmp" seeds/emoji_palette.yml
    fi
    echo "✅ Added ${MODULE_KEY} -> $EMOJI to seeds/emoji_palette.yml"
  fi
fi

echo
echo "🏗️ Creating constellation star scaffold..."

# Create base directory structure according to seedset.yml
mkdir -p "$BASE"/{seeds,schema,signals,scripts,assets}

# Create main README.md
cat > "$BASE/README.md" <<EOF
# $TITLE

> **$DESC**

## 🌌 Constellation Information

- **Module Key**: \`$MODULE_KEY\`  
- **Repository**: \`$REPO_NAME\`
- **Orbit**: \`$ORBIT\`
- **Status**: \`$STATUS\`
- **Emoji**: $EMOJI

## 🚀 Quick Start

1. **Review seeds/**: Adapt seeded data for this module
2. **Configure schemas/**: Update schema definitions as needed  
3. **Generate signals/**: Create latest.json broadcast file
4. **Run validation**: \`scripts/validate.sh\`

## 📡 Broadcasting

This module produces a \`signals/latest.json\` file conforming to the constellation's broadcast schema. The Signal (📡) aggregates these across all stars.

## 🔗 Constellation Links

- **Hub**: [FourTwenty Analytics](https://github.com/zbreeden/FourTwentyAnalytics)
- **Archive**: Glossary, tags, and canonical definitions
- **Signal**: Cross-constellation broadcasting and telemetry

---

*This star is part of the FourTwenty Analytics constellation - a modular analytics sandbox where each repository is a specialized "model" within an orbital system.*
EOF

# Create index.html for GitHub Pages
cat > "$BASE/index.html" <<EOF
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$TITLE - FourTwenty Analytics</title>
  <meta name="description" content="$DESC">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='0.9em' font-size='90'>$EMOJI</text></svg>">
</head>
<body>
  <header>
    <h1>$EMOJI $TITLE</h1>
    <p>$DESC</p>
    <nav>
      <a href="https://github.com/zbreeden/$REPO_NAME">Repository</a> |
      <a href="https://github.com/zbreeden/FourTwentyAnalytics">Hub</a>
    </nav>
  </header>
  
  <main>
    <section>
      <h2>🌌 Constellation Info</h2>
      <ul>
        <li><strong>Orbit</strong>: $ORBIT</li>
        <li><strong>Status</strong>: $STATUS</li>  
        <li><strong>Module Key</strong>: <code>$MODULE_KEY</code></li>
      </ul>
    </section>
    
    <section>
      <h2>📡 Latest Signal</h2>
      <p><em>Broadcast data will appear here when signals/latest.json is generated.</em></p>
    </section>
  </main>
  
  <footer>
    <p>Part of the <a href="https://zbreeden.github.io/FourTwentyAnalytics/">FourTwenty Analytics</a> constellation</p>
  </footer>
</body>
</html>
EOF

# Copy seedset files according to seeds/seedset.yml
echo "📦 Distributing seedset files..."
if [ -f "seeds/seedset.yml" ]; then
  # Read files list from seedset.yml and copy them
  grep -A 100 "^files:" seeds/seedset.yml | grep "^  - " | sed 's/^  - //' | while read -r file_path; do
    if [ -f "$file_path" ]; then
      target_dir="$BASE/$(dirname "$file_path")"
      mkdir -p "$target_dir"
      cp "$file_path" "$BASE/$file_path"
      echo "  ✓ $file_path"
    else
      echo "  ⚠️ Missing: $file_path"
    fi
  done
else
  echo "  ⚠️ No seeds/seedset.yml found, copying seeds manually..."
  if [ -d "seeds" ]; then
    cp seeds/*.yml "$BASE/seeds/" 2>/dev/null || true
    cp seeds/*.json "$BASE/seeds/" 2>/dev/null || true
  fi
  if [ -d "schemas" ]; then
    cp schemas/*.yml "$BASE/schema/" 2>/dev/null || true
  fi
fi

# Create initial signals/latest.json
cat > "$BASE/signals/latest.json" <<EOF
{
  "id": "$(date -u +%Y%m%dT%H%M%SZ)-${REPO_NAME}-genesis",
  "ts_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "date": "$(date -u +%Y-%m-%d)",
  "module": "$TITLE",
  "repo": "$REPO_NAME", 
  "title": "New constellation star initialized",
  "summary": "Generated module scaffold with seedset distribution and basic broadcast structure.",
  "tags": ["genesis", "scaffold", "module", "$ORBIT"],
  "rating": "normal",
  "origin": {
    "name": "$TITLE",
    "url": "https://zbreeden.github.io/$REPO_NAME/",
    "emoji": "$EMOJI"
  },
  "links": {
    "readme": "https://github.com/zbreeden/$REPO_NAME#readme",
    "page": "https://zbreeden.github.io/$REPO_NAME/",
    "data": "https://github.com/zbreeden/$REPO_NAME/tree/main/signals",
    "runbook": "https://github.com/zbreeden/$REPO_NAME/blob/main/RUNBOOK.md"
  },
  "payload": {
    "orbit": "$ORBIT",
    "status": "$STATUS", 
    "module_key": "$MODULE_KEY",
    "notes": "Initial scaffold created by new-module.sh script. Ready for customization and development."
  },
  "checksum": "",
  "version": "1.0.0"
}
EOF

# Create validation script
cat > "$BASE/scripts/validate.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

MODULE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "🔍 Validating module: $(basename "$MODULE_DIR")"

# Check required files exist
echo "📁 Checking required files..."
required_files=(
  "README.md"
  "index.html"
  "signals/latest.json"
  "seeds/modules.yml"
  "schema/latest.schema.yml"
)

for file in "${required_files[@]}"; do
  if [ -f "$MODULE_DIR/$file" ]; then
    echo "  ✓ $file"
  else
    echo "  ❌ Missing: $file"
  fi
done

# Validate signals/latest.json structure (basic check)
echo "📡 Validating signal structure..."
if [ -f "$MODULE_DIR/signals/latest.json" ]; then
  if command -v jq >/dev/null 2>&1; then
    if jq empty "$MODULE_DIR/signals/latest.json" 2>/dev/null; then
      echo "  ✓ signals/latest.json is valid JSON"
      # Check required fields
      required_fields=("id" "ts_utc" "module" "repo" "title" "summary" "rating" "origin" "links" "payload")
      for field in "${required_fields[@]}"; do
        if jq -e ".$field" "$MODULE_DIR/signals/latest.json" >/dev/null 2>&1; then
          echo "  ✓ Field: $field"
        else
          echo "  ❌ Missing field: $field"
        fi
      done
    else
      echo "  ❌ signals/latest.json is invalid JSON"
    fi
  else
    echo "  ⚠️ jq not available, skipping JSON validation"
  fi
else
  echo "  ❌ signals/latest.json not found"
fi

echo "✅ Validation complete"
EOF
chmod +x "$BASE/scripts/validate.sh"

# Create constellation integration script
cat > "$BASE/scripts/update-hub.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail

echo "📡 Updating hub constellation with this module..."

MODULE_KEY="$MODULE_KEY"
REPO_NAME="$REPO_NAME"
HUB_PATH="../FourTwentyAnalytics"

if [ ! -d "\$HUB_PATH" ]; then
  echo "❌ Hub not found at \$HUB_PATH"
  echo "   Make sure FourTwentyAnalytics is cloned alongside this repo"
  exit 1
fi

# Add entry to hub's seeds/modules.yml if not already present
if ! grep -q "key: \$MODULE_KEY" "\$HUB_PATH/seeds/modules.yml"; then
  echo "🌱 Adding module to hub seeds/modules.yml..."
  cat >> "\$HUB_PATH/seeds/modules.yml" <<MODULE
  
- key: $MODULE_KEY
  label: "$TITLE"
  repo: "$REPO_NAME"
  owner: "zbreeden"
  emoji: "$EMOJI"
  orbit: $ORBIT
  status: $STATUS
  tags: [$(echo "$DESC" | tr ' ' '\n' | head -3 | tr '\n' ',' | sed 's/,$//' | tr '[:upper:]' '[:lower:]')]
  description: "$DESC"
  repo_url: https://github.com/zbreeden/$REPO_NAME
  pages_url: https://zbreeden.github.io/$REPO_NAME/
  owners: [zach]
MODULE
  echo "  ✅ Module added to hub constellation"
else
  echo "  ℹ️ Module already exists in hub constellation"
fi

echo "🚀 Hub integration complete!"
echo "   Don't forget to commit changes in \$HUB_PATH"
EOF
chmod +x "$BASE/scripts/update-hub.sh"

# Add .gitkeep files to preserve directory structure
for d in "$BASE/seeds" "$BASE/schema" "$BASE/signals" "$BASE/assets"; do
  if [ ! "$(ls -A "$d" 2>/dev/null)" ]; then
    touch "$d/.gitkeep"
  fi
done

echo
echo "🌟 Constellation star created successfully!"
echo "   📁 Location: $BASE/"
echo "   🔑 Module Key: $MODULE_KEY"
echo "   📦 Repository: $REPO_NAME"
echo "   🛸 Orbit: $ORBIT"
echo "   📊 Status: $STATUS"
if [ -n "${EMOJI:-}" ]; then
  echo "   $EMOJI Emoji: $EMOJI"
fi
echo
echo "📋 Next steps:"
echo "   1. cd $BASE"
echo "   2. Review and customize files in seeds/ and schema/"
echo "   3. Run ./scripts/validate.sh to check structure"
echo "   4. Run ./scripts/update-hub.sh to register with constellation"
echo "   5. Initialize git repository and push to GitHub"
echo
echo "🔗 Part of the FourTwenty Analytics constellation"
