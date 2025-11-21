---
name: require-uv
enabled: true
event: bash
pattern: ^(?!uv\s|mise\s).*(python3?(?:\.\d+)?|pip3?|pytest)
action: block
---

# ⛔ Direct Python Command Detected

## UV Project Requirement Violation

You attempted to run a Python command directly instead of using `uv`.

**This is a UV project** - all Python operations must go through `uv`.

## What You Tried

Your command contains a direct Python invocation:
- `python` / `python3` / `python3.x`
- `pip` / `pip3`
- `pytest`

## What To Use Instead

| ❌ Don't Use | ✅ Use Instead |
|--------------|----------------|
| `python script.py` | `uv run python script.py` |
| `python -m module` | `uv run python -m module` |
| `pip install package` | `uv pip install package` |
| `pip install -e .` | `uv pip install -e .` |
| `pytest` | `mise exec -- pytest` or `uv run pytest` |
| `python -m pytest` | `mise exec -- pytest` |

## Why This Matters

**UV ensures:**
- Correct Python version from `.python-version`
- Virtual environment isolation
- Dependency resolution consistency
- Project-specific package versions

**Direct python calls can:**
- Use wrong Python version (system vs project)
- Install packages globally instead of in venv
- Miss project-specific dependencies
- Create subtle bugs from version mismatches

## Project Context

From `pyproject.toml`:
- Python requirement: `>=3.11`
- Package manager: UV
- Tool configuration: `mise.toml`

Always use `uv` or `mise exec --` for Python operations.

---

*This rule enforces the UV-first approach documented in README.md and CLAUDE.md*
