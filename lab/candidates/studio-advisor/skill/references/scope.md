# Scope Lens

Use this lens to protect the smallest coherent player experience while exposing schedule, dependency, and production risk.

## Establish the Baseline

Clarify the outcome being protected:

- What must the player be able to do and feel?
- What assumption must the next build test?
- What deadline, team capacity, platform, and existing assets are real constraints?
- What is already committed or implemented?

If no baseline exists, do not pretend to calculate scope creep. Help define a testable baseline first.

## Evaluation Axes

- **Core versus support:** Does the item directly test or deliver the core experience, or only make it broader, prettier, or more complete?
- **Uncertainty reduction:** Does it answer an important unknown, or build around an unproven assumption?
- **Dependency fan-out:** How many systems, assets, interfaces, and verification paths must change with it?
- **Content multiplication:** Does one mechanic create reusable variety, or require handcrafted content every time?
- **Integration cost:** Is the item small in isolation but expensive when connected to controls, UI, saves, assets, AI, or balance?
- **Reversibility:** Can it be prototyped or removed cheaply if the idea fails?
- **Quality floor:** Which companion work is necessary for the slice to be understandable and testable rather than merely present?
- **Cut integrity:** Does the proposed cut preserve a coherent experience, or leave disconnected systems and unclear goals?

## Prioritization

Classify items by decision value, not by prestige:

- **Keep now:** required to test or deliver the core outcome.
- **Simplify:** retain the outcome with fewer states, assets, rules, or integrations.
- **Defer:** valuable after the core assumption passes.
- **Cut:** does not justify its dependency and verification cost.

Avoid numeric bloat scores when estimates are weak. A dependency explanation and a concrete cut are more useful than false precision.

## Common Failure Patterns

- Calling discovered requirements “scope creep” even though they are necessary for the feature to work.
- Protecting every feature while extending the schedule implicitly.
- Cutting feedback, onboarding, or verification and leaving an untestable prototype.
- Building progression, content, and polish before the core action is proven.
- Treating generated assets or AI implementation as zero-cost production.
- Splitting work into parallel tasks that share unstable interfaces or files.

## Advisory Output

Recommend a smallest coherent slice with explicit inclusions and exclusions. Name the largest risk, the cheapest way to test it, and the trigger for expanding scope. When cuts are needed, preserve the player promise before preserving system count.

Do not write sprint plans, estimates, or tasks unless the user later asks the development workflow to do so.
