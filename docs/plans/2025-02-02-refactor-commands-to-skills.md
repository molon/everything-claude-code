# Refactor Commands to Skills Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Convert commands to skills structure while preserving command entry points, add skill creation logic to evolve, and create install-opencode skill.

**Architecture:** Convert existing commands into modular skills with `disable-model-invocation: true`, simplify command files to delegate to skills using "Invoke the instinct:xxx skill" pattern. Add skill creation tool detection to evolve for intelligent fallback between superpowers:writing-skills and skill-creator.

**Tech Stack:** Claude Code Plugin system, YAML frontmatter, Markdown, Shell scripting

---

## Task 1: Remove skill-create Command

**Files:**
- Delete: `commands/skill-create.md`

**Step 1: Delete skill-create command**

Run:
```bash
rm commands/skill-create.md
```

Expected: File removed, no error

**Step 2: Verify deletion**

Run:
```bash
ls commands/
git status
```

Expected: skill-create.md not in commands/

**Step 3: Commit**

```bash
git add commands/skill-create.md
git commit -m "refactor: remove skill-create command"
```

---

## Task 2: Create evolve Skill

**Files:**
- Create: `skills/evolve/SKILL.md`

**Step 1: Create evolve skill directory**

Run:
```bash
mkdir -p skills/evolve
```

**Step 2: Write evolve SKILL.md**

Create `skills/evolve/SKILL.md`:

```markdown
---
name: evolve
description: Cluster related instincts into skills, commands, or agents. Use when instincts need to be organized into higher-level structures, when multiple instincts cluster around a domain, or when creating reusable knowledge from observed patterns.
disable-model-invocation: true
---

# Evolve Instincts

Analyzes instincts and clusters related ones into higher-level structures:
- **Commands**: When instincts describe user-invoked actions
- **Skills**: When instincts describe auto-triggered behaviors
- **Agents**: When instincts describe complex, multi-step processes

## Usage

```
/evolve                    # Analyze all instincts and suggest evolutions
/evolve --domain testing   # Only evolve instincts in testing domain
/evolve --dry-run          # Show what would be created without creating
/evolve --threshold 5      # Require 5+ related instincts to cluster
```

## Implementation

Run the instinct CLI using the plugin root path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/learning-instinct/scripts/instinct-cli.py" evolve [--generate]
```

Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation):

```bash
python3 ~/.claude/skills/learning-instinct/scripts/instinct-cli.py evolve [--generate]
```

## Evolution Rules

### → Command (User-Invoked)
When instincts describe actions a user would explicitly request:
- Multiple instincts about "when user asks to..."
- Instincts with triggers like "when creating a new X"
- Instincts that follow a repeatable sequence

Example:
- `new-table-step1`: "when adding a database table, create migration"
- `new-table-step2`: "when adding a database table, update schema"
- `new-table-step3`: "when adding a database table, regenerate types"

→ Creates: `/new-table` command

### → Skill (Auto-Triggered)
When instincts describe behaviors that should happen automatically:
- Pattern-matching triggers
- Error handling responses
- Code style enforcement

Example:
- `prefer-functional`: "when writing functions, prefer functional style"
- `use-immutable`: "when modifying state, use immutable patterns"
- `avoid-classes`: "when designing modules, avoid class-based design"

→ Creates: `functional-patterns` skill

### → Agent (Needs Depth/Isolation)
When instincts describe complex, multi-step processes that benefit from isolation:
- Debugging workflows
- Refactoring sequences
- Research tasks

Example:
- `debug-step1`: "when debugging, first check logs"
- `debug-step2`: "when debugging, isolate the failing component"
- `debug-step3`: "when debugging, create minimal reproduction"
- `debug-step4`: "when debugging, verify fix with test"

→ Creates: `debugger` agent

## What to Do

1. Read all instincts from `~/.claude/homunculus/instincts/`
2. Group instincts by:
   - Domain similarity
   - Trigger pattern overlap
   - Action sequence relationship
