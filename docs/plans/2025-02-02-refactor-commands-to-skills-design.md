# Refactor Commands to Skills - Design Document

**Date:** 2025-02-02
**Author:** AI Assistant
**Status:** Design Complete

## Overview

Refactor the instinct plugin to convert commands into skills while preserving command entry points. This enables better modularity and follows Claude Code plugin best practices.

## Objectives

1. Remove skill-create command and its git analysis functionality
2. Add skill creation logic to evolve command/skill
3. Convert evolve, import, export, status commands to skills
4. Preserve command entry points that delegate to skills
5. Create install-opencode skill for easy opencode CLI installation

## Changes

### Part 1: Remove skill-create

**Files to Delete:**
- `commands/skill-create.md`

**Reasoning:** skill-create is redundant - skill creation should be handled through evolve with proper tool detection.

### Part 2: Add Skill Creation Logic to evolve

**File to Modify:** `skills/evolve/SKILL.md` (new file)

**Add logic to detect and use skill creation tools:**

1. Check for `superpowers:writing-skills`
   - Search: `~/.claude/plugins/cache/*/skills/writing-skills/SKILL.md`
   - If found: Use Skill tool to invoke (TDD-based, higher priority)

2. Fallback to `skill-creator`
   - Search: `~/.claude/plugins/cache/*/skills/skill-creator/SKILL.md`
   - If found: Invoke and follow process

3. Error if neither available
   - Report error with installation instructions
   - Stop execution

### Part 3: Convert Commands to Skills

**New Directory Structure:**
```
skills/
├── learning-instinct/    # existing
├── evolve/               # new
│   └── SKILL.md
├── import/               # new
│   └── SKILL.md
├── export/               # new
│   └── SKILL.md
├── status/               # new
│   └── SKILL.md
└── install-opencode/     # new
    └── SKILL.md

commands/
├── evolve.md             # simplified
├── import.md             # simplified
├── export.md             # simplified
└── status.md             # simplified
```

**Skill File Format:**
```markdown
---
name: {skill-name}
description: {description}
disable-model-invocation: true
---

# {Title}

[Content from original command file, adapted for skill format]
```

**Command File Format (simplified):**
```markdown
---
name: {command-name}
description: {description}
command: true
---

Invoke the instinct:{skill-name} skill and follow it exactly as presented to you.
```

**Conversions:**

| Original | New Skill | New Command |
|----------|-----------|-------------|
| `commands/evolve.md` | `skills/evolve/SKILL.md` | `commands/evolve.md` (simplified) |
| `commands/import.md` | `skills/import/SKILL.md` | `commands/import.md` (simplified) |
| `commands/export.md` | `skills/export/SKILL.md` | `commands/export.md` (simplified) |
| `commands/status.md` | `skills/status/SKILL.md` | `commands/status.md` (simplified) |

### Part 4: Create install-opencode Skill

**File:** `skills/install-opencode/SKILL.md`

**Functionality:**
1. Check if opencode is already installed
2. If not installed, install opencode CLI
3. Verify installation with test command

**Verification Command:**
```bash
opencode run "what is 2+2" --model opencode/big-pickle
```

**Expected Output:** Should show "4" as the answer.

## Implementation Notes

1. **plugin.json Update:** Add new skills to the skills array
2. **Content Adaptation:** When converting commands to skills, adapt content for skill format (not command format)
3. **disable-model-invocation:** All new skills use this to prevent model from summarizing/rewriting

## Success Criteria

- [ ] skill-create command and generated files removed
- [ ] evolve skill has skill creation tool detection logic
- [ ] All 4 commands converted to skills with `disable-model-invocation: true`
- [ ] Command files simplified to delegate to skills
- [ ] install-opencode skill created and working
- [ ] plugin.json updated with new skills
- [ ] All changes tested and verified

## References

- Existing commands: `commands/*.md`
- Plugin manifest: `.claude-plugin/plugin.json`
- Learning instinct skill: `skills/learning-instinct/SKILL.md`
