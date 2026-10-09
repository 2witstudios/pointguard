# pointguard

Agent tooling. Starts with universal skills; other tools land here as they come.

The skills are workflow commands that work across any project, kept separate
from [paralleldrive/aidd](https://github.com/paralleldrive/aidd) so they can
diverge freely. PageSpace-aware where it helps, never required.

## Skills

| Skill | What it does |
|---|---|
| `design` | Explore UI directions and prototypes in PageSpace Canvases, then hand off the selected revision. Codex `$design` / `/prompts:design`, OpenCode `/design`, Claude Code `/pg:design`. |
| `review` | Full code review, including an explicit OWASP Top 10 pass → publishes a review record to the repo's PageSpace drive, links it from tasks, posts the verdict on the PR. `/review` |
| `pr` | Open/update a PR whose description links the PageSpace task, plan and prompt pages. `/pr` |
| `handoff` | Hand a finished branch to review in one step: push, PR, handoff page, task moves, parent notify. `/handoff` |
| `task` | Carry an authorized objective through planning, tasking, provisional integration and independent reviews. Separate branch build inputs from main acceptance obligations; keep proof and delivery records current. `/task` |
| `triage` | Triage PR review comments, resolve already-addressed threads, delegate fix prompts to sub-agents. `/triage` |
| `rtc` | Reflective Thought Composition: restate → ideate → self-critique → expand orthogonally → score → respond. `--compact` for internal passes, `--depth N` for user-facing. `/rtc` |
| `geo-interview` | Interview AI models about GEO visibility for a product; share of voice + citation strategy. `/geo-interview` |
| `pagespace-cli` | Thin guide to the `pagespace` CLI: credentials (login vs keys), verbs, JSON/exit codes, plus an in-app-tool → CLI/SDK mapping. `/pagespace-cli` |
| `pagespace-sdk` | Thin guide to `@pagespace/sdk`: auth providers, namespaces, uploads, typed errors, custom operations. `/pagespace-sdk` |
| `pagespace-canvas-websites` · `pagespace-spreadsheets` · `pagespace-task-management` · `pagespace-writing-documents` | PageSpace's built-in page-type skills, copied verbatim from the app (`apps/web/src/lib/ai/skills/bodies`) so any agent can author CANVAS, SHEET, TASK_LIST and DOCUMENT pages. Re-copy when the app's bodies change. |

Dependencies on AIDD skills (`/aidd-fix`, `/aidd-churn`, `/aidd-javascript`,
`/aidd-tdd`, ...) are soft: each skill degrades gracefully when they are not
installed.

## Install

```sh
./install.sh          # link skills that aren't installed yet
./install.sh --force  # replace existing installs and legacy aidd-* names
```

Links each skill into `~/.claude/skills`, `~/.config/opencode/skills`, and
`~/.agents/skills`. This repo is the single source of truth — edit here, every
agent sees the change.

The design workflow has one shared skill body and thin command wrappers. Claude
Code uses `~/.claude/commands/pg/design.md` for `/pg:design`; OpenCode uses
`~/.config/opencode/commands/design.md` for `/design`; Codex discovers `$design`
through `~/.agents/skills` and also gets `/prompts:design`. These wrappers load
the shared skill without depending on Claude Design or a model provider.
To install only these new entries, run `zsh ./install-design.sh`. The installer
preserves unrelated existing entries. Restart the agents after installation.
PageSpace authoring dependencies are included in the full `./install.sh` install.

### Codex

The shared skills above are already available to Codex through `~/.agents/skills`.
Invoke them explicitly with `$task`, `$review`, `$triage`, `$rtc`, `$pr`, or
`$pagespace-cli`. These names select the PointGuard workflows, including when
Codex has a built-in command with the same name.

Install Codex slash prompts and the additional Codex-only skills separately:

```sh
zsh ./install-codex.sh
```

This links `codex-prompts/*.md` into `${CODEX_HOME:-$HOME/.codex}/prompts` and
`codex-skills/` into `${CODEX_HOME:-$HOME/.codex}/skills`. It refuses to overwrite
unrelated existing entries. It does not change Claude Code, OpenCode, the shared
skills, or plugin caches.

Custom prompts explicitly load the corresponding workflow and pass along your
arguments. Use `/prompts:task`, `/prompts:task sync <epic>`, `/prompts:triage`,
`/prompts:rtc`, `/prompts:review`, `/prompts:plan`, `/prompts:pu`, or
`/prompts:orchestrate`. Every shared PointGuard and PageSpace skill has a prompt
wrapper. Restart Codex after installing or changing prompts.

The `/prompts:` namespace distinguishes your workflows from built-in commands
such as `/plan` and `/review`. Codex custom prompts are deprecated upstream but
remain the requested explicit slash-command interface; skills remain available
alongside them. The wrappers reference this checkout's absolute paths, so
regenerate them if the checkout moves.

| Codex addition | What it does |
|---|---|
| `$plan` | Draft and independently review a plan; continue implementation only when already authorized. |
| `$orchestrate` | PurePoint's orchestration command converted into a skill. |
| `$pu-cli` | PurePoint's complete CLI command reference converted into a skill; complements the existing `$pu` awareness skill. |

The PurePoint conversions originate from the installed `pu` 0.1.0 command files.
They are independent Codex copies; check live CLI help for version-sensitive
options. Restart Codex if newly installed skills do not appear in the selector.

## Attribution

`review`, `pr` and `geo-interview` are derived from
[paralleldrive/aidd](https://github.com/paralleldrive/aidd) (MIT © 2025
Eric Elliott) and diverged from there. MIT licensed — see
[LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

## History

`review`, `pr` and `handoff` started as forks of AIDD's `aidd-review` /
`aidd-pr` / handoff flow and have since diverged (PageSpace drive records,
review-record checks, gates). `triage` and `geo-interview` were renamed from
`aidd-triage` / `aidd-geo-interview` when they moved here.
