---
name: ping-beads
description: "Verify the bead daemon is alive and responsive"
source_url: https://github.com/kbarbel640-del/skills/blob/e7e336ac628c3e3bd771aff1aaa469c93778f94a/skills/xejrax/ping-beads/SKILL.md
source_repo: kbarbel640-del/skills
category: other
body_hash: 68e595e378762da4b6d62df4e5f41915542aac76d1a193b71c2bfc1fc22ef382
---

# Ping Beads

Verify the bead daemon is alive and responsive. Checks the `bd.sock` socket to confirm the bead daemon (`bd`) is running and accepting connections.

## Commands

```bash
# Check if the bead daemon is alive (checks bd.sock)
ping-beads

# Show detailed bead daemon status
ping-beads status
```

## Install

No installation needed. `bd` is expected to be in PATH as part of the beads system.
