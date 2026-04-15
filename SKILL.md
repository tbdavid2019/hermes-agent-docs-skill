---
name: hermes-troubleshooting
description: Use when troubleshooting, configuring, or extending the Hermes Agent. This skill provides an automated index of the official documentation to help diagnose errors (e.g., hermes: command not found, 64k context requirement, API key issues) and understand internal architecture (SOUL.md, Messaging Gateway).
---

# Hermes Agent Troubleshooting Skill

## Overview
This skill leverages the indexed official documentation of the Hermes Agent to provide accurate troubleshooting and configuration guidance. It ensures that any LLM can quickly locate and apply the correct fix based on the latest documentation.

## When to Use
- **Installation Issues**: `hermes: command not found`, WSL2 requirements, missing dependencies.
- **Runtime Errors**: Model context window rejection (< 64k), API key misconfiguration, provider connection issues.
- **Configuration Needs**: Setting up providers (OpenRouter, Ollama, etc.), custom profiles, or the Messaging Gateway.
- **Deep Understanding**: Inquiring about the Agent Loop, SOUL.md, or Personality settings.

## Core Workflow

1.  **Consult the Index**: Start by reading `references/index.md` to find the most relevant document for the user's issue.
2.  **Verify Context Requirements**: If the agent fails at startup, check if the model has the required **64k context window**.
3.  **Run Diagnostic Commands**: Advise users to run `hermes doctor` for automated dependency and config checks.
4.  **Check Configuration**: Use documentation in `user-guide/` or `reference/` to verify `.env` or YAML configurations.

## Quick Reference Table

| Symptom | Relevant Document | Fix/Command |
|---------|-------------------|-------------|
| Command not found | `getting-started/installation.md` | Add `~/.local/bin` to PATH |
| Model rejected | `getting-started/quickstart.md` | Ensure 64,000 token context |
| Config migration | `reference/config.md` | `hermes config migrate` |
| Voice issues | `getting-started/installation.md` | Check Termux/Android limitations |

## Troubleshooting Strategy
- **Step 1**: Identify the symptom (e.g., "Voice mode isn't working on Android").
- **Step 2**: Search `references/index.md` for keywords (e.g., "Android", "Voice").
- **Step 3**: Read the specific document (e.g., `references/getting-started/installation.md`).
- **Step 4**: Provide the documented solution (e.g., "Android Termux does not support faster-whisper; use .[termux] extra").

## References
- [Documentation Index](references/index.md)
- [Architecture Guide](references/developer-guide/architecture.md)
- [Messaging Gateway](references/user-guide/messaging-gateway.md)
