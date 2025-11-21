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
