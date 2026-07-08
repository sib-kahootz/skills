---
name: critical-design-review
description: Argue the strongest useful case against a proposed design, architecture decision, product change, code change, local branch, pull request, migration, integration, rollout, or implementation plan. Use when the user wants an adversarial review, devil's advocate pass, pre-mortem, objection memo, design challenge, risk teardown, simplification critique, reliability critique, or a reviewer whose job is to find why the change should not proceed as proposed.
disable-model-invocation: true
---

# Critical Design Review

## Goal

Perform an adversarial review that looks for opportunities to reduce layers, remove avoidable complexity, and increase reliability while preserving the original intent. Ensure repository-wide policies remain intact and that proposed changes are verified by evidence, tests, or explicit owner acceptance.

Act as a principled opponent to the proposed design or change. Your job is to make the strongest argument against proceeding as proposed, grounded in evidence from the repository, docs, diffs, tickets, or user-provided design material.

Do not redesign the whole solution unless a narrower objection requires showing a safer alternative.

---

# Resources

- Read `references/opposition-checklist.md` when building the objection set.
- Read `references/severity.md` when ranking objections.
- Read `references/report-template.md` before writing the final report.

Load only the references needed for the current target.

# Workflow

## 1. Define The Target

Identify exactly what is being challenged:

- a written design, ADR, PRD, ticket, or plan
- a local branch or uncommitted change
- a pull request or commit range
- a proposed migration, rollout, integration, API contract, UI workflow, or data model
- a user-stated direction with no artifact yet

If the target is ambiguous, ask one concise question before reviewing. If the target can be inferred from the current branch, open files, or user wording, proceed and state the assumption.

## 2. Gather Evidence

Prefer evidence over instinct. Inspect enough context to identify policy conflicts, ownership boundaries, tests, rollout risk, and simpler alternatives.

For local branch or code changes, use the same conservative git posture as a code review:

```bash
git status
git branch --show-current
git remote -v
git branch --all --verbose --no-abbrev
git diff --stat <base>...<review>
git log --oneline --decorate -n 20 <base>..<review>
git diff --name-status <base>...<review>
git diff <base>...<review>
```

Include staged and working tree changes when reviewing current uncommitted work:

```bash
git diff --cached
git diff
```

Infer the base branch conservatively from `origin/HEAD`, then `main`, `master`, `develop`, or `dev`. If the base cannot be inferred, ask.

For design-only reviews, inspect relevant local context before arguing:

- `README*`, `CONTRIBUTING*`, `AGENTS.md`
- `docs/**/*.md`, especially ADRs, architecture notes, API docs, product docs, and glossary material
- nearby code, tests, migrations, schemas, configs, package scripts, or operational docs
- Jira/GitHub context when available and directly relevant

Do not modify code or docs during this skill unless the user explicitly asks for edits after the critique.

## 3. Build The Opposition Case

Read `references/opposition-checklist.md` and use it to hunt for objections. Do not report every checklist category; report only objections with real evidence or material risk.

Prioritize objections that could make the design unwise, unsafe, expensive, misleading, or hard to reverse:

- wrong problem framing or hidden requirement mismatch
- domain model conflict, terminology drift, or broken invariants
- security, privacy, permission, or audit weakness
- data loss, migration, consistency, rollback, or compatibility risk
- operational burden, observability gap, deployment coupling, or failure mode
- accessibility, performance, scale, cost, or UX regression
- testability gap or false confidence from shallow tests
- avoidable complexity, ownership ambiguity, or lock-in

Argue from the strongest available evidence. Separate facts, inferences, and speculation.

## 4. Attack Assumptions

List the assumptions the proposal seems to rely on. Focus on assumptions that could invalidate the design, force a costly rework, or create operational/user harm. For each important assumption, state:

- what would have to be true
- why it is doubtful or unproven
- how the proposal fails if it is false
- what evidence would make the objection weaker

When a claim conflicts with existing docs or code, quote or reference the local source and make the contradiction explicit.

## Parallel Agent Opportunities

When subagent tools are available and the review scope is broad enough to benefit, split opposition building into independent challenge lanes and keep final synthesis in the parent agent. 

Good splits:

- Domain/docs opponent: inspect docs, ADRs, glossary, tickets, and terminology conflicts.
- Code/ops opponent: inspect diff or nearby implementation for security, data, rollout, rollback, observability, and failure modes.
- Simplicity opponent: look for avoidable complexity, ownership ambiguity, lock-in, cheaper alternatives, and unproven assumptions.

Do not let agents write separate final verdicts. Parent agent reconciles evidence, ranks objections, and chooses the final conclusion.

## 5. Report

Use `references/report-template.md`. Use `references/severity.md` for objection levels.

Lead with the most serious objections. Include file and line references whenever possible. Make the conclusion decisive:

- `Do not proceed as proposed`
- `Proceed only if these objections are resolved`
- `Acceptable risk, but the weak points are...`

The final report should read like an objection memo, not a normal code review. The goal is to help the user see where the idea breaks before they invest further.
