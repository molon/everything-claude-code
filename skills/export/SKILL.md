---
name: export
description: Export learned instincts to share with team or backup. Use when sharing instincts with teammates, creating backups, or contributing to community collections.
disable-model-invocation: true
---

# Export Instincts

Export learned instincts for:
- Sharing with teammates
- Creating backups
- Contributing to community collections
- Migrating to new machines

## Usage

```
/export                           # Export all personal instincts
/export --domain testing          # Export only testing instincts
/export --min-confidence 0.7      # Only export high-confidence instincts
/export --output team-instincts.yaml
```

## Implementation

Run the instinct CLI using the plugin root path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/learning-instinct/scripts/instinct-cli.py" export [--output FILE] [--domain DOMAIN] [--min-confidence N]
```

Or if `CLAUDE_PLUGIN_ROOT` is not set:

```bash
python3 ~/.claude/skills/learning-instinct/scripts/instinct-cli.py export
```

## What to Do

1. Read instincts from `~/.claude/homunculus/instincts/personal/`
2. Filter based on flags
3. Strip sensitive information:
   - Remove session IDs
   - Remove file paths (keep only patterns)
   - Remove timestamps older than "last week"
4. Generate export file

## Output Format

Creates a YAML file:

```yaml
# Instincts Export
# Generated: 2025-01-22
# Source: personal
# Count: 12 instincts

version: "2.0"
exported_by: "learning-instinct"
export_date: "2025-01-22T10:30:00Z"

instincts:
  - id: prefer-functional-style
    trigger: "when writing new functions"
    action: "Use functional patterns over classes"
    confidence: 0.8
    domain: code-style
    observations: 8

  - id: test-first-workflow
    trigger: "when adding new functionality"
    action: "Write test first, then implementation"
    confidence: 0.9
    domain: testing
    observations: 12

  - id: grep-before-edit
    trigger: "when modifying code"
    action: "Search with Grep, confirm with Read, then Edit"
    confidence: 0.7
    domain: workflow
    observations: 6
```

## Privacy Considerations

Exports include:
- ✅ Trigger patterns
- ✅ Actions
- ✅ Confidence scores
- ✅ Domains
- ✅ Observation counts

Exports do NOT include:
- ❌ Actual code snippets
- ❌ File paths
- ❌ Session transcripts
- ❌ Personal identifiers

## Flags

- `--domain <name>`: Export only specified domain
- `--min-confidence <n>`: Minimum confidence threshold (default: 0.3)
- `--output <file>`: Output file path (default: instincts-export-YYYYMMDD.yaml)
- `--format <yaml|json|md>`: Output format (default: yaml)
- `--include-evidence`: Include evidence text (default: excluded)

## Output

After export:
```
✅ Export complete!

Exported 12 instincts to: instincts-export-20250122.yaml

Breakdown:
  - Personal instincts: 8
  - High confidence (0.7+): 9
  - Testing domain: 3

Ready to share with teammates or project documentation.
```