3. For each cluster of 3+ related instincts:
   - Determine evolution type (command/skill/agent)
   - Generate the appropriate file
   - Save to `~/.claude/homunculus/evolved/{commands,skills,agents}/`
4. Link evolved structure back to source instincts

## Output Format

```
🧬 Evolve Analysis
==================

Found 3 clusters ready for evolution:

## Cluster 1: Database Migration Workflow
Instincts: new-table-migration, update-schema, regenerate-types
Type: Command
Confidence: 85% (based on 12 observations)

Would create: /new-table command
Files:
  - ~/.claude/homunculus/evolved/commands/new-table.md

## Cluster 2: Functional Code Style
Instincts: prefer-functional, use-immutable, avoid-classes, pure-functions
Type: Skill
Confidence: 78% (based on 8 observations)

Would create: functional-patterns skill
Files:
  - ~/.claude/homunculus/evolved/skills/functional-patterns.md

## Cluster 3: Debugging Process
Instincts: debug-check-logs, debug-isolate, debug-reproduce, debug-verify
Type: Agent
Confidence: 72% (based on 6 observations)

Would create: debugger agent
Files:
  - ~/.claude/homunculus/evolved/agents/debugger.md

---
Run `/evolve --execute` to create these files.
```

## Flags

- `--execute`: Actually create the evolved structures (default is preview)
- `--dry-run`: Preview without creating
- `--domain <name>`: Only evolve instincts in specified domain
- `--threshold <n>`: Minimum instincts required to form cluster (default: 3)
- `--type <command|skill|agent>`: Only create specified type

## Skill Creation

When evolving instincts into a new skill:

1. **Check for superpowers:writing-skills**
   ```bash
   ls ~/.claude/plugins/cache/*/skills/writing-skills/SKILL.md 2>/dev/null
   ```
   - If found: Use Skill tool to invoke it and follow TDD-based process
   - Priority: **Higher** (TDD approach, more rigorous)

2. **Fallback to skill-creator**
   ```bash
   ls ~/.claude/plugins/cache/*/skills/skill-creator/SKILL.md 2>/dev/null
   ```
   - If found: Invoke and follow its creation process
   - Priority: **Lower** (standard skill creation)

3. **Error if neither available**
   ```
   ❌ Error: No skill creation tool found

   Please install one of:
   - superpowers:writing-skills (recommended, TDD-based)
   - skill-creator (standard)

   Installation instructions:
   https://github.com/obra/superpowers
   https://github.com/anthropics/skills
   ```
   - Stop execution and report error to user

## Generated File Format

### Command
```markdown
---
name: new-table
description: Create a new database table with migration, schema update, and type generation
command: /new-table
evolved_from:
  - new-table-migration
  - update-schema
  - regenerate-types
---

# New Table Command

[Generated content based on clustered instincts]
```

### Skill
```markdown
---
name: functional-patterns
description: Enforce functional programming patterns
evolved_from:
  - prefer-functional
  - use-immutable
  - avoid-classes
---

# Functional Patterns Skill

[Generated content based on clustered instincts]
```

### Agent
```markdown
---
name: debugger
description: Systematic debugging agent
model: sonnet
evolved_from:
  - debug-check-logs
  - debug-isolate
  - debug-reproduce
---

# Debugger Agent

[Generated content based on clustered instincts]
```
```

**Step 3: Verify file created**

Run:
```bash
cat skills/evolve/SKILL.md | head -20
```

Expected: YAML frontmatter with name, description, disable-model-invocation

**Step 4: Commit**

```bash
git add skills/evolve/SKILL.md
git commit -m "feat: create evolve skill with skill creation tool detection"
```

---

## Task 3: Simplify evolve Command

**Files:**
- Modify: `commands/evolve.md`

**Step 1: Backup original command**

Run:
```bash
cp commands/evolve.md commands/evolve.md.bak
```

**Step 2: Replace with simplified content**

Replace entire `commands/evolve.md` with:

```markdown
---
name: evolve
description: Cluster related instincts into skills, commands, or agents
command: true
---

