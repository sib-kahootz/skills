---
name: evolve-openspec-requirements
description: Evolve OpenSpec requirements after an /opsx:apply has already completed. Use when testing, user feedback, code review, implementation discoveries, or acceptance review reveal additional changes that need to be captured in OpenSpec artifacts, verified, and mapped to next actions such as no implementation change or another /opsx:apply.
---

# Evolve OpenSpec Requirements

## Objective

Keep OpenSpec artifacts and implementation aligned after applied work reveals new or changed requirements.

Assume `/opsx:apply` has already completed unless local evidence shows otherwise.

## Workflow

1. Confirm the post-apply context.
   - Identify the applied change, feature, or OpenSpec change directory.
   - Read relevant OpenSpec artifacts before editing them.
   - Inspect tests, review comments, feedback, or code discoveries that triggered the requirement change.

2. Determine the requirement delta.
   - Separate confirmed requirements from questions, preferences, defects, and implementation tasks.
   - Use `$grill-me` when available if the requirement is ambiguous, high-impact, or has unresolved decision branches.
   - Ask only for decisions that cannot be resolved from repository evidence.

3. Update OpenSpec artifacts.
   - Preserve the repository's existing OpenSpec structure and terminology.
   - Update requirements, scenarios, proposal/design notes, and task tracking only where the delta changes them.
   - Mark completed tasks accurately; add new tasks only when implementation or verification work remains.
   - Do not rewrite applied history merely for style.

4. Verify the updated specifications.
   - Run the repository's OpenSpec validation command when discoverable.
   - Prefer strict validation if the repo already uses it.
   - If validation cannot run, state the exact blocker and perform a manual consistency check across changed artifacts.

5. Recommend next actions.
   - Return `No implementation changes required` when the updated artifacts only clarify or record already-correct behavior.
   - Return `Run /opsx:apply` when the updated artifacts require implementation, test, migration, or documentation changes.
   - Include any unresolved decisions or validation gaps before recommending implementation.

## Output Shape

End with:

- `Requirement delta`: concise list of changed or newly discovered requirements.
- `OpenSpec updates`: files changed and what changed in each.
- `Verification`: validation command and result, or manual check performed.
- `Next action`: exactly one of `No implementation changes required` or `Run /opsx:apply`, with a short reason.

## Guardrails

- Do not treat bugs, review comments, or user preferences as requirements until they are translated into expected behavior.
- Do not update implementation unless the user explicitly asks for more than OpenSpec evolution.
- Do not skip spec verification after edits.
- Do not recommend `/opsx:apply` for documentation-only clarifications that do not change expected behavior.
