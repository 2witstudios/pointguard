---
name: design
description: >
  Explore UI directions, screen flows, and interactive prototypes in PageSpace
  Canvases, refine a selected design, and prepare a revision-specific handoff for
  implementation. Use for PageSpace design exploration or an explicit design
  workflow; ordinary code changes do not require this skill.
---

# PageSpace design

Turn a brief into reviewable designs stored in PageSpace CANVAS pages. This
workflow works with any coding agent; it does not depend on Claude Design,
Anthropic artifacts, a particular model, or a particular browser tool.

## Tools and destination

Before authoring, read the sibling
[Canvas authoring skill](../pagespace-canvas-websites/SKILL.md). Resolve sibling
paths against this skill's real directory when installed through symlinks.
Use available PageSpace MCP tools, the CLI, or SDK. For terminal operations,
read [pagespace-cli](../pagespace-cli/SKILL.md); for SDK code, read
[pagespace-sdk](../pagespace-sdk/SKILL.md). Discover supported operations rather
than inventing tool names or flags.

Use the drive and parent specified by the user or established by the project.
Inspect existing pages before choosing a destination or modifying a design.
If the destination is ambiguous, ask for the drive or parent while gathering
the brief and visual references. Do not create an unrelated drive. If PageSpace
access is unavailable, prepare a local HTML prototype and handoff source in the
workspace, report what could not be saved, and resume saving when access exists.
Do not claim a local file is a saved PageSpace Canvas.

Creating private design pages is part of this workflow. Publishing publicly,
sending messages, tasking an epic, and implementing the production application
require the user's request to include those actions. Honor authorization already
given; do not add approval gates to routine design work.

## Ground the design

Read enough of the existing product to understand its users, primary action,
content, navigation, and constraints. Reuse available screenshots, brand assets,
tokens, fonts, and component references. Distinguish requirements from your
assumptions; ask only for information that materially changes the design.

For an existing product, preserve its design language unless a redesign is
requested. Inspect actual component variants and states instead of guessing
from a palette. For a new identity, choose typography, layout, and color based
on the subject and audience. Use realistic copy and data that exercise the UI,
not repeated filler. Keep a compact record of token values and their sources.

## Explore and prototype

Follow the user's requested scope. For open exploration, a useful default is
two or three genuinely different directions. Vary hierarchy, information
architecture, density, or interaction approach; color swaps alone are not
different directions. When the user supplies an exact reference or wants one
screen, build that directly instead of forcing alternatives.

Use a Canvas comparison board for an overview and separate Canvas pages for
substantial directions or flows. Give every direction a stable label and every
important screen or state a stable identifier. Link related pages using the
Canvas authoring conventions. Keep comparison controls and design notes outside
the product UI; a prototype should read like the product its users would use.

Use inline HTML/CSS/JS. Build meaningful interactions with in-memory state and
represent relevant empty, loading, error, success, and disabled states where
they affect the flow. Record simulated behavior in design notes. Do not make
fake purchases, authentication, data saves, or submissions appear connected to
a backend. Existing provisioned forms follow the Canvas skill's exact rules.

Carry over tokens and component appearance accurately. An HTML/CSS recreation
is not the original React component. If actual components are needed, inspect
their dependencies and use a verified build that emits Canvas-compatible
inline code; external scripts and API access remain subject to Canvas CSP.
Do not relax the sandbox to make a prototype work.

Text editing, spacing sliders, and other custom prototype controls can modify
the preview, but do not promise autosave. Canvas content cannot call PageSpace
APIs to persist those changes. Save revisions through the agent's PageSpace
tools; preserve any user edits before replacing content.

## Inspect and refine

Render and inspect screenshots when browser tooling is available. Prefer the
actual in-app Canvas; a local preview helps diagnose layout but does not verify
PageSpace sanitization, theme injection, file rewriting, or CSP. Check desktop
and narrow mobile widths, both themes, overflow, text wrapping, primary flows,
keyboard focus, contrast, and reduced motion as relevant to the design.

Fix visible problems and blocked assets before presenting a direction as ready.
Read back saved content to verify the edit landed. State which rendering and
interaction checks were performed and any checks unavailable in the environment;
never substitute a source-code read for a claimed visual inspection. Do not
publish just to run a check unless publishing is already authorized.

Present links to the alternatives, their meaningful differences, and a concise
recommendation. Let the user choose when the request calls for a choice. When
selection is delegated, choose and explain the tradeoff. Continue independent
polish while waiting, but do not treat silence as selection.

Refine the chosen direction through the user's feedback. Refer to stable screen
and element identifiers for targeted changes. Preserve earlier alternatives;
before a substantial new direction or handoff, make a named snapshot instead of
overwriting the sole copy. Never describe snapshots as native version history.

## Handoff

When handoff is requested or the chosen design is ready, save concise design
notes alongside the Canvases using the available DOCUMENT or CODE operations.
For a local fallback, keep equivalent notes and source files in the workspace.
Include:

- The brief, chosen direction, Canvas links and page IDs, and unresolved choices.
- The exact selected source: a saved HTML snapshot with a SHA-256 digest and
  timestamp, or a verified immutable revision identifier if the tool exposes one.
  A mutable Canvas URL alone is not a revision reference.
- Tokens, assets, fonts, and component mappings, identifying recreations versus
  original components and required production dependencies.
- Screen/state identifiers, navigation, responsive behavior, and interactions,
  including simulations and the backend work still needed.
- Observable acceptance criteria and visual/interaction verification results.

An implementing agent should read this selected revision and map it to the
repository's components and architecture. Do not ask it to implement a comparison
board or discard existing application behavior. If implementation is requested,
continue with the repository's normal workflow; otherwise finish with the design
links, chosen revision when available, and remaining decisions.
