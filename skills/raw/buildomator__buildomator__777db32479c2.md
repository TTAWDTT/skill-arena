---
name: do
description: "Route freeform text to the right GSD command automatically"
source_url: https://github.com/buildomator/buildomator/blob/4f9c3850e884e924aa34d5d0a5675106815533ee/skills/do/SKILL.md
source_repo: buildomator/buildomator
category: review
body_hash: 777db32479c2b295fafa7236878a7e3fd79b83b76b3a20a00ed67f2bb671c676
---

<objective>
Analyze freeform natural language input and dispatch to the most appropriate GSD command.

Acts as a smart dispatcher — never does the work itself. Matches intent to the best GSD command using routing rules, confirms the match, then hands off.

Use when you know what you want but don't know which `/gsd-*` command to run.
</objective>

<execution_context>
@${CLAUDE_PLUGIN_ROOT}/workflows/do.md
@${CLAUDE_PLUGIN_ROOT}/references/ui-brand.md
</execution_context>

<context>
$ARGUMENTS
</context>

<process>
Execute the do workflow from @${CLAUDE_PLUGIN_ROOT}/workflows/do.md end-to-end.
Route user intent to the best GSD command and invoke it.
</process>