Invoke the instinct:evolve skill and follow it exactly as presented to you.
```

**Step 3: Verify change**

Run:
```bash
cat commands/evolve.md
```

Expected: Only 3 lines of YAML frontmatter + 1 invocation line

**Step 4: Remove backup**

Run:
```bash
rm commands/evolve.md.bak
```

**Step 5: Commit**

```bash
git add commands/evolve.md
git commit -m "refactor: simplify evolve command to delegate to skill"
```

---

## Task 4: Create import Skill

**Files:**
- Create: `skills/import/SKILL.md`

**Step 1: Read original command for reference**

Run:
```bash
cat commands/import.md
```

**Step 2: Create import skill directory**

Run:
```bash
mkdir -p skills/import
```

**Step 3: Write import SKILL.md**

Create `skills/import/SKILL.md`:

```markdown
---
name: import
description: Import instincts from teammates, Skill Creator, or other sources. Use when loading instincts from external files, URLs, or community collections.
disable-model-invocation: true
---

# Import Instincts

Import instincts from:
- Teammates' exports
- Skill Creator (repo analysis)
- Community collections
- Previous machine backups

## Usage

```
/import team-instincts.yaml
/import https://github.com/org/repo/instincts.yaml
/import --from-skill-creator acme/webapp
```

## Implementation

Run the instinct CLI using the plugin root path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/learning-instinct/scripts/instinct-cli.py" import <file-or-url> [--dry-run] [--force] [--min-confidence 0.7]
```

Or if `CLAUDE_PLUGIN_ROOT` is not set (manual installation):

```bash
python3 ~/.claude/skills/learning-instinct/scripts/instinct-cli.py import <file-or-url>
```

## What to Do

1. Fetch the instinct file (local path or URL)
2. Parse and validate the format
3. Check for duplicates with existing instincts
4. Merge or add new instincts
5. Save to `~/.claude/homunculus/instincts/inherited/`

## Import Process

```
📥 Importing instincts from: team-instincts.yaml
================================================

Found 12 instincts to import.

Analyzing conflicts...

## New Instincts (8)
These will be added:
  ✓ use-zod-validation (confidence: 0.7)
  ✓ prefer-named-exports (confidence: 0.65)
  ✓ test-async-functions (confidence: 0.8)
  ...

## Duplicate Instincts (3)
Already have similar instincts:
  ⚠️ prefer-functional-style
     Local: 0.8 confidence, 12 observations
     Import: 0.7 confidence
     → Keep local (higher confidence)

  ⚠️ test-first-workflow
     Local: 0.75 confidence
     Import: 0.9 confidence
     → Update to import (higher confidence)

## Conflicting Instincts (1)
These contradict local instincts:
  ❌ use-classes-for-services
     Conflicts with: avoid-classes
     → Skip (requires manual resolution)

---
Import 8 new, update 1, skip 3?
```

## Merge Strategies

### For Duplicates
When importing an instinct that matches an existing one:
- **Higher confidence wins**: Keep the one with higher confidence
- **Merge evidence**: Combine observation counts
- **Update timestamp**: Mark as recently validated

### For Conflicts
When importing an instinct that contradicts an existing one:
- **Skip by default**: Don't import conflicting instincts
- **Flag for review**: Mark both as needing attention
- **Manual resolution**: User decides which to keep

## Source Tracking

Imported instincts are marked with:
```yaml
source: "inherited"
imported_from: "team-instincts.yaml"
imported_at: "2025-01-22T10:30:00Z"
original_source: "session-observation"  # or "repo-analysis"
```

## Skill Creator Integration

When importing from Skill Creator:

```
/import --from-skill-creator acme/webapp
```

This fetches instincts generated from repo analysis:
- Source: `repo-analysis`
- Higher initial confidence (0.7+)
- Linked to source repository

## Flags

- `--dry-run`: Preview without importing
- `--force`: Import even if conflicts exist
- `--merge-strategy <higher|local|import>`: How to handle duplicates
- `--from-skill-creator <owner/repo>`: Import from Skill Creator analysis
- `--min-confidence <n>`: Only import instincts above threshold

## Output

After import:
```
✅ Import complete!

