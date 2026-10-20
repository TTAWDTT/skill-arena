---
name: h
description: "World H Skill"
source_url: https://github.com/plurigrid/asi/blob/293ce9f76e3abcd5ba18db284688bc0d9ac6691d/skills/h/SKILL.md
source_repo: plurigrid/asi
category: review
body_hash: df62a787e919cb73e510fb1820c2ea9560f14a56ba1382c820f2a15ca609723d
---

# World H Skill

**Trit**: +0 (ERGODIC (coordinator/synthesizer))
**Color Range**: Neutral hues (60-180°)
**Index**: 7
**Wallet**: world_h_aptos
**MCP Server**: `mcp__world_h_aptos__*`

## GF(3) Role

This world operates as **ERGODIC (coordinator/synthesizer)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__world_h_aptos__aptos_balance      # Check APT balance
mcp__world_h_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__world_h_aptos__aptos_swap         # Swap tokens on DEX
mcp__world_h_aptos__aptos_stake        # Stake with validator
mcp__world_h_aptos__aptos_view         # Call view function (read-only)
mcp__world_h_aptos__aptos_intent       # Natural language intent
mcp__world_h_aptos__aptos_pending      # List pending decisions
mcp__world_h_aptos__aptos_approve      # Approve/reject decision
```

## World Description

gdlog/datalog systems

## Triadic Coordination

When operating in parallel with other worlds:

| Your Role | Partner Roles | Combined |
|-----------|--------------|----------|
| +0 | Need -1, +1 | Σ = 0 ✓ |

## Related Skills

- `aptos-agent` - Core Aptos interaction patterns
- `aptos-society` - World Extractable Value (WEV) contracts
- `gay-mcp` - Deterministic color generation from seed
- `plurigrid-asi-integrated` - Unified skill orchestration

## Customization

Add world-specific configurations below this line:

---

<!-- World H custom content -->
