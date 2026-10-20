---
name: upstash-vector-js
description: "Provides quick-start guidance and a unified entry point for Vector features, SDK usage, and integrations. Use when users ask how to work with Vector, its TS SDK, features, or supported frameworks."
source_url: https://github.com/upstash/vector-js/blob/ad3ad721a1d5035c5a891830174cbba8bcd9d10d/skills/SKILL.md
source_repo: upstash/vector-js
category: coding
body_hash: 46a046514fdd2dfd2681096cd9c7278d7b40c247272d3b5847c88d8612da9508
---

# Vector Documentation Skill

## Quick Start

Vector is a high‑performance vector database for storing, querying, and managing vector embeddings.

Basic workflow:

- Install the Vector TS SDK.
- Connect to a Vector instance.
- Upsert vectors, query them, and manage namespaces.

Example (TypeScript):

```ts
import { Index } from "@upstash/vector";
const index = new Index({
  url: process.env.UPSTASH_VECTOR_REST_URL!,
  token: process.env.UPSTASH_VECTOR_REST_TOKEN!,
});

await index.upsert([{ id: "1", vector: [0.1, 0.2], metadata: { tag: "example" } }]);

const results = await index.query({
  vector: [0.1, 0.2],
  topK: 5,
});
```

For full usage, refer to the linked skill files below.

## Other Skill Files

### TS SDK Reference

- `sdk-methods`: Explains SDK commands: delete, fetch, info, query, range, reset, resumable-query, upsert

### Features

- `features/namespaces`: Explains namespaces and dataset organization.
- `features/index-structure`: Covers hybrid and sparse index structures.
- `features/filtering-and-metadata`: Details metadata storage and server-side filtering.

Use these files for deeper guidance on SDK usage, advanced configurations, algorithms, and integrations.
