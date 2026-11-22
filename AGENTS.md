
# Agentic AI Bootcamp — Coding Agent Instructions

## Project
Enterprise banking multi-agent learning platform.

## Technology
- Python 3.11+
- Google Gemini API
- Pydantic
- pytest
- LangGraph and Google ADK in later projects

## Development Rules
1. Prefer small, testable Python functions.
2. Use type hints and clear docstrings.
3. Never hardcode secrets.
4. Never commit .env files.
5. Use synthetic banking data only.
6. Validate all model-generated tool arguments.
7. Enforce authorization in trusted application code.
8. Do not add new dependencies unnecessarily.
9. Add tests for new functionality.
10. Keep cloud API calls out of unit tests.

## Verification
Run:
python -m pytest tests/ -v

## Git
Use descriptive commit messages.
Do not commit code with failing tests.

## Architecture
Keep LLM reasoning separate from tool execution.
Do not treat LLM-generated content as trusted input.
