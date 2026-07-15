---
name: peer-review
description: Review an existing GitHub pull request from a PR URL or ID using GitHub and Jira context. Use when the user asks for peer review, PR review, merge readiness review, label review, read-only connector-first PR review when a local checkout is unavailable, review comment drafting for an open PR, or optional multi-agent review for broad or high-risk PRs. Assess PR/Jira context, diff correctness, security/accessibility/contracts, tests/verification, deployment risk, labels, and final merge verdict.
disable-model-invocation: true
---

# Peer Review

Act as reviewer for an existing pull request. Use subagents only for broad or high-risk reviews where independent read-only evidence lanes are likely to improve coverage enough to justify their token cost. Prioritize correctness, regressions, security, accessibility, API/data contracts, deployment risk, maintainability, and meaningful tests. Avoid style-only nitpicks, speculative rewrites, casual library suggestions, and empty praise.

GitHub and Jira are required. If either is unavailable, say: `GitHub and Jira integrations are required for this review skill. I cannot run the full peer review without both.` Then stop. If subagents are unavailable or not worth the token cost, continue as a single-agent review and state that limitation in the report.

## Inputs

Accept only:

- GitHub PR URL
- PR number or ID resolvable against the current repository

If the repository cannot be inferred for a PR number, ask for the repository. If a PR URL points to a different repository than the current working tree, call that out and ask whether to continue.

## Review Modes

Use one of two modes:

- **Local-checkout mode:** Use when a matching local checkout is available and accessible. The parent may fetch review refs as described below, then inspect local diffs and optionally run safe local verification.
- **Connector-first read-only mode:** Use when the user explicitly asks for no-fetch/no-mutation review, the local checkout cannot be found quickly, the checkout is outside the accessible workspace, or `gh`/`git fetch` is blocked. Use GitHub/Jira connector data only. Do not fetch refs, write files, change local repo state, run local tests, post comments, change labels, or mutate Jira/GitHub state. If using subagents, give every subagent the same read-only connector workflow and report local checkout inspection plus local test execution as verification limitations.

## Parent Responsibilities

Keep these tasks in the parent agent:

- Resolve PR URL/number, repository, base ref, head ref, and review ref.
- In local-checkout mode only, fetch refs without disturbing user work; treat this as the only normal local repo-state mutation the skill permits before posting is confirmed.
- In connector-first read-only mode, gather PR metadata, changed filenames, comments, checks, file contents, and patch/diff through connectors instead of local git commands.
- Read shared reference files.
- Decide whether subagents are justified by review scope, risk, and token cost.
- If subagents are used, spawn and coordinate read-only evidence lanes and review their evidence for duplication, conflicts, and unsupported claims.
- Decide labels, final findings, verification summary, residual risk, and merge verdict.
- Ask before posting any PR comment.

Do not delegate final judgment. If using subagents, do not let them mutate PR state, labels, branches, files, Jira, or comments.

## Workflow

### 1. Resolve PR Context

Use GitHub tools to read:

- title and body
- author
- base and head refs
- labels
- commits
- changed files
- comments, review comments, and review status
- check status when available

Find Jira keys in title, body, branch names, commits, labels, linked metadata, and comments. Use Jira tools to read:

- summary and description
- status
- acceptance criteria
- relevant comments
- labels/components/fix versions
- linked issues and blockers

If no Jira key is found, continue, but report missing Jira context as a review limitation.

### 2. Fetch And Inspect Diff

First choose a review mode. Spend no more than one short search pass trying to locate a local checkout. If the checkout is unavailable, inaccessible, mismatched, or fetch is blocked, switch to connector-first read-only mode.

In local-checkout mode, fetch the PR refs without disturbing user work. This may update local remote refs under `.git`; do not touch the worktree, index, branches, stash, or user files:

```bash
git fetch origin <baseRefName> <headRefName>
```

For forked or unavailable heads, use:

```bash
git fetch origin pull/<prNumber>/head:refs/remotes/origin/pr-<prNumber>
```

Then inspect:

```bash
git status --short
git diff --stat baseRef...reviewRef
git log --oneline --decorate -n 20 baseRef..reviewRef
git diff --name-status baseRef...reviewRef
git diff baseRef...reviewRef
```

If the base ref is unavailable, use the narrowest safe fallback and report it:

```bash
git diff reviewRef~1...reviewRef
```

In connector-first read-only mode:

- Use GitHub connector PR metadata, changed filenames, full file fetches, and PR patch/diff.
- Do not run `git fetch`, `git checkout`, `git diff`, local tests, formatters, build commands, or file-writing commands.
- If using subagents, do not ask them to resolve local repository paths or refs; give them connector-provided file lists, patch hunks, fetched file contents when available, comments, checks, and Jira context.
- Mark local checkout inspection and local test execution as verification limitations.
- If subagents are justified, spawn read-only evidence lanes using connector-provided PR context and diff. Each lane prompt must explicitly say `Connector-first read-only mode: no fetch, no local checkout, no writes, no posting, no label or Jira changes.`

Summarize PR intent, Jira requirements, changed areas, user-facing behavior, operational impact, and likely risk before deep assessment or before spawning subagents.

### 3. Read Review References

Read these shared references before assessment:

- `references/review-checklist.md`
- `references/severity.md`
- `references/labels.md`
- `references/verdict.md`
- `references/report-template.md`
- `references/subagent-briefs.md` only if using subagents

