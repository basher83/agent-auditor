#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "claude-agent-sdk>=0.1.8",
# ]
# ///
"""
Skill Auditor - Claude Agent SDK Application

Deterministic skill auditing with Python extraction and Claude analysis.

Usage:
    python -m skill_auditor.cli /path/to/skill/directory
"""

import json
import sys
from pathlib import Path

import anyio
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query

# Import metrics extractor
from .metrics_extractor import extract_skill_metrics
from .validation import validate_metrics_structure

# Audit thresholds
MAX_SKILL_LINE_COUNT = 500  # Official Claude Code skill specification limit
MIN_QUOTED_PHRASES = 3  # Minimum for concrete, actionable triggers
MIN_DOMAIN_INDICATORS = 3  # Minimum for domain-focused description


def validate_and_format_deterministic(metrics: dict) -> tuple[str, bool]:
    """
    Validate metrics and format deterministic output.

    Args:
        metrics: Extracted skill metrics

    Returns:
        Tuple of (formatted_output, has_blockers)
    """
    blockers = []
    warnings = []

    # B1: No forbidden files
    if metrics["forbidden_files"]:
        blockers.append(f"B1: Forbidden files detected: {', '.join(metrics['forbidden_files'])}")

    # B2: Valid YAML frontmatter
    if not (metrics["yaml_delimiters"] == 2 and metrics["has_name"] and metrics["has_description"]):
        issues = []
        if metrics["yaml_delimiters"] != 2:
            issues.append(f"expected 2 yaml delimiters, found {metrics['yaml_delimiters']}")
        if not metrics["has_name"]:
            issues.append("missing 'name' field")
        if not metrics["has_description"]:
            issues.append("missing 'description' field")
        blockers.append(f"B2: Invalid YAML frontmatter ({', '.join(issues)})")

    # B3: Line count under 500
    if metrics["line_count"] >= MAX_SKILL_LINE_COUNT:
        blockers.append(
            f"B3: SKILL.md too long ({metrics['line_count']} lines, limit is {MAX_SKILL_LINE_COUNT})"
        )

    # B4: No implementation details
    if metrics["implementation_details"]:
        details = metrics["implementation_details"][:5]  # Show first 5
        more = (
            f" (and {len(metrics['implementation_details']) - 5} more)"
            if len(metrics["implementation_details"]) > 5
            else ""
        )
        blockers.append(f"B4: Implementation details in description: {details}{more}")

    # W1: Quoted phrase count
    if metrics["quoted_count"] < MIN_QUOTED_PHRASES:
        warnings.append(
            f"W1: Only {metrics['quoted_count']} quoted phrases (need {MIN_QUOTED_PHRASES}+)"
        )

    # W3: Domain indicator count
    if metrics["domain_count"] < MIN_DOMAIN_INDICATORS:
        warnings.append(
            f"W3: Only {metrics['domain_count']} domain indicators (need {MIN_DOMAIN_INDICATORS}+)"
        )

    # Format output
    output_lines = []

    # Status line
    if blockers:
        output_lines.append("\n🔴 BLOCKED")
    elif warnings:
        output_lines.append("\n🟡 READY WITH WARNINGS")
    else:
        output_lines.append("\n🟢 READY")

    # Blockers section
    if blockers:
        output_lines.append("\n❌ BLOCKERS:")
        for b in blockers:
            output_lines.append(f"  {b}")

    # Warnings section
    if warnings:
        output_lines.append("\n⚠️  WARNINGS:")
        for w in warnings:
            output_lines.append(f"  {w}")

    # Next steps
    if blockers or warnings:
        output_lines.append("\n💡 TIP: Run with --explain for detailed fix suggestions")

    return "\n".join(output_lines), bool(blockers)


