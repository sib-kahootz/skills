# AI Skills

Repository for storing, testing, and sharing AI skills.

## Structure

```text
skills/
+-- custom/         # Skills built from scratch
+-- third-party/    # External or community skills
+-- experimental/   # Prototypes, tests, and ideas
```

## Skill Structure

Each skill should follow this structure:

```text
skill-name/
+-- SKILL.md
+-- agents/
|   +-- openai.yaml
+-- scripts/
+-- references/
+-- assets/
```

## Installation

Install this repository in the skills directory configured for your AI assistant or agent runtime. Refer to that runtime's documentation for the discovery path and refresh procedure.

To update an existing installation, run `git pull` from the skills directory, then refresh the runtime's skill list if required.

## Agent Instructions

Example root `AGENTS.md`:

```markdown
## Skills

- For non-trivial coding or refactoring, use the `karpathy-guidelines` and `ousterhout-comment-guidelines` skills when they are available.
- Before choosing between materially different approaches, scopes, trade-offs, or outcomes, use the `grilling` skill when it is available.
- Skip `grilling` when the choice is routine, low-risk and easily reversible, or already made explicitly by the user.
- After using a skill from `skills/custom` or `skills/experimental`, suggest at most one concrete improvement to that skill, and only when the suggestion is genuinely worthwhile.
```
