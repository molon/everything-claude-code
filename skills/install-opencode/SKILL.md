---
name: install-opencode
description: Use when user needs opencode CLI functionality for code analysis, generation, or other tasks, or when opencode command is not found
disable-model-invocation: true
---

# Install OpenCode

## Overview

Install opencode CLI using the official installer script and verify installation works.

## Official Documentation

**https://opencode.ai/docs/#install**

Always reference official docs for the most current installation instructions.

## Installation

```bash
curl -fsSL https://opencode.ai/install | bash
```

This is the official installation method. The installer handles PATH automatically.

**Permission denied?**
```bash
curl -fsSL https://opencode.ai/install | sudo bash
```

## Verification

**After installation, always verify with a test:**

```bash
opencode run "what is 2+2" --model opencode/big-pickle
```

**Expected output:** "4" or equivalent

Only after seeing correct output, confirm installation succeeded.

## Troubleshooting

**Command not found after install:**

The installer should add `~/.opencode/bin` to PATH automatically. If `opencode` is still not found:

```bash
# Check if it exists
ls ~/.opencode/bin/opencode

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/.opencode/bin:$PATH"
```

**Installer script fails?**

Check official docs for alternative installation methods: https://opencode.ai/docs/#install
