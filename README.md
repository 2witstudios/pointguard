# skills

Jono's universal agent skills — workflow commands that work across any project,
kept separate from [paralleldrive/aidd](https://github.com/paralleldrive/aidd)
so they can diverge freely. PageSpace-aware where it helps, never required.

## Skills

| Skill | What it does |
|---|---|
| `review` | Full code review → publishes a review record to the repo's PageSpace drive, links it from tasks, posts the verdict on the PR. `/review` |
| `owasp-review` | Dedicated OWASP Top 10 security pass over a diff. `/owasp-review` |
| `pr` | Open/update a PR whose description links the PageSpace task, plan and prompt pages. `/pr` |
| `handoff` | Hand a finished branch to review in one step: push, PR, handoff page, task moves, parent notify. `/handoff` |
| `triage` | Triage PR review comments, resolve already-addressed threads, delegate fix prompts to sub-agents. `/triage` |
| `geo-interview` | Interview AI models about GEO visibility for a product; share of voice + citation strategy. `/geo-interview` |

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

## History

`review`, `pr` and `handoff` started as forks of AIDD's `aidd-review` /
`aidd-pr` / handoff flow and have since diverged (PageSpace drive records,
review-record checks, gates). `triage` and `geo-interview` were renamed from
`aidd-triage` / `aidd-geo-interview` when they moved here. `owasp-review` was
extracted from `review`'s security criteria to stand alone.
