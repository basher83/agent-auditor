# Migration Checklist

This document tracks the migration of agent-auditor content from lunar-claude to a standalone repository.

## Status

**Current Phase:** Project Configuration Complete ✅

All content has been copied to `agent-auditor/` directory. Project is now
configured as a standalone Python package with:

- `pyproject.toml` with proper dependencies and build configuration
- Updated file paths and references throughout codebase
- Console script entry point (`skill-auditor` command)
- Module execution support (`python -m skill_auditor.cli`)

## What Was Copied

### Documentation (✅ Complete)

- [x] Research documentation from `docs/research/audit-skill/`
- [x] Review documentation from `docs/reviews/skill-auditor/`
- [x] Audit reports from `docs/reviews/audits/meta-claude/`
- [x] Notes from `docs/notes/` (skill-auditor related)
- [x] Planning documents from `docs/plans/` (skill-auditor related)

### Source Code (✅ Complete)

- [x] Python SDK from `scripts/skill_auditor/`
- [x] Main CLI script `scripts/skill-auditor.py`
- [x] All test files

### Agents (✅ Complete)

- [x] All agent definitions from `plugins/meta/meta-claude/agents/skill/`

### Commands (✅ Complete)

- [x] Command definitions from `plugins/meta/meta-claude/commands/skill/`

## Next Steps for New Repository

### 1. Repository Setup

- [x] Create new GitHub repository `agent-auditor`
- [x] Initialize git repository
- [x] Copy content from `agent-auditor/` to new repo root
- [x] Create `.gitignore` (Python, Claude Code patterns)
- [x] Add LICENSE file

### 2. Project Configuration

- [x] Create `pyproject.toml` with proper dependencies
- [x] Set up Python package structure
- [x] Configure build system (hatchling with uv/pip support)
- [x] Add pre-commit hooks if desired (already configured)

### 3. Update File Paths

- [x] Update import paths in Python files (relative imports already correct)
- [x] Update file references in agent definitions (skill-auditor-v6.md updated)
- [x] Update documentation cross-references (README.md, sdk-reference.md updated)
- [x] Fix any hardcoded paths (cli.py example paths updated)

**Completed Changes:**

- Created `pyproject.toml` with hatchling build system, dependencies, and console script entry point
- Updated `agents/skill-auditor-v6.md`: Changed `./scripts/skill-auditor.py` → `python -m skill_auditor.cli`
- Updated `README.md`: Added installation and usage instructions
- Updated `docs/api/sdk-reference.md`: Removed lunar-claude specific paths
- Updated `src/skill_auditor/cli.py`: Generic example paths and added `_main()` wrapper for console script
- Package can be installed with `pip install -e .` or `uv pip install -e .`
- CLI available as `python -m skill_auditor.cli` or `skill-auditor` command

### 4. Documentation

- [ ] Create comprehensive README.md
- [ ] Write usage guides
- [ ] Document API reference
- [ ] Create CHANGELOG.md from git history

### 5. Testing

- [ ] Verify all tests pass in new structure
- [ ] Update test paths if needed
- [ ] Set up CI/CD if desired

### 6. Cleanup

- [ ] Review and remove unnecessary files
- [ ] Organize documentation structure
- [ ] Archive historical versions appropriately

## Files That Reference Skill Auditor (Need Updates)

These files in lunar-claude reference skill-auditor and may need updates:

- `CLAUDE.md` - Line 8 mentions skill-auditor in audit protocol
  - **Action:** Add note pointing to new repository

- `.claude-plugin/marketplace.json` - May reference skill-auditor commands
  - **Action:** Remove or update references

## Notes

- All files copied (not moved) - originals preserved
- Structure mirrors proposed new repository layout
- Some files may need path updates after migration
- Agent definitions may reference local paths that need updating