Added: 8 instincts
Updated: 1 instinct
Skipped: 3 instincts (2 duplicates, 1 conflict)

New instincts saved to: ~/.claude/homunculus/instincts/inherited/

Run /status to see all instincts.
```
```

**Step 4: Verify file created**

Run:
```bash
cat skills/import/SKILL.md | head -10
```

**Step 5: Commit**

```bash
git add skills/import/SKILL.md
git commit -m "feat: create import skill"
```

---

## Task 5: Simplify import Command

**Files:**
- Modify: `commands/import.md`

**Step 1: Replace with simplified content**

Replace entire `commands/import.md` with:

```markdown
---
name: import
description: Import instincts from teammates, Skill Creator, or other sources
command: true
---

Invoke the instinct:import skill and follow it exactly as presented to you.
```

**Step 2: Verify change**

Run:
```bash
cat commands/import.md
```

**Step 3: Commit**

```bash
git add commands/import.md
git commit -m "refactor: simplify import command to delegate to skill"
```

---

## Task 6: Create export Skill

**Files:**
- Create: `skills/export/SKILL.md`

**Step 1: Read original command**

Run:
```bash
cat commands/export.md
```

**Step 2: Create export skill directory and file**

Run:
```bash
mkdir -p skills/export
```

Create `skills/export/SKILL.md`:

```markdown
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
/export                    # Export all instincts to YAML
/export --output my-instincts.yaml
/export --domain testing   # Only export testing instincts
/export --min-confidence 0.7
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

1. Read all instincts from `~/.claude/homunculus/instincts/`
2. Filter by specified criteria (domain, confidence)
3. Validate format and relationships
4. Write to YAML file with metadata

## Export Format

```yaml
---
exported_at: "2025-01-22T10:30:00Z"
exported_by: "username"
plugin_version: "1.0.0"
---

instincts:
  - id: prefer-grep-before-edit
    trigger: "when searching for code to modify"
    confidence: 0.65
    domain: "workflow"
    source: "session-observation"
    created_at: "2025-01-15T08:00:00Z"
    evidence:
      - "Observed 8 times in session abc123"
      - "Pattern: Grep → Read → Edit sequence"
    action: |
      Always use Grep to find the exact location before using Edit.

  - id: test-before-commit
    trigger: "before committing code changes"
    confidence: 0.8
    domain: "workflow"
    source: "session-observation"
    created_at: "2025-01-10T14:00:00Z"
    evidence:
      - "Observed 15 times across multiple sessions"
    action: |
      Always run tests before committing to ensure no regressions.
```

## Output

After export:
```
✅ Export complete!

Exported 12 instincts to: my-instincts.yaml

Breakdown:
  - Personal instincts: 8
  - Inherited instincts: 3
  - Team instincts: 1

Confidence distribution:
  - High (0.8+): 5
  - Medium (0.5-0.8): 6
  - Low (<0.5): 1

Share with: teammates, project documentation, or community
```

## Flags

- `--output <file>`: Output file path (default: instincts-export.yaml)
- `--domain <name>`: Only export instincts in specified domain
- `--source <personal|inherited|team>`: Filter by source
- `--min-confidence <n>`: Only export instincts above threshold
- `--format <yaml|json>`: Output format (default: yaml)
```

**Step 3: Commit**

```bash
git add skills/export/SKILL.md
git commit -m "feat: create export skill"
```

---

## Task 7: Simplify export Command

**Files:**
- Modify: `commands/export.md`