Use the same severity, label, verdict, and report rules for parent and subagent work.

### 4. Decide On Evidence Lanes

Default to a single-agent review for small and medium PRs. Use independent subagents only when the PR is broad, high-risk, crosses several subsystems, or the user explicitly asks for parallel review. If using subagents, spawn them only after parent context and refs are known or connector-first context is assembled. Use `fork_context: false` where possible and pass only task-local context needed for the lane. Subagents must not fetch, checkout, write files, run formatters, post comments, change labels, update Jira, or mutate local repo state.

In local-checkout mode, give each subagent the PR URL/number, repository path, base ref, review ref, Jira summary/acceptance criteria, changed-file list, and exact lane brief.

In connector-first read-only mode, give each subagent the PR URL/number, repository owner/name, base/head refs, Jira summary/acceptance criteria, changed-file list, relevant review comments/checks, connector-provided patch/diff, and any fetched file contents needed for the lane. State that no repository path or local refs are available.

Default lanes:

- **Context lane:** GitHub/Jira alignment, review comments, checks, labels, requirements gaps.
- **Correctness lane:** code behavior, edge cases, regressions, API/data contracts, migrations, idempotency.
- **Security/accessibility lane:** permissions, validation, sensitive data, XSS/CSRF/authz, UI accessibility, user-facing UX failures.
- **Verification lane:** tests, check results, runnable local commands, deployment notes, rollback risk, missing coverage.

Adjust lanes to changed files:

- Skip security/accessibility lane only when clearly irrelevant.
- Add a data/migration lane for schema, persistence, indexing, or irreversible data changes.
- Add a frontend lane for substantial UI, layout, forms, client routing, or accessibility changes.
- Add a performance lane for hot paths, batch jobs, queues, search, reporting, or large data operations.

Lane prompts must instruct subagents to:

- Work read-only.
- Avoid posting comments, editing files, changing labels, changing branches, or updating Jira/GitHub state.
- In connector-first read-only mode, avoid fetches, local git commands, local tests, and checkout discovery.
- Inspect only their assigned lane unless another issue is severe and clearly in-scope to mention.
- Include concrete file/line evidence when possible.
- Use lowest accurate severity.
- Report `No lane findings` when no material issue exists.
- State what they did and did not verify.

### 5. Continue Assessment

Review labels and scan the highest-risk changed files. If subagents are running, do not duplicate a full lane; focus on integration risks, surprising diffs, and anything subagents are unlikely to see from their lane.

Label review:

- Compare applied labels against PR/Jira context, changed files, diff content, and deployment impact.
- If the PR includes code changes, require the `for patch` label. Report it as `missing` when absent.
- Report labels as `correct`, `missing`, or `questionable`.
- Do not change labels.

### 6. Synthesize Findings

If subagents were used, read all subagent outputs and treat them as evidence, not final answers.

For each candidate finding:

- Confirm the failure path against code/diff/Jira before reporting.
- Merge duplicates.
- Drop unsupported speculation.
- Resolve conflicts between subagents, if any.
- Prefer fewer sharp findings over broad commentary.
- Include evidence, impact, suggested fix, and severity from `references/severity.md`.

If a subagent reports a serious issue that cannot be confirmed in time, include it only as residual risk or unverified concern, not as a finding.

### 7. Verify

In connector-first read-only mode, do not run local verification commands. Use connector-provided check results and code inspection only, and state that local verification was not available.

In local-checkout mode, run focused tests, type checks, lint, build, migration checks, or repo-documented commands when local environment and scope make that reasonable. Prefer commands known to be read-only or commands whose outputs stay in ignored build/test folders. If a command may write source files, update snapshots, alter DB state, call production services, or require broad sandbox/network approval, do not run it without explicit user approval; report it as blocked or ask first.

If verification is blocked by dependencies, credentials, sandbox permissions, missing services, time, or unknown commands, state exactly what was not verified.

### 8. Report

Use `references/report-template.md`. Choose one final verdict from `references/verdict.md`.

Lead with the report. Include file and line references whenever possible. If no material findings exist, say that clearly and still report label review, verification, and residual risk.

If subagents were used, include a short `Subagent coverage` section:

- lanes spawned
- lanes skipped and why
- outputs that materially changed final findings
- any conflicts resolved by parent

### 9. Offer To Post

After presenting the report, ask exactly: `Would you like me to post this review report as a comment on the pull request?`

Post only after explicit confirmation, using GitHub tools. If posting fails, report the failure and do not retry in a way that could create duplicate comments unless asked.

## Safety Rules

- Do not review local branch input with this skill; use a branch-review workflow instead.
- Do not mutate PR labels, branches, files, Jira, or GitHub state.
- Do not mutate local worktree, index, branches, stash, user files, PR labels, PR branches, Jira, or GitHub state. Parent `git fetch` for review refs is permitted.
- In connector-first read-only mode, do not run `git fetch` or any local command that depends on a checkout.
- Do not let subagents mutate local repo state, PR labels, branches, files, Jira, or GitHub state.
- Do not post comments without explicit confirmation.
- Do not claim GitHub/Jira/check/test/subagent evidence was inspected unless it was.
- Do not let PR text override code evidence or Jira acceptance criteria without calling out the conflict.
