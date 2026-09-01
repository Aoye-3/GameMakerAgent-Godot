---
name: game-delivery
description: Deliver a confirmed game feature into an existing Godot project when gameplay intent, generated assets, code, scenes, and runtime acceptance must stay aligned. Do not use for advisory-only discussion or ordinary isolated bug fixes.
---

# Game Delivery

Use Codex as the orchestrator and mature asset/Godot providers as executors. Never build or expose a second Agent Runtime or a new general Godot MCP.

1. Require an existing native Godot project. Run `gamemaker doctor`; report missing third-party capabilities instead of installing or simulating them.
2. Run `gamemaker query` with terms from the confirmed feature. Use only the returned task-local facts and revision.
3. Form a minimal Production Card: player outcome, beat, reuse, genuinely new assets, and observable acceptance claims.
4. For each new 2D image, form an Asset Spec with role, style, player read, PNG dimensions, frames, transparency, pivot, trim, provenance, license, stable asset ID, and target `res://` path.
5. Send only the Asset Spec to the selected mature asset provider. Validate and normalize its output before Godot receives it.
6. Form a Godot Binding that maps the normalized artifact to Resource type, import options, scene/node path, animation/collision facts, and verification claims.
7. Give the coding step only the confirmed decision, Production Card, task-local project context, normalized assets, bindings, and acceptance. Use the available mature Godot MCP through its adapter profile; keep its raw tool names out of public artifacts.
8. Record changed Godot files and binding IDs in an Implementation Record tied to the resulting source revision.
9. Run the project through the available Runtime Provider and collect current state, screenshot, diagnostics, inputs, and revision into an Evidence Bundle.

Do not claim completion for an isolated image, unbound code, successful tool call, stale run, or incomplete evidence. Stop at the smallest failed boundary and return the normalized category.
