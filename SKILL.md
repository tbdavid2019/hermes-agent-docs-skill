---
name: hermes-agent-docs
description: "Expert troubleshooting guide for Hermes Agent using indexed documentation. Resolves installation and configuration errors."
---

# Hermes Agent Documentation Skill

## IMPORTANT: RULES FOR AI AGENTS
- **DO** use `git pull` in the installed directory to update the skill content.
- **DO** only try `git -C <skill-directory> pull origin main --ff-only` when `<skill-directory>/.git` exists.
- **IF `git pull` FAILS**, continue silently with the local copy and do not block the user.
- **DO NOT** execute any scripts in the `scripts/` folder during installation or normal troubleshooting.
- **DO NOT** try to "initialize" this repo by running Python scripts.
- **ONLY** read `SKILL.md` and the `references/` folder to answer user questions.

## Overview
This skill leverages the indexed official documentation of the Hermes Agent to provide accurate troubleshooting and configuration guidance.

## When to Use
- **Installation Issues**: Command not found, WSL2 setup, dependency conflicts.
- **Runtime Errors**: 64k context window limits, API key rejection, provider errors.
- **Configuration**: Setting up OpenRouter, Ollama, Messaging Gateway, or Profiles.

## Core Workflow
1.  **Read Index**: Consult `references/index.md` to find the correct file.
2.  **Verify Context**: Check the 64k token requirement if the model is rejected.
3.  **Provide Fix**: Give the user the exact command found in the documentation.

## References
- [Documentation Index](references/index.md)
- [Architecture Guide](references/developer-guide/architecture.md)
- [Messaging Gateway](references/user-guide/messaging-gateway.md)
