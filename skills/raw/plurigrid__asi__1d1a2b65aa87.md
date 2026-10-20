---
name: z
description: "World Z Skill"
source_url: https://github.com/plurigrid/asi/blob/293ce9f76e3abcd5ba18db284688bc0d9ac6691d/skills/z/SKILL.md
source_repo: plurigrid/asi
category: review
body_hash: 1d1a2b65aa87b972c6a8145b188a5693507a2723975b397f1491f10c3059b8a2
---

# World Z Skill

**Trit**: +0 (ERGODIC (coordinator/synthesizer))
**Color Range**: Neutral hues (60-180°)
**Index**: 25
**Wallet**: world_z_aptos
**MCP Server**: `mcp__world_z_aptos__*`

## GF(3) Role

This world operates as **ERGODIC (coordinator/synthesizer)** in the triadic system.

Conservation law: `Σ trits ≡ 0 (mod 3)` across all parallel operations.

## Usage

Access blockchain operations via MCP tools:

```
mcp__world_z_aptos__aptos_balance      # Check APT balance
mcp__world_z_aptos__aptos_transfer     # Transfer APT (requires approval)
mcp__world_z_aptos__aptos_swap         # Swap tokens on DEX
mcp__world_z_aptos__aptos_stake        # Stake with validator
mcp__world_z_aptos__aptos_view         # Call view function (read-only)
mcp__world_z_aptos__aptos_intent       # Natural language intent
mcp__world_z_aptos__aptos_pending      # List pending decisions
mcp__world_z_aptos__aptos_approve      # Approve/reject decision
```

## World Description

Zeta functions and spectral

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

<!-- World Z custom content -->
