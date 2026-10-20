---
name: i
description: "World I Skill"
source_url: https://github.com/plurigrid/asi/blob/293ce9f76e3abcd5ba18db284688bc0d9ac6691d/skills/i/SKILL.md
source_repo: plurigrid/asi
category: review
body_hash: 780da3294badfb803ae5066825ba24a3aa144c237a58bd33756a4e292c89cdc9
---

# World I Skill

**Trit**: +1 (PLUS (generator/executor))
**Color Range**: Warm hues (0-60°, 300-360°)
**Index**: 8
**Wallet**: world_i_aptos
**MCP Server**: `mcp__world_i_aptos__*`

## GF(3) Role

This world operates as **PLUS (generator/executor)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__world_i_aptos__aptos_balance      # Check APT balance
mcp__world_i_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__world_i_aptos__aptos_swap         # Swap tokens on DEX
mcp__world_i_aptos__aptos_stake        # Stake with validator
mcp__world_i_aptos__aptos_view         # Call view function (read-only)
mcp__world_i_aptos__aptos_intent       # Natural language intent
mcp__world_i_aptos__aptos_pending      # List pending decisions
mcp__world_i_aptos__aptos_approve      # Approve/reject decision
```

## World Description

InverterNetwork DeFi

## Triadic Coordination

When operating in parallel with other worlds:

| Your Role | Partner Roles | Combined |
|-----------|--------------|----------|
| +1 | Need -1, 0 | Σ = 0 ✓ |

## Related Skills

- `aptos-agent` - Core Aptos interaction patterns
- `aptos-society` - World Extractable Value (WEV) contracts
- `gay-mcp` - Deterministic color generation from seed
- `plurigrid-asi-integrated` - Unified skill orchestration

## Customization

Add world-specific configurations below this line:

---

<!-- World I custom content -->
