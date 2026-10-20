---
name: wemp-operator
description: "微信公众号自动化运营。触发词：采集热点、公众号日报、周报、检查评论、回复评论、生成文章。依赖 wemp skill。"
source_url: https://github.com/IanShaw027/wemp-operator/blob/7574534715edf5423b258beb12a2dc63372f8c2a/SKILL.md
source_repo: IanShaw027/wemp-operator
category: data
body_hash: 8bb05919946251aa9664a8a4a2fb4975d65e8c756f90de3cede09c028fea6527
---

# wemp-operator

公众号自动化运营：内容采集、数据分析、互动管理。

## 环境检查

```bash
node scripts/setup.mjs        # 检查依赖
node scripts/setup.mjs --help # 配置指南
```

## 内容采集

```bash
node scripts/content/smart-collect.mjs \
  --query "需求" --keywords "关键词" --sources "数据源" [--deep]
```

数据源：hackernews, github, v2ex, 36kr, weibo, zhihu, producthunt, wallstreetcn 等

## 数据分析

```bash
node scripts/analytics/daily-report.mjs [--date YYYY-MM-DD]
node scripts/analytics/weekly-report.mjs
```

## 互动管理

```bash
node scripts/interact/check-comments.mjs [--list]
node scripts/interact/reply.mjs --comment-id <id> [--content "回复"]
```
