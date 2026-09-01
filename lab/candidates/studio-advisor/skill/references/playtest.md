# Playtest Lens

Use this lens when actual player behavior, runtime evidence, screenshots, traces, diagnostics, or structured notes exist.

## Separate Evidence From Interpretation

Organize the available information into:

- **Observation:** what the player did, said, missed, repeated, or abandoned;
- **Context:** build revision, player familiarity, platform, input method, test goal, and session conditions;
- **Interpretation:** a plausible explanation of the observation;
- **Confidence:** how strongly the evidence supports that explanation;
- **Evidence gap:** what would distinguish competing explanations.

Player suggestions are observations about dissatisfaction or desire, not automatically the correct solution.

## Evaluation Axes

- **Reproducibility:** Did the behavior recur across attempts or players? Can the same state be reached again?
- **Severity:** Does it block progress, hide the intended experience, create unfairness, or merely reduce polish?
- **Frequency and exposure:** How often can it happen, and how many players or sessions encounter it?
- **Design intent conflict:** Is the implementation failing the intended experience, or is the intended experience itself weak?
- **Signal agreement:** Do player behavior, verbal feedback, structured state, screenshots, and diagnostics support the same conclusion?
- **Alternative causes:** Could onboarding, controls, readability, balance, performance, or a bug produce the same symptom?
- **Change risk:** Would the proposed fix damage players or situations not represented by the session?

## Finding Categories

- **Implementation defect:** expected rule did not occur or diagnostics show an error.
- **Comprehension problem:** the player could act, but could not understand goal, state, cause, or control.
- **Balance or pacing problem:** rules work, but pressure, reward, timing, or progression misses the intended range.
- **Experience problem:** the feature functions but does not produce the intended emotion or clarity.
- **Evidence problem:** the session cannot support a reliable conclusion.

## Common Failure Patterns

- Treating one player's proposed solution as the root cause.
- Aggregating several symptoms into one broad “game feel” issue.
- Prioritizing by how easy a fix sounds rather than player impact and confidence.
- Using screenshots without matching input, state, revision, and diagnostics.
- Reusing evidence after the code or design decision changed.
- Changing several variables at once, making the next result uninterpretable.

## Advisory Output

For each important finding, provide:

1. the observation and context;
2. the most plausible cause plus at least one credible alternative when uncertainty is material;
3. severity and confidence in plain language;
4. the smallest next experiment or change that distinguishes the hypotheses;
5. the evidence required to accept or reject the result.

Prioritize at most three findings. If evidence is stale, incomplete, or contradictory, recommend a targeted replay rather than a design change.
