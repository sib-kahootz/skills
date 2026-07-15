---
name: deskpro-to-jira
description: Create Jira tasks from Deskpro ticket URLs. Use when Codex is given a Deskpro support ticket link and asked to inspect, summarize, convert, raise, log, or create a Jira issue from it, especially when the Jira site, project, issue fields, user confirmation, or missing support-ticket details are needed before creating the Jira ticket.
disable-model-invocation: true
---

# Deskpro to Jira

## Overview

Convert a Deskpro support ticket URL into a confirmed Jira Task. Retrieve the ticket through an authenticated browser/session when possible, ask the user only for missing or ambiguous information, then draft and confirm the Jira fields before creation.

## Workflow

1. Open the Deskpro ticket URL using the user's authenticated browser/session when available.
2. Extract the useful ticket facts:
   - Deskpro ticket URL and visible ticket ID/reference.
   - Customer or reporter context, redacting customer-identifying details unless the user wants them included.
   - Subject, description, requested outcome, business impact, priority/urgency, affected site/account, attachments or screenshots, and relevant conversation notes.
   - Reproduction steps, actual result, expected result, and error details when the ticket describes broken existing behavior.
3. If browser retrieval fails because authentication or access is unavailable, ask the user to either open the ticket in the authenticated browser or paste the ticket content. Do not guess ticket details from the URL alone.
4. Identify the minimum missing information needed to create a useful Jira Task. Ask only targeted questions for missing or ambiguous fields, usually Jira site/base URL, Jira project key, summary, expected outcome, priority, component/team when required, and whether customer-identifying details may be included.
5. Draft the Jira issue and show it to the user for confirmation before creating it.
6. Create the Jira issue only after the user confirms the draft.
7. If a Deskpro-Jira integration exists in the Deskpro ticket UI or available tools, link the newly created Jira issue to the Deskpro ticket.
8. Return the Jira issue key and URL, the Deskpro link status, and any Deskpro follow-up note the user may want to post.

## Jira Requirements

- Jira site/base URL: ask the user unless already provided in the request or current context.
- Project: ask the user for the Jira project key unless already provided in the request or current context.
- Issue type: `Task`
- Label: `Support`
- Source link: include the Deskpro ticket URL in the Jira description.
- Deskpro link: link the Jira issue back to the Deskpro ticket through the Deskpro-Jira integration when available.
- Confirmation: required before creating the Jira issue.

Use other fields such as priority, components, assignee, sprint, or fix version only when they are present in the Deskpro ticket, required by Jira, or supplied by the user.

## Draft Format

Before creating Jira, present a concise draft:

```markdown
Jira site: ...
Project: ...
Issue type: Task
Summary: ...
Priority: ...
Labels: Support
Components/Team: ...

Description:
...

Open questions:
- ...
```

If open questions remain, ask the user to answer them before creation unless the user explicitly says to create the Jira ticket with the current draft.

## Deskpro Linking

After Jira creation, look for an existing Deskpro-Jira integration action in the Deskpro ticket UI or available tools. Use it to link the created Jira issue to the Deskpro ticket when possible.

If no integration is visible, unavailable, or blocked by permissions, do not improvise an unsupported link action. Tell the user that the Jira issue was created but not linked in Deskpro, and remind them to link the Deskpro and Jira tickets manually.

## Description Template

Use this structure unless the ticket content calls for a more natural format:

```markdown
Deskpro ticket: <url>

Summary
<one or two sentences>

Customer impact
<impact, urgency, affected customer/site if allowed>

Requested outcome
<what support/customer needs>

Details
<relevant Deskpro notes, errors, screenshots, attachments, links>

Acceptance criteria
- <testable outcome>
- <testable outcome>
```

For defect-like tickets, include:

- Steps to reproduce
- Expected result
- Actual result
- Frequency and affected environment, if known
