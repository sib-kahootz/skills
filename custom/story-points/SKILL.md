---
name: story-points
description: Estimate story points for sprint stories from a Jira ticket link first, falling back to a pasted story description when Jira is unavailable or no link is provided. Use when the user asks to size, estimate, point, score, or allocate story points to a Jira issue, backlog item, sprint story, bug, spike, or change request.
---

# Estimate Story Points

## Overview

Estimate story points by reading the work item, comparing scope against risk and uncertainty, and returning a defensible point recommendation. Prefer the team's existing calibration when it is available.

## Input Handling

1. If the user provides a Jira ticket link or issue key, use available Jira or Atlassian tools to retrieve the issue before estimating.
2. Read the summary, description, acceptance criteria, comments, linked issues, subtasks, labels, components, priority, and any design or technical notes that are visible.
3. If Jira cannot be reached, the link cannot be resolved, or the user provides no link, estimate from the pasted description and state that the estimate is based only on pasted context.
4. When a relevant local checkout is available, do a quick code-path scan before estimating and cite the likely files or modules that drive the estimate.
5. If the input is too thin to estimate responsibly, ask for the smallest missing detail that would change the estimate, such as acceptance criteria, affected system, integration points, or test expectations.

## Jira Write-Back

When the estimate is based on a Jira issue and Jira write access is available, include a short offer to apply the recommended story point value to the ticket and add the rationale as a Jira comment. Do not update Jira until the user explicitly confirms.

After confirmation, update the story point field with the recommended value and add a concise comment that includes the estimate, confidence, main rationale, and any material uncertainty or split recommendation. If either write operation fails, report exactly what was and was not changed.

## Estimation Guide

Read [references/estimation-guide.md](references/estimation-guide.md) after collecting the Jira or pasted story context. Use it for the estimation workflow, default scale, uncertainty checks, and response format.
