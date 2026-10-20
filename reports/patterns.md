# Skill Writing Patterns (draft)

This report is filled after pilot / full eval. Early hypotheses to test:

## Length
- Too short (<150 words): often no measurable lift.
- Very long (>2k words): may dilute trigger compliance / waste tokens.

## Structure
- Clear `When to use` / trigger description correlates with higher trigger success.
- Numbered steps beat prose blobs for coding / review skills.

## Examples
- At least one concrete input→output example helps writing and coding categories.

## Failure modes
- Ads / promo language → coarse-filtered out.
- Skills that require external accounts excluded from v1 arena.
- Category mismatch (skill vs task) depresses win rate — match before judging.

## Method notes
- Executor: `gpt-5.6-luna`
- Judge: `gpt-5.6-sol` (blind A/B, order swapped)
- Load mode: skill body prepended as `instructions` (offline approximation of real trigger)

Update this file after inspecting curated winners vs losers.