**Step 1: Replace with simplified content**

Replace `commands/export.md` with:

```markdown
---
name: export
description: Export learned instincts to share with team or backup
command: true
---

Invoke the instinct:export skill and follow it exactly as presented to you.
```

**Step 2: Commit**

```bash
git add commands/export.md
git commit -m "refactor: simplify export command to delegate to skill"
```

---

## Task 8: Create status Skill

**Files:**
- Create: `skills/status/SKILL.md`

**Step 1: Read original command**

Run:
```bash
cat commands/status.md
```

**Step 2: Create status skill directory and file**

Run:
```bash
mkdir -p skills/status
```

Create `skills/status/SKILL.md`:

```markdown
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
python3 "${CLAUDE_PLUGIN_ROOT}/skills/learning-instinct/scripts/instinct-cli.py" status [--filter OPTIONS]
```

Or if `CLAUDE_PLUGIN_ROOT` is not set:

```bash
python3 ~/.claude/skills/learning-instinct/scripts/instinct-cli.py status
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

Run /evolve to cluster related instincts into skills/agents.
```

## Flags

- `--domain <name>`: Filter by domain
- `--source <personal|inherited|team>`: Filter by source
- `--min-confidence <n>`: Show only instincts above threshold
- `--stale`: Show instincts needing attention
- `--sort <confidence|recent|alpha>`: Sort order
```

**Step 3: Commit**

```bash
git add skills/status/SKILL.md
git commit -m "feat: create status skill"
```

---

## Task 9: Simplify status Command

**Files:**
- Modify: `commands/status.md`

**Step 1: Replace with simplified content**

Replace `commands/status.md` with:

```markdown
---
name: status
description: View all learned instincts and their confidence levels
command: true
---

Invoke the instinct:status skill and follow it exactly as presented to you.
```

**Step 2: Commit**

```bash
git add commands/status.md
git commit -m "refactor: simplify status command to delegate to skill"
```

---

## Task 10: Create install-opencode Skill

**Files:**
- Create: `skills/install-opencode/SKILL.md`

**Step 1: Create skill directory**

Run:
```bash
mkdir -p skills/install-opencode
```

**Step 2: Write install-opencode SKILL.md**

Create `skills/install-opencode/SKILL.md`:

```markdown
---
name: install-opencode
description: Install opencode CLI if not already installed and verify installation. Use when user needs opencode CLI functionality for code analysis, generation, or other tasks.
disable-model-invocation: true
---

# Install OpenCode

Installs the opencode CLI tool if not already present on the system.

## Installation

OpenCode is typically installed via npm:

```bash
npm install -g opencode
```

Alternative installation methods:

**Via yarn:**
```bash
yarn global add opencode
```

**Via pnpm:**
```bash
pnpm add -g opencode
```

## Verification

After installation, verify with a simple test:

```bash
opencode run "what is 2+2" --model opencode/big-pickle
```

**Expected output:** The answer should be "4" or equivalent.

If verification succeeds, opencode is ready to use.

## Check if Already Installed

Before attempting installation:

```bash
which opencode
opencode --version
```

- If `opencode` is found and version shows: Already installed, skip installation
- If command not found: Proceed with installation

## Troubleshooting

**Permission denied (npm global install):**
```bash
# Use sudo (not recommended)
sudo npm install -g opencode

# Or fix npm permissions (recommended)
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
npm install -g opencode
```

**Command not found after install:**
Check npm global bin directory and add to PATH:
```bash
npm config get prefix
# Add <prefix>/bin to your PATH in ~/.zshrc or ~/.bashrc
```

## Usage Examples

Once installed, opencode can be used for various tasks:

