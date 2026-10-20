---
name: l
description: "World L Skill"
source_url: https://github.com/plurigrid/asi/blob/293ce9f76e3abcd5ba18db284688bc0d9ac6691d/skills/l/SKILL.md
source_repo: plurigrid/asi
category: coding
body_hash: 4eaaa4fba4afef791e44bab1f066846a2a45d54274a6571b5a80ce466d49a83b
---

# World L Skill

**Trit**: +1 (PLUS (generator/executor))
**Color Range**: Warm hues (0-60°, 300-360°)
**Index**: 11
**Wallet**: world_l_aptos
**MCP Server**: `mcp__world_l_aptos__*`

## GF(3) Role

This world operates as **PLUS (generator/executor)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__world_l_aptos__aptos_balance      # Check APT balance
mcp__world_l_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__world_l_aptos__aptos_swap         # Swap tokens on DEX
mcp__world_l_aptos__aptos_stake        # Stake with validator
mcp__world_l_aptos__aptos_view         # Call view function (read-only)
mcp__world_l_aptos__aptos_intent       # Natural language intent
mcp__world_l_aptos__aptos_pending      # List pending decisions
mcp__world_l_aptos__aptos_approve      # Approve/reject decision
```

## World Description

Pretty bugs and debugging

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

<!-- World L custom content -->
