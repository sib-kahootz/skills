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

## Notes

Keep experiments lightweight. Move only useful, reviewed skills into `custom/`.