```bash
# Basic code generation
opencode run "write a function to reverse a string"

# Specific model
opencode run "explain this code" --model opencode/big-pickle

# File input
opencode run "review this code" --input myfile.js
```
```

**Step 3: Verify file created**

Run:
```bash
cat skills/install-opencode/SKILL.md | head -20
```

**Step 4: Commit**

```bash
git add skills/install-opencode/SKILL.md
git commit -m "feat: create install-opencode skill"
```

---

## Task 11: Update plugin.json

**Files:**
- Modify: `.claude-plugin/plugin.json`

**Step 1: Read current plugin.json**

Run:
```bash
cat .claude-plugin/plugin.json
```

**Step 2: Update skills array**

The current plugin.json has:
```json
{
  "skills": ["./skills/learning-instinct/"],
  ...
}
```

Update to:
```json
{
  "skills": [
    "./skills/learning-instinct/",
    "./skills/evolve/",
    "./skills/import/",
    "./skills/export/",
    "./skills/status/",
    "./skills/install-opencode/"
  ],
  ...
}
```

**Step 3: Verify JSON is valid**

Run:
```bash
python3 -m json.tool .claude-plugin/plugin.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

Expected: "Valid JSON"

**Step 4: Commit**

```bash
git add .claude-plugin/plugin.json
git commit -m "feat: register new skills in plugin.json"
```

---

## Task 12: Final Verification

**Files:**
- Verify all changes

**Step 1: Verify all skills exist**

Run:
```bash
ls -la skills/
```

Expected output should include:
- `learning-instinct/`
- `evolve/`
- `import/`
- `export/`
- `status/`
- `install-opencode/`

**Step 2: Verify all commands simplified**

Run:
```bash
for cmd in commands/*.md; do echo "=== $cmd ==="; cat "$cmd"; echo ""; done
```

Expected: Each command file should have only:
- YAML frontmatter (name, description, command: true)
- One line: "Invoke the instinct:xxx skill..."

**Step 3: Verify skill frontmatter**

Run:
```bash
for skill in skills/*/SKILL.md; do echo "=== $skill ==="; head -5 "$skill"; echo ""; done
```

Expected: Each skill should have:
- `name:` field
- `description:` field starting with "Use when..."
- `disable-model-invocation: true`

**Step 4: Verify plugin.json includes all skills**

Run:
```bash
cat .claude-plugin/plugin.json | grep -A 10 '"skills"'
```

Expected: All 6 skills listed in skills array

**Step 5: Test skill creation logic in evolve**

Run:
```bash
cat skills/evolve/SKILL.md | grep -A 20 "Skill Creation"
```

Expected: Should show the tool detection logic (writing-skills → skill-creator → error)

**Step 6: Final commit if any adjustments needed**

```bash
git add -A
git commit -m "chore: final adjustments to commands-to-skills refactor"
```

---

## Task 13: Clean Up Old Files

**Files:**
- Verify cleanup

**Step 1: Check for any leftover backup files**

Run:
```bash
find . -name "*.bak" -o -name "*~"
```

Expected: No backup files found

**Step 2: Verify skill-create is gone**

Run:
```bash
ls commands/skill-create.md 2>&1
```

Expected: "No such file or directory"

**Step 3: Check git status**

Run:
```bash
git status
```

Expected: Clean working directory (all changes committed)

**Step 4: View commit history**

Run:
```bash
git log --oneline -10
```

Expected: Should see all the refactor commits

---

## Testing Checklist

After implementation, verify:

- [ ] `/evolve` command works and delegates to skill
- [ ] `/import` command works and delegates to skill
- [ ] `/export` command works and delegates to skill
- [ ] `/status` command works and delegates to skill
- [ ] All skills are discoverable and loadable
- [ ] plugin.json validates correctly
- [ ] No duplicate content between commands and skills
- [ ] skill-create is completely removed

---

## Summary

This plan refactors the instinct plugin to:
1. Remove redundant skill-create functionality
2. Convert commands to modular skills with delegation
3. Add intelligent skill creation tool detection to evolve
4. Create install-opencode skill for easy CLI installation

**Total estimated time:** 30-45 minutes
**Total commits:** 13
