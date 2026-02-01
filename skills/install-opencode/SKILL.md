---
name: install-opencode
description: Install opencode CLI if not already installed and verify installation. Use when user needs opencode CLI functionality for code analysis, generation, or other tasks.
disable-model-invocation: true
---

# Install OpenCode

Installs the opencode CLI tool if not already present on the system.

## Check if Already Installed

Before attempting installation:

```bash
which opencode
opencode --version
```

- If `opencode` is found and version shows: Already installed, skip installation
- If command not found: Proceed with installation

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
