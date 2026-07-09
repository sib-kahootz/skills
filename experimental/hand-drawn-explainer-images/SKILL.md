---
name: hand-drawn-explainer-images
description: >-
  Create explainer images with a polished hand-drawn infographic style: large hand-lettered title, content-led layout, labeled cards or sections, arrows, icons, checklists, small doodles, and limited accent colors. Use when the user asks to generate, edit, or prompt for illustrated explainer images, visual summaries, personal/team role maps, product explainers, concept posters, capability maps, or infographic-style images inspired by a provided reference image. Prefer deterministic SVG/PDF/HTML output over raster AI generation when exact wording, dense tables, or full source-document coverage is required.
---

# Hand-Drawn Explainer Images

## Workflow

1. Extract every provided fact, label, role, relationship, constraint, and required phrase from the user request.
2. If the source is a file, extract its content first and preserve the source structure where it carries meaning, such as table columns, ordering, headings, numbering, or labels.
3. Ask only for missing factual content that cannot be reasonably inferred.
4. Read `references/style-guide.md` before producing the visual.
5. Choose the output method:
   - Use raster image generation when the visual can tolerate approximate typography and short labels.
   - Use deterministic SVG, PDF, HTML, or slide generation when exact spelling, dense text, tables, many named items, or "include all information" is required.
6. Choose a layout that suits the extracted information.
7. For raster generation, produce an image prompt that specifies composition, text hierarchy, illustration style, palette, subject treatment, panels, icons, and negative constraints.
8. For deterministic generation, encode the extracted facts as structured data and render exact text into the visual using the same style guide.
9. Include every extracted fact either as visible text, a labeled icon, a section, a relationship arrow, or an illustrated scene detail.
10. If generating directly, create the visual artifact. If providing a prompt only, give one final prompt and a short note about any assumptions.

## Output Method Decision

- Use deterministic output when the user says "include all information", "exact wording", "from this document/PDF/table", "do not omit anything", or when there are more than about 12 labels, bullets, rows, names, or stages.
- Use deterministic output for tables, process matrices, compliance checklists, schedules, inventories, and source documents where spelling and completeness matter more than painterly texture.
- Use raster image generation for conceptual posters, role maps, illustrated metaphors, mood-driven summaries, and light text where minor visual interpretation is acceptable.
- If the requested hand-drawn style conflicts with exact-text density, preserve exact content first and apply the style through layout, icons, paper texture, color, hand-drawn outlines, and typography.
- If a write or render step fails in the current workspace, switch to another deterministic artifact format before dropping content.

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
- If exact supplied text must remain visible, do not compress or paraphrase it unless the user permits summarization.
- If the image would become too dense, use a larger canvas, multiple panels, deterministic SVG/PDF/HTML, or split information into clearly separated sections before omitting anything.

## Output Expectations

- For direct generation, call the image generation tool with one complete prompt.
- For exact-text or dense-source tasks, create a deterministic artifact and verify that the expected items are present.
- For prompt-only requests, return one final prompt, not a long explanation.
- For iterations, preserve the established layout unless the user asks for a structural change.
