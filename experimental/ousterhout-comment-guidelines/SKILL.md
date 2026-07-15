---
name: ousterhout-comment-guidelines
description: Review, add, rewrite, or remove source-code comments using John Ousterhout's interface-focused principles. Use when the user requests Ousterhout-style comments, wants documentation that captures abstractions and design decisions, or needs a comment review focused on what clients need to know rather than implementation detail.
disable-model-invocation: true
---

# Ousterhout Comment Guidelines

Edit comments directly when code paths or a diff are available. Preserve runtime behavior; report design problems instead of changing code unless the user explicitly requests code changes.

## Comment at the Interface

Write comments for the reader of an abstraction, not the implementer of its current body. Explain the abstraction's purpose, interface, guarantees, constraints, side effects, and the information callers need to use it correctly.

- Document the overall abstraction before its operations when it has a non-obvious purpose or model.
- Explain each public method, parameter, result, error, and side effect that a caller cannot safely infer from its name and type.
- State the semantics of configuration, state, callbacks, ordering, ownership, lifecycle, concurrency, and failure behavior where they form part of the contract.
- Keep implementation details out of interface comments unless clients must rely on them.

## Capture Design Decisions

Use comments to preserve information that the code cannot express clearly: why a design was chosen, what alternative was rejected, compatibility constraints, invariants, performance or security tradeoffs, and external workarounds.

Do not invent rationale. If it cannot be established from the code, tests, issue references, or nearby context, leave the comment unchanged or ask for context.

## Avoid Duplication and Low-Level Narration

Use different words from the code: the comment should add information, not restate identifiers, types, syntax, or obvious control flow.

- Delete comments that translate the next line into English.
- Do not describe the body of a method line by line.
- Prefer a precise comment over a vague label such as `helper`, `magic`, `simple`, or `handles errors`.
- Do not rely on better names alone when readers still need an explanation of the abstraction or contract.

## Review Workflow

1. Identify the reader: caller, maintainer, or both.
2. Read the surrounding abstraction, its call sites, tests, and local documentation style.
3. Classify each relevant comment as `keep`, `delete`, `rewrite`, or `add`.
4. Prefer comments at the highest useful abstraction level: module, class, interface, then method or local block.
5. Recheck every edited comment against the code. Ensure it is true, client-relevant, and adds information the code does not convey.
6. Report the comments added, rewritten, deleted, and any design rationale that could not be inferred.

## Signs of a Comment Problem

Flag rather than refactor these conditions unless code changes are requested:

- The comment must expose many implementation details for clients to use the API.
- Each method needs extensive explanation because the abstraction lacks a clear model.
- The public interface reveals complexity that could be hidden behind a deeper module.
- Repeated comments are needed to explain a cross-cutting invariant that has no clear owner.
