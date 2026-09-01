---
name: evidence-review
description: Review whether a Godot game feature is supported by current static, runtime-state, visual, and diagnostic evidence. Use for completion review or re-verification, not to implement the feature.
---

# Evidence Review

Review claims, not effort or tool success.

1. Load the Production Card acceptance claims, Implementation Record, Godot Bindings, Evidence Bundle, and current project revision.
2. Reject evidence whose implementation ID or source revision differs from the current implementation.
3. Evaluate separately:
   - static evidence: required scene, script, Resource, input and binding facts exist;
   - runtime state: the recorded input trace produces the required observable state;
   - runtime visual: current screenshots show the intended player-visible result;
   - diagnostics: no error invalidates the claim.
4. Map every acceptance claim to evidence. A screenshot alone cannot prove hidden state or interaction behavior.
5. Return exactly one verdict:
   - `PASS`: every claim has current sufficient evidence and no invalidating diagnostic;
   - `FAIL`: current evidence demonstrates a broken claim;
   - `INSUFFICIENT_EVIDENCE`: evidence is missing, stale, ambiguous, or cannot establish the claim.

State the smallest failed boundary and the cheapest bounded re-run. Do not edit the project, repair files, invoke generation, or reinterpret human judgments such as whether the game feels good.
