# Decision Card 0.1

Read this reference only after the user has explicitly confirmed a decision and asked to retain it or hand it to development.

## Write Boundary

- In a project containing `.vibegame/`, write one card under `.vibegame/decisions/`.
- Create the directory if needed.
- Use `<YYYY-MM-DD>-<short-kebab-slug>.md`; if that path exists, add the next numeric suffix. Never overwrite an existing card.
- Outside such a project, present the complete card in the conversation unless the user supplies an explicit destination.
- Do not write a card when confirmation is ambiguous.
- Do not write or edit the GDD, goal, task, plan, code, scene, asset, or configuration as a side effect.

## Format

```markdown
---
schema_version: "0.1"
decision_id: "YYYY-MM-DD-short-slug"
lenses: ["gameplay"]
status: "confirmed"
confirmed_at: "YYYY-MM-DD"
handoff_target: "gdd"
supersedes: null
---

# Decision: <short title>

## Context
<The problem, goal, and evidence that matter to this decision.>

## Confirmed Direction
<What the user explicitly chose.>

## Rationale
<Why this direction was chosen and the material tradeoff accepted.>

## Constraints and Cuts
- <What must remain true.>
- <What is explicitly excluded or deferred.>

## Success Signal
<The observable result or bounded experiment that tests the decision.>

## Open Questions
- <Only unresolved questions that affect later work, or "None".>
```

## Field Rules

- `lenses` contains one primary lens and at most one secondary lens.
- `handoff_target` is one of `gdd`, `goal`, `task`, `playtest-followup`, or `none`.
- Use `supersedes` only when the user explicitly replaces a prior decision; otherwise keep `null`.
- Record conclusions, constraints, and evidence pointers. Do not copy the full discussion transcript.
- A card is confirmed input, not proof that implementation or validation is complete.
