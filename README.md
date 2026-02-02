# Instinct

Instinct-based learning system for Claude Code - observes sessions, creates atomic behaviors with confidence scoring, and evolves them into reusable knowledge.

## Quick Start

### Install

```bash
/plugin marketplace add yourusername/instinct
/plugin install instinct@instinct
```

### Enable Hooks

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/observe.sh pre"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/observe.sh post"
          }
        ]
      }
    ]
  }
}
```

## Commands

| Command   | Description                            |
| --------- | -------------------------------------- |
| `/init`   | Initialize the learning system         |
| `/status` | View learned instincts with confidence |
| `/import` | Import instincts from file             |
| `/export` | Export your instincts                  |
| `/evolve` | Cluster instincts into skills/commands |

## Skills

| Skill            | When It Activates                         |
| ---------------- | ----------------------------------------- |
| `session-memory` | Session start — loads context             |
| `instinct-apply` | During work — surfaces relevant instincts |

## How It Works

Session activity → Hooks capture → Observer agent detects patterns → Creates instincts → Evolve into reusable knowledge

See the individual skill documentation for details on each command.

## License

MIT
