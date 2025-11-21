# Scripts

This directory contains helper scripts

## Documentation and Web Scraping

**firecrawl_sdk_research.py** - Advanced web research tool using Firecrawl SDK.
Searches the web with optional category filtering (github, research, pdf), scrapes
content with combined API calls for efficiency, filters results by quality scoring,
and synthesizes into a single markdown document. Includes retry logic with exponential
backoff and quality indicators (⭐ for high-quality sources). Requires
`FIRECRAWL_API_KEY`.

## Markdown Processing

**markdown_formatter.py** - Fixes missing language tags and spacing issues in markdown
files. Detects programming languages in unlabeled code fences and adds appropriate
identifiers. Works as a Claude Code hook or standalone CLI tool.

## Development Tools

**note_smith.py** - Interactive research assistant demonstrating Claude Agent SDK
features. Provides custom MCP tools for saving and searching notes, WebFetch integration
for URL summarization, and hook-based command safety.

## Usage Patterns

Most scripts use inline script dependencies (PEP 723) and run with `uv`:

Scripts requiring API keys check environment variables and exit with clear error messages when credentials are missing.
