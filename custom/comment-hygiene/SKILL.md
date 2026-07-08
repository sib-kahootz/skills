---
name: comment-hygiene
description: Create, rewrite, audit, or remove source code comments and documentation comments so they explain useful design knowledge rather than restating code. Use when the user asks to add comments, improve comments, clean up comments, review comments, improve comment hygiene, remove noisy comments, update stale comments, write docstrings, rewrite API docs, or edit inline, block, module, class, function, method, interface, or public contract comments in files, diffs, pull requests, or selected code.
disable-model-invocation: true
---

# Comment Hygiene

Edit comments directly in source files when paths or diffs are available. Preserve runtime behavior unless the user explicitly asks for code changes.

Good comments explain non-obvious intent, contracts, invariants, rationale, constraints, tradeoffs, side effects, failure modes, ownership, ordering, security implications, or reader-facing behavior. Bad comments repeat names, syntax, types, or simple control flow.

## Workflow

1. Identify scope: selected file, file list, diff hunk, function, class, module, API surface, or comment block.
2. Read enough surrounding code to understand the abstraction, call sites, tests, and local comment style.
3. Read `references/comment-practice.md` when the task needs judgment beyond obvious cleanup or when adding new comments.
4. Classify each relevant comment:
   - `keep`: explains intent, contract, invariant, limitation, side effect, assumption, tradeoff, or design reason.
   - `delete`: restates code, duplicates names, explains syntax, narrates obvious flow, or has become noise.
   - `rewrite`: stale, vague, too low-level, misleading, contradictory, too broad, or missing reader-facing constraints.
   - `add`: code has a non-obvious contract, invariant, workaround, failure mode, concurrency rule, security rule, data-shape assumption, or public behavior.
5. Apply focused edits. Match the repository's existing comment style, docstring format, line length, and terminology.
6. Review the edited comments against the code to ensure they remain true and still explain a non-obvious contract, invariant, rationale, or constraint.
7. Report changed files and the main comment decisions.

## Editing Rules

- Prefer fewer, stronger comments.
- Explain why, contract, or invariant; avoid narrating what each line does.
- Keep comments close to the abstraction or code they clarify.
- Delete comments that became obvious after renaming or simplifying nearby code only if the user allowed code edits; otherwise improve the comment alone.
- Do not invent rationale. If intent cannot be inferred, leave the comment unchanged or ask for context.
- Add TODO comments only when the repo already uses TODOs and the TODO includes a concrete owner/tracker or removal condition.
- Preserve generated files unless the user explicitly asks to edit them.
- Preserve license headers, copyright notices, linter directives, coverage pragmas, region markers, and required tool annotations.

## What To Add

Add or improve comments for:

- public APIs and exported abstractions with caller-visible contracts
- surprising behavior or intentionally unusual choices
- invariants later code relies on
- error handling, retries, idempotency, ordering, ownership, or lifecycle rules
- concurrency, caching, performance, security, or data-consistency constraints
- external bug workarounds, compatibility constraints, migration assumptions, or temporary limitations

## What To Remove

Remove or rewrite comments that:

- paraphrase the next line of code
- repeat function, variable, or type names
- explain language syntax or obvious control flow
- drift from current behavior
- use vague words such as `magic`, `stuff`, `thing`, `simple`, `probably`, or `normally`
- leave TODOs without enough context to act on them

## Reporting

Keep the final response brief:

- files edited
- categories of changes made: added, rewritten, deleted, preserved
- any comments left unchanged because intent could not be inferred
- verification performed, if any

If no paths, diffs, or code are provided and scope is not discoverable, ask for the file path, diff, or selected code.
