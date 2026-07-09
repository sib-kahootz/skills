---
name: hand-drawn-explainer-images
description: >-
  Create raster explainer images with a polished hand-drawn infographic style: large hand-lettered title, content-led layout, labeled cards or sections, arrows, icons, checklists, small doodles, and limited accent colors. Use when the user asks to generate, edit, or prompt for illustrated explainer images, visual summaries, personal/team role maps, product explainers, concept posters, capability maps, or infographic-style images inspired by a provided reference image.
---

# Hand-Drawn Explainer Images

## Workflow

1. Extract every provided fact, label, role, relationship, constraint, and required phrase from the user request.
2. Ask only for missing factual content that cannot be reasonably inferred.
3. Read `references/style-guide.md` before writing an image prompt.
4. Choose a layout that suits the extracted information.
5. Produce an image-generation prompt that specifies composition, text hierarchy, illustration style, palette, subject treatment, panels, icons, and negative constraints.
6. Include every extracted fact in the prompt, either as visible text, a labeled icon, a section, a relationship arrow, or an illustrated scene detail.
7. If generating directly, use the image tool with the finished prompt. If not generating directly, give the user the prompt and a short note about any assumptions.

## Prompt Structure

Use this order when writing prompts:

1. Format and purpose: "wide illustrated explainer poster" or the requested aspect ratio.
2. Main subject or topic: person, product, process, concept, organization, timeline, comparison, map, or system.
3. Title and subtitle text.
4. Layout: choose a structure that fits the information, such as radial map, grid, timeline, flow, comparison, layered stack, annotated scene, or role cards.
5. Card content: short headings, concise bullets, icons, and color accents.
6. Visual treatment: hand-drawn ink lines, soft watercolor shading, warm off-white paper, playful but legible lettering.
7. Coverage controls: include all supplied information and preserve exact names, titles, labels, numbers, and required phrases.
8. Quality controls: accurate spelling, no cramped text, no extra unreadable words, no photorealistic corporate template look.

## Text Rules

- Keep generated image text short enough to fit: headings under 5 words, bullets under 6 words where possible.
- Use sentence case for subtitles and compact title case for card headings.
- Tell the image model to preserve exact supplied names, titles, and labels.
- When the user provides lots of prose, transform every point into image-safe labels, bullets, callouts, icons, or scene details instead of dropping lower-priority information.
- If the image would become too dense, use a larger canvas or split information into clearly separated sections before omitting anything.

## Output Expectations

- For direct generation, call the image generation tool with one complete prompt.
- For prompt-only requests, return one final prompt, not a long explanation.
- For iterations, preserve the established layout unless the user asks for a structural change.
