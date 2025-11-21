# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## ⚠️ CRITICAL: Audit Agent Protocol

**When invoking ANY audit agent (skill-auditor, command-audit, pr-review, etc.):**

1. **ONLY provide the file path** - Nothing else
2. **DO NOT mention what you just fixed** - No context about recent changes
3. **DO NOT hint at what to look for** - No expectations or guidance
4. **DO NOT use words like "test", "verify", "check"** - Taints the agent's objectivity
5. **DO NOT explain why you're auditing** - Let the agent form independent conclusions

**Correct audit invocation:**

```text
plugins/meta/meta-claude/skills/skill-factory
```

**WRONG - Tainted audit invocation:**

```text
We just fixed effectiveness issues. Can you audit plugins/meta/meta-claude/skills/skill-factory
to verify the triggers are now concrete?
```

**Why this matters:** Tainted context skews audit results. The agent will look for what you
mentioned instead of finding issues independently. This creates false positives and missed violations.

**Remember:** Trust but verify. Always audit with untainted context.

---

## Project Overview

**agent-auditor** is a comprehensive auditing system for Claude Code skills, agents, and components.
It provides deterministic Python-based metric extraction and Claude-powered analysis.

See `README.md` and `docs/` for detailed documentation.

## Development

- **Tools:** See `mise.toml` for developer tools and tasks
- **Testing:** `mise exec -- pytest src/tests/`
- **Linting:** `ruff check .` and `ruff format .`
- **Type Checking:** `mise exec -- pyright src`

## Key Concepts

- **Deterministic Auditing:** Python-based extraction ensures consistent results
- **Effectiveness Validation:** Checks compliance and auto-invocation potential
- **Progressive Disclosure:** Validates information architecture patterns

## Core Principles

### Trust But Verify

**Never trust claims without verification.** This applies to:

- Test counts: Run `mise exec -- pytest src/tests/` to verify actual pass/fail status
- Documentation claims: Check the actual code/files referenced
- Migration status: Verify completion with actual commands, not checklist marks
- Metrics and statistics: Run the tools to get current values

**Example:**

- ❌ "The README says 41 tests pass" → Unverified claim
- ✅ Run `mise exec -- pytest src/tests/` → Verified: 41 passed in 0.03s

## Multi-Agent Orchestration Patterns

This repository has proven multi-agent patterns for high-quality, efficient work:

### Parallel Scout Agents

For comprehensive codebase exploration, dispatch multiple general-purpose agents in parallel:

```text
Launch 5 scouts simultaneously:
- Agent 1: Explore root-level docs
- Agent 2: Explore docs/ directory
- Agent 3: Explore src/ structure
- Agent 4: Explore agents/ definitions
- Agent 5: Explore tests/ coverage
```

**Why**: Provides complete repo overview in one shot for strategic planning.

### Research → Validate → Execute

For technical configurations, use research tools before implementing:

```bash
./scripts/firecrawl_sdk_research.py "Claude Agent SDK configuration usage" --limit 5
```

**Why**: Verify against official documentation instead of guessing. Prevents trial-and-error loops.

### Specialized Agents for Complex Workflows

Use predefined agents for multi-step processes:

- `commit-craft` - Creates atomic, conventional commits; discovers and fixes issues autonomously
- `elements-of-style:writing-clearly-and-concisely` - Applies Strunk's principles rigorously

**Why**: Specialized agents have workflows and can solve problems independently.

### Key Learnings

1. **Skills beat instructions**: Invoking skills > describing principles in prompts
2. **Parallel > Sequential**: Multiple scouts exploring simultaneously >> one at a time
3. **Verify don't guess**: Research first (firecrawl) before implementing
4. **Let agents solve problems**: Agents discover and fix issues autonomously (e.g., pre-commit hooks)
5. **General-purpose agents work**: Most tasks used on-demand general-purpose agents, not predefined subagents
