---
name: t
description: "World T Skill"
source_url: https://github.com/plurigrid/asi/blob/293ce9f76e3abcd5ba18db284688bc0d9ac6691d/skills/t/SKILL.md
source_repo: plurigrid/asi
category: review
body_hash: 7889cc0a11f94800fe7f81c22603d7ab0faf76728cea5b8a228b9ab4fd90585d
---

# World T Skill

**Trit**: +0 (ERGODIC (coordinator/synthesizer))
**Color Range**: Neutral hues (60-180°)
**Index**: 19
**Wallet**: world_t_aptos
**MCP Server**: `mcp__world_t_aptos__*`

## GF(3) Role

This world operates as **ERGODIC (coordinator/synthesizer)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__world_t_aptos__aptos_balance      # Check APT balance
mcp__world_t_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__world_t_aptos__aptos_swap         # Swap tokens on DEX
mcp__world_t_aptos__aptos_stake        # Stake with validator
mcp__world_t_aptos__aptos_view         # Call view function (read-only)
mcp__world_t_aptos__aptos_intent       # Natural language intent
mcp__world_t_aptos__aptos_pending      # List pending decisions
mcp__world_t_aptos__aptos_approve      # Approve/reject decision
```

## World Description

CatColab collaborative CT

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

<!-- World T custom content -->
