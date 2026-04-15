---
name: hermes-agent-docs
description: "Expert troubleshooting guide for Hermes Agent using indexed documentation. Resolves installation and configuration errors."
---

# Hermes Agent Documentation Skill

## IMPORTANT: RULES FOR AI AGENTS
- **DO NOT** execute any scripts in the `scripts/` folder during installation or normal troubleshooting.
- **DO NOT** try to "initialize" this repo by running Python scripts.
- **ONLY** read the `references/` folder to answer user questions.
- **ONLY** run `git pull` if you suspect the local documentation is outdated.

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
