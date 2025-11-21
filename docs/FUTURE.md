# Future Vision

## Universal Artifact Validation

We built a skill auditor that validates Claude Code skills. We observed a powerful pattern:

1. **Extract metrics** (deterministic, Python-based)
2. **Validate rules** (deterministic, rule-based)
3. **Enhance with LLM** (optional, for explanations)

This pattern applies to other Claude Code artifacts:

- **Commands**: Validate `/commands:name` definitions
- **Agents**: Validate subagent configurations
- **Workflows**: Validate multi-step processes
- **Policies**: Validate security and access rules

## Deferred Until Needed

We defer these abstractions:

- `BaseAuditor` abstract class (requires 2+ implementations first)
- Auto-detection of artifact types (requires multiple types first)
- Unified CLI interface (requires multiple auditors first)
- Rule registry system (may be unnecessary)

## Next Experiment

**Command auditor** - Build as a separate, independent tool to:

- Validate the extract/validate/enhance pattern for commands
- Discover common elements vs. artifact-specific logic
- Learn which rules apply universally vs. per-type
- Test whether the pattern holds before abstracting

After we have 2-3 working auditors, we extract common patterns
based on what emerged, not what we imagined.

## Why This Approach

Following the **Rule of Three**:

1. First time: Just build it (skill auditor ✅)
2. Second time: Notice the pattern (command auditor - future)
3. Third time: Extract the abstraction (agent auditor - future)

This avoids premature abstraction. Our patterns emerge from
real implementations, not imagined requirements.

## Current Focus

Ship v1.0 and learn from usage:

- Use skill-auditor on real skills
- Document false positives and missing checks
- Identify which Claude explanations add value
- Gather requirements before building framework

The vision is real. We reach it through disciplined iteration.
