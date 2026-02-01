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
    "PreToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh pre"
      }]
    }],
    "PostToolUse": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh post"
      }]
    }]
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `/skill-create` | Analyze git history to generate skills |
| `/instinct-status` | View learned instincts with confidence |
| `/instinct-import` | Import instincts from file |
| `/instinct-export` | Export your instincts |
| `/evolve` | Cluster instincts into skills/commands |

## How It Works

Session activity → Hooks capture → Observer agent detects patterns → Creates instincts → Evolve into reusable knowledge

See `skills/continuous-learning-v2/SKILL.md` for full documentation.

## License

MIT