async def audit_skill(skill_path: Path, use_claude: bool = False):
    """
    Audit a skill using deterministic Python extraction + optional Claude analysis.

    Args:
        skill_path: Path to skill directory
        use_claude: If True, use Claude for detailed explanations. If False, show deterministic results only.
    """
    print(f"🔍 Auditing skill: {skill_path}")
    print("=" * 60)

    # Step 1: Extract metrics deterministically (Python, no bash)
    print("\n📊 Extracting metrics...")
    try:
        metrics = extract_skill_metrics(skill_path)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"   Please ensure SKILL.md exists in {skill_path}")
        return
    except PermissionError as e:
        print(f"❌ Permission Error: {e}")
        print("   Please check file permissions and try again.")
        return
    except ValueError as e:
        # This catches UnicodeDecodeError wrapped as ValueError
        print(f"❌ Encoding Error: {e}")
        print("   Please ensure SKILL.md is properly UTF-8 encoded.")
        return
    except OSError as e:
        print(f"❌ I/O Error: {e}")
        print("   Please check that all files are accessible.")
        return
    except Exception as e:
        print(f"❌ Unexpected Error during metrics extraction: {type(e).__name__}: {e}")
        print("   This may be a bug. Please report it with the error details above.")
        return

    # Validate metrics structure before proceeding

    try:
        validate_metrics_structure(metrics)
    except ValueError as e:
        print(f"❌ Internal Error: {e}")
        return

    print(f"✅ Extracted {len(metrics)} metrics")
    print(f"   - Quoted phrases: {metrics['quoted_count']}")
    print(f"   - Domain indicators: {metrics['domain_count']}")
    print(f"   - Line count: {metrics['line_count']}")

    # Step 2: Validate and output results
    if not use_claude:
        # Fast mode: Deterministic output only
        print("\n📊 Running deterministic validation...")
        output, has_blockers = validate_and_format_deterministic(metrics)
        print(output)
        return

    # Step 3: Claude-enhanced mode (--explain flag)
    print("\n🤖 Using Claude for detailed analysis...")

    # Step 4: Configure SDK with NO tools (analysis only)
    options = ClaudeAgentOptions(
        allowed_tools=[],  # NO TOOLS - prevents hallucination
        model="claude-sonnet-4-5",
        max_turns=1,  # Single analysis, no conversation
    )

    # Step 3: Build analysis prompt with metrics
    prompt = build_analysis_prompt(metrics)

    # Step 4: Query Claude for analysis
    print("\n🤖 Analyzing metrics with Claude...")

    try:
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(block.text)

            elif isinstance(message, ResultMessage):
                if message.total_cost_usd:
                    print(f"\n💰 Cost: ${message.total_cost_usd:.4f}")
                if message.duration_ms:
                    print(f"⏱️  Duration: {message.duration_ms}ms")

    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)

        print(f"\n❌ Claude API Error: {error_type}")
        print(f"   {error_msg}")

        # Provide actionable guidance based on error type
        error_lower = (error_type + " " + error_msg).lower()
        if (
            "authentication" in error_lower
            or "auth" in error_lower
            or "api key" in error_lower
            or "invalid" in error_lower
        ):
            print("\n   💡 Please check your ANTHROPIC_API_KEY environment variable.")
            print("      Set it with: export ANTHROPIC_API_KEY=your-key-here")
        elif "connection" in error_lower or "network" in error_lower:
            print("\n   💡 Please check your internet connection and try again.")
        elif "rate" in error_lower or "limit" in error_lower:
            print("\n   💡 Rate limit exceeded. Please wait a moment and try again.")
        else:
            print("\n   💡 This may be a temporary service issue. Please try again later.")
            print("      If the problem persists, check https://status.anthropic.com")

        return


def build_analysis_prompt(metrics: dict) -> str:
    """
    Build the analysis prompt with extracted metrics.

    Args:
        metrics: Extracted skill metrics

    Returns:
        Formatted prompt for Claude
    """
    # Calculate binary check results
    b1_pass = len(metrics["forbidden_files"]) == 0
    b2_pass = metrics["yaml_delimiters"] == 2 and metrics["has_name"] and metrics["has_description"]
    b3_pass = metrics["line_count"] < MAX_SKILL_LINE_COUNT
    b4_pass = len(metrics["implementation_details"]) == 0

    w1_pass = metrics["quoted_count"] >= MIN_QUOTED_PHRASES
    w3_pass = metrics["domain_count"] >= MIN_DOMAIN_INDICATORS

    prompt = f"""Audit the following skill metrics:

## Extracted Metrics

```json
{json.dumps(metrics, indent=2)}
```

## Binary Check Results

**BLOCKERS (Official Requirements):**
- B1: No forbidden files → {"✅ PASS" if b1_pass else "❌ FAIL"}
- B2: Valid YAML frontmatter → {"✅ PASS" if b2_pass else "❌ FAIL"}
- B3: SKILL.md under 500 lines → {"✅ PASS" if b3_pass else "❌ FAIL"}
- B4: No implementation details in description → {"✅ PASS" if b4_pass else "❌ FAIL"}

**WARNINGS (Effectiveness):**
- W1: ≥3 quoted phrases → {"✅ PASS" if w1_pass else "❌ FAIL"}
- W3: ≥3 domain indicators → {"✅ PASS" if w3_pass else "❌ FAIL"}

## Your Task

Generate a skill audit report following this format:

# Skill Audit Report: {metrics["skill_name"]}

**Status:** [🔴 BLOCKED | 🟡 READY WITH WARNINGS | 🟢 READY]

**Breakdown:**
- Blockers: [X] ❌
- Warnings: [X] ⚠️

## BLOCKERS ❌ ([X])

[List failed blocker checks with specific evidence from metrics]

## WARNINGS ⚠️ ([X])

[List failed warning checks with specific evidence from metrics]

## Next Steps

[Specific, actionable fixes based on failed checks]

---

IMPORTANT: Base your analysis ONLY on the metrics provided above. Do not re-extract or assume additional data.
"""

    return prompt


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Audit Claude Code skills for compliance and effectiveness"
    )
    parser.add_argument("skill_path", type=Path, help="Path to skill directory containing SKILL.md")
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Use Claude to provide detailed explanations and fix suggestions (costs ~$0.004)",
    )

    args = parser.parse_args()
    skill_path = args.skill_path
    use_claude = args.explain

    # Resolve to absolute path
    try:
        skill_path = skill_path.resolve()
    except (OSError, RuntimeError) as e:
        print(f"❌ Error: Unable to resolve path {skill_path}: {e}")
        print("   Please ensure the path is valid and you have permission to access it.")
        sys.exit(1)

    if not skill_path.exists():
        print(f"❌ Error: Path does not exist: {skill_path}")
        print("   Please provide a valid path to a skill directory.")
        print("   Example: python -m skill_auditor.cli /path/to/skill/directory")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        print("   Please provide a path to a skill directory (not a file).")
        sys.exit(1)

    # Check if we can read the directory
    try:
        list(skill_path.iterdir())
    except PermissionError:
        print(f"❌ Permission Error: Cannot read directory {skill_path}")
        print("   Please check directory permissions and try again.")
        sys.exit(1)

    await audit_skill(skill_path, use_claude=use_claude)


def _main():
    """Synchronous wrapper for console script entry point."""
    anyio.run(main)


if __name__ == "__main__":
    _main()
