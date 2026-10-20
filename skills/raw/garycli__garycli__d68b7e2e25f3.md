---
name: skills
description: "This directory contains Skill source packages that can be installed from Gary's interactive mode."
source_url: https://github.com/garycli/garycli/blob/31e4e520222a14f6e55e0a2294b44c144b9b2238/skills/skill.md
source_repo: garycli/garycli
category: coding
body_hash: d68b7e2e25f3ed99bf136524a2d318415b79cd7a8932b3dfdf1c969551a3b45e
---

# Bundled Skills

This directory contains Skill source packages that can be installed from Gary's interactive mode.

| Skill | Target | Purpose |
| --- | --- | --- |
| `dht11_atomic` | STM32F1 / F4 正点原子精英板 | DHT11 driver and complete examples |
| `dht11_discovery` | STM32F407ZG 正点原子探索版 | DHT11 with OLED or UART output |
| `ds18b20_atomic` | STM32F1 / F4 正点原子精英板 | DS18B20 driver and complete examples |
| `oled_8080_discovery` | STM32F407ZG 正点原子探索版 | 8080 OLED and optional DS18B20 display |
| `oled_8080_elite` | STM32F103 正点原子精英板 | 8080 OLED text, geometry, and bitmap demos |

Install a bundled Skill from the repository root:

```text
/skill install ./skills/<skill-name>
```

Each package keeps its metadata in `skill.json`, schemas in `schemas.json`, implementation in `tools.py`, and runtime guidance in `prompt.md`.
