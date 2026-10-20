---
name: product-launch
description: "Product launch page with countdown, feature reveals, teaser video placeholder,\nand early-access signup. Use for \"launch\", \"product launch\", \"coming soon\"."
source_url: https://github.com/pujan-modha/clover-design/blob/bcd24e99b5c3e703c7fd08c6bdf08df5ceb39ab2/skills/product-launch/SKILL.md
source_repo: pujan-modha/clover-design
category: review
body_hash: b6c2d8773734badab6dfbd51b7aa960c0f82fc9b9b1bd4f0a5f55e2ff605c883
---

# Product Launch Skill

Produce a product launch / coming-soon page.

## Sections
1. **Hero**: massive product name, tagline, countdown timer (CSS animation).
2. **Teaser**: gradient placeholder for video/screenshot with play button overlay.
3. **Feature reveals**: 3 cards that fade in on scroll (CSS `animation-timeline`).
4. **Early access**: email signup form (styled input + button).
5. **Social proof**: "Join X others" with avatar stack.
6. **Footer**: minimal links, copyright.

## Rules
- Countdown: CSS-only, updates via JS interval.
- Avatar stack: overlapping circles with colored initials.
- Accent used for CTA and countdown numbers only.
- `data-df-id` on each section.

## Output
Single `index.html`, inline CSS/JS.
