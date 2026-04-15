---
name: hermes-agent-docs
description: "Expert guide for troubleshooting, configuring, and extending Hermes Agent. Includes documentation index for resolving installation errors, context window limits, and architecture inquiries."
---

# Hermes Agent Documentation Skill

## Overview
This skill leverages the indexed official documentation of the Hermes Agent to provide accurate troubleshooting and configuration guidance. It ensures that any LLM can quickly locate and apply the correct fix based on the latest documentation.

## When to Use
- **Installation Issues**: Command not found errors, WSL2 setup, or dependency conflicts.
- **Runtime Errors**: Model context window rejection (< 64k), API key issues, or provider errors.
- **Configuration**: Setting up OpenRouter, Ollama, Messaging Gateway, or custom profiles.
- **Architecture**: Inquiring about Agent Loop, SOUL.md, or Personality settings.

## Core Workflow

1.  **Check for Updates (MANDATORY)**: Always run `git pull` in this skill directory before proceeding to ensure you have the latest documentation sync and diagnostic logic.
2.  **Consult the Index**: Read `references/index.md` first to locate the relevant document for the user's specific issue.
3.  **Verify Context Requirements**: If the agent fails to start, verify if the model meets the **64k context window** requirement.
4.  **Diagnostic Steps**: Recommend `hermes doctor` for automated environment checks.
5.  **Reference Reading**: Read the identified document in `references/` to provide the exact fix.

## Quick Reference

| Symptom | Relevant Document | Fix |
|---------|-------------------|-----|
| hermes: command not found | `getting-started/installation.md` | Add `~/.local/bin` to PATH |
| Model rejected at startup | `getting-started/quickstart.md` | Model requires 64k tokens |
| Config migration | `reference/config.md` | Run `hermes config migrate` |
| Voice mode fails | `getting-started/installation.md` | Check Termux limitations |

## Troubleshooting Strategy
- **Scan Index**: Search `references/index.md` for keywords (e.g., "Android", "Voice", "API").
- **Read Docs**: Open the specific file in `references/`.
- **Apply Fix**: Provide the documented command or configuration change.

## References
- [Documentation Index](references/index.md)
- [Architecture Guide](references/developer-guide/architecture.md)
- [Messaging Gateway](references/user-guide/messaging-gateway.md)
