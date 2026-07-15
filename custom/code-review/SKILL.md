---
name: code-review
description: Review a local branch before a pull request exists. Use when the user asks for a code review, branch review, pre-PR review, review of current changes, comparison against main/master/develop, readiness check before opening a PR, or PR-style findings for uncommitted, staged, committed, or named branch work. Inspect diffs, commit history, local project guidance, optional Jira context, likely PR labels, tests, security, accessibility, correctness, maintainability, and deployment risk.
disable-model-invocation: true
---

# Code Review

Find material risks before the user opens a pull request. Prioritize correctness, regressions, security, accessibility, data/API contracts, deployment risk, maintainability, and tests. Avoid style-only commentary unless it hides real risk.

## Inputs

Accept:

- current branch
- current staged or unstaged changes
- named review branch
- named base and review branches
- explicit commit range
- user-provided Jira key or task context

Ask one concise question only when the base branch or review scope cannot be inferred safely.

## Scope Rules

- Never overwrite, stash, reset, clean, checkout over, or otherwise disturb user work.
- Include staged and unstaged changes when the user asks to review current changes or current branch.
- If a remote fetch is needed and allowed, fetch only the relevant base ref. If fetch fails, continue with local refs and report freshness limits.
- If Git is unavailable or the directory is not a repo, explain that branch review cannot proceed and ask for a diff or repo path.

## Workflow

### 1. Orient

Run enough Git commands to identify scope:

```bash
git status --short
git branch --show-current
git remote -v
git branch --all --verbose --no-abbrev
```

Infer base branch in this order:

1. explicit user input
2. `origin/HEAD`
3. GitHub default branch if available
4. local `main`, `master`, `develop`, then `dev`

Set `baseRef` and `reviewRef`. For explicit ranges, preserve the range exactly.

### 2. Gather Evidence

Collect:

```bash
git diff --stat baseRef...reviewRef
git log --oneline --decorate -n 30 baseRef..reviewRef
git diff --name-status baseRef...reviewRef
git diff baseRef...reviewRef
```

For current staged/unstaged work, also collect:

```bash
git diff --cached
git diff
```

Inspect nearby code and project guidance before judging:

- `README*`, `CONTRIBUTING*`, `AGENTS.md`
- relevant docs under `docs/`
- package/build/test config
- existing tests and code around changed files

Find Jira keys in branch name, commits, changed paths, and user text. If Jira tools are available, read summary, acceptance criteria, status, labels/components, relevant comments, and linked issues. If unavailable, continue and state the gap.

### 3. Review

Read `references/review-checklist.md` before assessing findings. Look for concrete defects and pre-PR cleanup issues:

- accidental debug/local files
- missing generated files, migrations, snapshots, docs, or lockfile updates
- stale contracts, schema drift, or rollout gaps
- branch drift or merge conflict risk
- missing tests for risky behavior
- unclear release notes, migration steps, screenshots, config changes, or manual QA needs

For each finding, include evidence, impact, and a suggested fix. Use the lowest accurate severity from `references/severity.md`.

### 4. Labels And Readiness

Read `references/labels.md` and suggest labels for the eventual PR. Mark each label as suggested, questionable, or not needed. Do not imply labels were applied.

Read `references/verdict.md` and choose one final readiness verdict.

### 5. Verify

Run focused tests, type checks, lint, build, migration checks, or accessibility checks when commands are discoverable and proportionate to the risk. Prefer repo-documented commands and package scripts.

If verification is blocked by dependencies, credentials, sandbox permissions, time, missing services, or unknown commands, say exactly what was not verified.

## Parallel Agent Opportunities

When subagent tools are available and the review scope is broad enough to benefit, split review work into independent evidence streams and keep final synthesis in the parent agent. 

Good splits:

- Diff reviewer: inspect changed code for correctness, security, contracts, and regressions.
- Test reviewer: inspect nearby tests, missing risky-path coverage, and runnable verification commands.
- Context reviewer: inspect docs, Jira context when available, likely PR labels, release risk, and readiness.

Do not duplicate review areas between agents. Do not let agents mutate files. Parent agent owns severity, labels, verification summary, and final readiness verdict.

## Report

Use `references/report-template.md`.

Lead with findings. If there are no material findings, say so clearly. Use file and line references whenever possible. Keep summaries brief and secondary to review issues.

Required report sections:

- Key Findings
- Summary
- Suggested PR Labels
- Verification
- Positive Notes, only when substantive
- Final Readiness Verdict

Finding format:

```markdown
## [Severity] Title

File:
Problem:
Impact:
Suggested Fix:
```

Do not include speculative concerns without a plausible failure path. Do not bury required fixes under compliments.
