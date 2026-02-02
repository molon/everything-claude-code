---
name: status
description: View all learned instincts and their confidence levels. Use when reviewing what patterns have been learned, checking instinct health, or understanding current knowledge state.
disable-model-invocation: true
---

# Instinct Status

View all learned instincts and their current state.

## Usage

```
/status                    # Show all instincts
/status --domain testing   # Only show testing instincts
/status --sort confidence  # Sort by confidence level
/status --stale            # Show instincts needing refresh
```

## Implementation

Run the instinct CLI using the plugin root path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/learning-instinct/scripts/instinct.py" status [--filter OPTIONS]
```

Or if `CLAUDE_PLUGIN_ROOT` is not set:

```bash
python3 ~/.claude/skills/learning-instinct/scripts/instinct.py status
```

## What to Do

1. Read all instincts from `~/.claude/homunculus/instincts/`
2. Group by domain, source, confidence
3. Identify stale instincts (low confidence, old, or conflicting)
4. Display summary with actionable insights

## Output Format

```
📊 Instinct Status
==================

Total Instincts: 24

By Source:
  🧠 Personal: 15
  📥 Inherited: 7
  👥 Team: 2

By Domain:
  🔧 workflow: 10
  🧪 testing: 6
  📝 documentation: 4
  🐛 debugging: 4

By Confidence:
  ✅ High (0.8+): 8
  🟡 Medium (0.5-0.8): 12
  ⚠️ Low (<0.5): 4

## Code Style (4 instincts)

### prefer-functional-style
Trigger: when writing new functions
Action: Use functional patterns over classes
Confidence: ████████░░ 80%
Source: session-observation | Last updated: 2025-01-22

### use-path-aliases
Trigger: when importing modules
Action: Use @/ path aliases instead of relative imports
Confidence: ██████░░░░ 60%
Source: repo-analysis (github.com/acme/webapp)

## Stale Instincts (need attention)

⚠️ prefer-typescript-interfaces
   Confidence: 0.35 (below 0.5 threshold)
   Last observed: 2024-12-01 (30+ days ago)
   Action: Consider removing or re-validating

⚠️ use-environment-variables
   Confidence: 0.42 (declining)
   Contradicts: use-config-files
   Action: Manual resolution needed

## Recent Activity

✅ Added: test-driven-development (confidence: 0.75)
✅ Updated: functional-patterns (confidence: 0.65 → 0.80)

---
Total: 9 instincts (4 personal, 5 inherited)
Observer: Running (last analysis: 5 min ago)

Run /evolve to cluster related instincts into skills/agents.
```

## Flags

- `--domain <name>`: Filter by domain
- `--source <personal|inherited|team>`: Filter by source
- `--min-confidence <n>`: Show only instincts above threshold
- `--stale`: Show instincts needing attention
- `--sort <confidence|recent|alpha>`: Sort order
- `--json`: Output as JSON for programmatic use
