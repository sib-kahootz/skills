---
name: jira-ticket
description: Create a single Jira ticket from user-provided requirements after drafting and confirming the exact ticket details with the user. Use when the user asks to turn requirements, notes, feature ideas, bugs, acceptance criteria, or implementation tasks into one Jira issue for any Jira project or backlog.
disable-model-invocation: true
---

# Jira Ticket

## Overview

Turn rough requirements into one well-structured Jira issue. Resolve the target Jira site and project first, keep questioning the user until the required fields are known, then confirm the exact ticket details before creating or mutating anything in Jira.

## Workflow

### 1. Resolve Jira Context

Identify the target Jira site and project before drafting the final ticket. Prefer, in order:

- Explicit site, project key, or Jira link from the user
- Existing connector context that clearly identifies the right Jira workspace
- A short follow-up question when several projects or sites are plausible

Do not assume a default project, board, or sprint. If the user does not care about the exact project, ask for the intended team, product, or backlog and map that to a project only after verifying metadata.

### 2. Understand Requirements

Extract the likely Jira fields from the user's requirements:

- Summary
- Project key
- Issue type
- Description
- Acceptance criteria
- Suggested story point estimate
- Priority, if inferable
- Labels, components, or custom fields, if clearly supplied
- Links to supporting docs, tickets, PRs, screenshots, or conversations
- Open questions or assumptions

Keep asking concise follow-up questions until the required Jira creation fields are known. Do not draft or create from assumptions when required information is missing.

At minimum, establish:

- Which Jira project should receive the issue
- What needs to change or be built
- Why it is needed or what problem it solves
- Desired outcome or user or business value
- Issue type
- Clear summary
- Requirements or scope
- Acceptance criteria or how the team will know it is done
- Relevant context, source links, affected area, component, customer, or environment when applicable

For bugs, also establish expected behavior, actual behavior, impact, reproduction steps or observed conditions, and affected environment or version when known.

Ask no more than 3 questions at a time. If the user cannot provide a detail, record it explicitly as `Unknown` or `To refine` only after the user confirms that is acceptable.

### 3. Inspect Jira Metadata

Use the Atlassian Rovo or Jira connector tools. If tool names are not already loaded, discover them with `tool_search` for Jira issue creation and project metadata.

Before finalizing the draft, verify:

- The target project exists and is the right destination
- Available issue types for the project
- Required create fields for the chosen issue type
- Whether the project exposes writable estimate, component, priority, or label fields

Prefer:

- `Bug` for defects, regressions, errors, or incorrect existing behavior
- `Story` for user-facing feature or change requests
- `Task` for technical, operational, admin, or investigation work
- The closest available non-subtask issue type only when the preferred type is unavailable

If creation later fails because required fields are missing, inspect field metadata and ask the user only for those required values.

### 4. Draft Ticket

Draft the ticket only after the required information gate is satisfied and the Jira project metadata has been checked.

Suggest a story point estimate using the team's stated scale if known. If the team scale is unknown, default to a likely Fibonacci scale: `1`, `2`, `3`, `5`, `8`, `13`. Base it on scope, uncertainty, dependencies, testing effort, and cross-team coordination. Prefer:

- `1`: tiny, well-understood change
- `2`: small change with limited testing
- `3`: normal ticket with modest implementation and test work
- `5`: multi-part change, notable uncertainty, or several affected areas
- `8`: large ticket that may need splitting
- `13`: too large for a normal ticket; recommend splitting before creation

Do not write the story point value into Jira unless the user confirms it and the Jira project exposes a writable estimate field. Always include the suggested estimate in the confirmation details.

Use this structure unless the user or project metadata requires something else:

```markdown
## Background
[Why this ticket exists and relevant context.]

## Requirements
- [Specific requirement]
- [Specific requirement]

## Acceptance Criteria
- [ ] [Testable criterion]
- [ ] [Testable criterion]

## Estimate
[Suggested story points] - [short rationale]

## Notes
- [Assumption, dependency, source link, or open question]
```

Summary must name the change and affected area. Acceptance criteria must be observable and pass or fail.

### 5. Confirm Before Creating

Before calling any create, update, comment, or link tool, present the exact proposed ticket details and ask for confirmation.

Use a compact confirmation format:

```markdown
Ready to create this Jira ticket:

Site: [site URL or workspace]
Project: [project key]
Issue type: [Story/Bug/Task/etc.]
Summary: [summary]
Priority: [priority or "not set"]
Suggested story points: [points + rationale]
Labels/components: [values or "not set"]

Description:
[draft description]

Create it?
```

If the user changes anything, update the draft and confirm again. Treat `yes`, `approved`, `create it`, or equivalent as confirmation.

### 6. Create Ticket

After confirmation only, call the Jira issue creation tool with:

- The confirmed project key or project identifier
- The confirmed issue type
- The confirmed summary
- The confirmed description
- Additional fields only for confirmed or required extra values

Do not set sprint unless the user explicitly asks for sprint placement. When the user wants backlog placement, prefer leaving sprint unset unless the project workflow requires something else.

### 7. Report Result

After creation, return:

- Issue key and summary
- Browse URL
- The project it was created in
- Any fields that were defaulted, omitted, or left unset

## Safety Rules

- Never create, update, comment on, or link Jira issues before user confirmation.
- Never invent business facts, project keys, or field values; label assumptions clearly.
- Preserve user-supplied wording where it carries product meaning.
- If requirements describe several independent work items, ask whether to create one umbrella ticket or split into multiple tickets. This skill's default is one ticket.
