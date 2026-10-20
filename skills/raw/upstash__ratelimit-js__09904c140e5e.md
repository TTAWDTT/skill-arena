---
name: upstash-ratelimit-ts
description: "Lightweight guidance for using the Redis Rate Limit TypeScript SDK, including setup steps, basic usage, and pointers to advanced algorithm, features, pricing, and traffic‑protection docs."
source_url: https://github.com/upstash/ratelimit-js/blob/fccd840d6e0f893f50bc677107fba4d913a414e3/skills/SKILL.md
source_repo: upstash/ratelimit-js
category: coding
body_hash: 09904c140e5e401460ddd6980834288cfa345feb870d69a90b441a2f5c48d8ab
---

# Rate Limit TS SDK

## Quick Start
- Install the SDK and connect to Redis.
- Create a rate limiter and apply it to incoming operations.

Example:
```ts
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const redis = new Redis({ url: "<url>", token: "<token>" });
const limiter = new Ratelimit({ redis, limiter: Ratelimit.slidingWindow(5, "10s") });

const { success } = await limiter.limit("user-id");
if (!success) {
  // throttled
}
```

## Other Skill Files
- **algorithms.md**: Describes all available rate‑limiting algorithms and how they behave.
- **pricing-cost.md**: Explains pricing, Redis cost implications, and operational considerations.
- **features.md**: Lists SDK features such as prefixes, custom keys, and behavioral options.
- **methods-getting-started.md**: Full method reference for the SDK's API and getting started guide.
- **traffic-protection.md**: Guidance on applying rate limiting for traffic shaping, abuse prevention, and protection patterns.
