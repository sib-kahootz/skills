# AI Skills Repository

Repository for storing, testing, and sharing AI skills.

## Structure

```text
ai-skills/
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

Codex loads skills from the `skills/` directory under the Codex home folder. Clone this repository into that existing directory.

On Windows, the target folder is usually:

```text
%USERPROFILE%\.codex\skills
```

For a first-time install:

```powershell
git clone https://github.com/sib-kahootz/codex-skills.git $env:USERPROFILE\.codex\skills
```

To update an existing install, run `git pull` from the skills directory. Restart Codex or start a new session after installing or updating so the skill list is refreshed.

## Agent Instructions

Example root `AGENTS.md`:

```markdown
## Skills

- For non-trivial coding or refactoring, use the `karpathy-guidelines` skill when it is available.
- Before choosing between materially different approaches, scopes, trade-offs, or outcomes, use the `grilling` skill when it is available.
- Skip `grilling` when the choice is routine, low-risk and easily reversible, or already made explicitly by the user.
- After using a skill from `skills/custom` or `skills/experimental`, suggest at most one concrete improvement to that skill, and only when the suggestion is genuinely worthwhile.
```
