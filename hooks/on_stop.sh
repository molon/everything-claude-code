#!/bin/bash
# Instinct Learning v2 - Stop Hook
# Updates session count and archives observations

set -e

STATE="${HOME}/.claude/homunculus/identity.json"
OBSERVATIONS_FILE="${HOME}/.claude/homunculus/observations.jsonl"
ARCHIVE_DIR="${HOME}/.claude/homunculus/observations.archive"

# Ensure directories exist
mkdir -p "$(dirname "$STATE")"
mkdir -p "$ARCHIVE_DIR"

# Update session count
if [ -f "$STATE" ] && command -v jq >/dev/null 2>&1; then
  COUNT=$(jq -r ".journey.sessionCount // 0" "$STATE")
  TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  TMP=$(mktemp)

  jq --arg c "$((COUNT+1))" --arg t "$TIMESTAMP" \
    '.journey.sessionCount = ($c|tonumber) | .journey.lastSession = $t' \
    "$STATE" > "$TMP" && mv "$TMP" "$STATE"
fi

# Archive observations if file exists and is not empty
if [ -f "$OBSERVATIONS_FILE" ] && [ -s "$OBSERVATIONS_FILE" ]; then
  mv "$OBSERVATIONS_FILE" "$ARCHIVE_DIR/observations-$(date +%Y%m%d-%H%M%S).jsonl"
  touch "$OBSERVATIONS_FILE"
fi

exit 0
