# Agent Auditor

Comprehensive auditing system for Claude Code skills, agents, and components.

## Overview

This repository contains all research, development, and implementation artifacts
related to the skill auditor system - a tool for validating Claude Code skills
against official Anthropic specifications and ensuring effectiveness for
auto-invocation.

## Structure

```text
agent-auditor/
├── docs/                    # Documentation
│   ├── research/            # Research and analysis
│   └── guides/              # User guides
├── src/                     # Source code
│   ├── skill_auditor/       # Python SDK
│   └── tests/              # Test suite
├── agents/                  # Claude Code agent definitions
├── commands/                # Claude Code command definitions
└── MIGRATION.md            # Migration checklist
```

## What's Included

### Research & Documentation

- Architecture decisions and design rationale
- Problem analysis and root cause investigations
- Implementation documentation and plans
- Testing results and validation reports
- Agent evolution history
- Development notes and observations

### Source Code

- Python SDK for deterministic skill auditing
- Metrics extraction and validation logic
- Test suite with comprehensive coverage
- CLI application

### Agent Definitions

- Multiple versions of skill-auditor agents (v3-v6)
- Evolution showing progression from non-deterministic to deterministic approaches

### Commands

- Claude Code commands for skill validation and auditing

## Quick Start

### Installation

```bash
# Install from source
uv pip install -e .
```

### Usage

The skill auditor runs in two modes:

**Fast Mode (Default)** - Deterministic validation only:

```bash
# Using module
uv run python -m skill_auditor.cli /path/to/skill/directory

# Or using console script (after installation)
skill-auditor /path/to/skill/directory
```

**Explain Mode** - Claude-powered detailed analysis and fix suggestions:

```bash
# Add --explain flag for AI-powered explanations
uv run python -m skill_auditor.cli /path/to/skill/directory --explain

# Or with console script
skill-auditor /path/to/skill/directory --explain
```

### Examples

**Fast Mode** (instant, free):

```bash
$ uv run python -m skill_auditor.cli .claude/skills/my-skill

🔍 Auditing skill: .claude/skills/my-skill
============================================================

📊 Extracting metrics...
✅ Extracted 14 metrics
   - Quoted phrases: 2
   - Domain indicators: 4
   - Line count: 450

📊 Running deterministic validation...

🔴 BLOCKED

❌ BLOCKERS:
  B4: Implementation details in description: ['script.py', 'docker']

⚠️  WARNINGS:
  W1: Only 2 quoted phrases (need 3+)

💡 TIP: Run with --explain for detailed fix suggestions
```

**Explain Mode** (~2-3s, ~$0.004):

```bash
$ uv run python -m skill_auditor.cli .claude/skills/my-skill --explain

🔍 Auditing skill: .claude/skills/my-skill
============================================================

📊 Extracting metrics...
✅ Extracted 14 metrics

🤖 Using Claude for detailed analysis...

# Skill Audit Report: my-skill

**Status:** 🔴 BLOCKED

[Detailed explanations and fix suggestions from Claude...]
```

## Key Concepts

- **Deterministic Auditing**: Python-based extraction ensures consistent results across runs
- **Dual-Mode Operation**: Fast deterministic validation (default) or AI-powered explanations (--explain)
- **Effectiveness Validation**: Checks not just compliance but also auto-invocation potential
- **Progressive Disclosure**: Validates skills follow correct information architecture patterns

## Architecture

The auditor uses a two-tier architecture:

1. **Deterministic Layer (Python)** - Always runs:
   - Extracts metrics (quoted phrases, domain indicators, line count, etc.)
   - Validates against official requirements (B1-B4)
   - Checks effectiveness criteria (W1, W3)
   - Fast, free, reproducible

2. **Semantic Layer (Claude)** - Optional with `--explain`:
   - Provides human-friendly explanations
   - Suggests specific fixes
   - Adds context and recommendations
   - Costs ~$0.004 per audit, takes 2-3 seconds

## Origin

This content was extracted from the `lunar-claude` repository where it was
developed as part of the meta-claude plugin. All original files remain in their
original locations - this is a copy for migration purposes.
