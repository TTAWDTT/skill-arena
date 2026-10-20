---
name: blogwatcher
description: "Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI."
source_url: https://github.com/Hyaxia/blogwatcher/blob/58acfeb16258bd0e64d72f8f977ae8143cae5fa3/skills/SKILL.md
source_repo: Hyaxia/blogwatcher
category: coding
body_hash: cb2c76667893f7fe746abdcc7d4ca90c4cb8d554776f587c61e690833b6efd8d
---

# blogwatcher

Track blog and RSS/Atom feed updates with the `blogwatcher` CLI.

Install

- Go: `go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest`

Quick start

- `blogwatcher --help`

Common commands

- Add a blog: `blogwatcher add "My Blog" https://example.com`
- List blogs: `blogwatcher blogs`
- Scan for updates: `blogwatcher scan`
- List articles: `blogwatcher articles`
- Mark an article read: `blogwatcher read 1`
- Mark all articles read: `blogwatcher read-all`
- Remove a blog: `blogwatcher remove "My Blog"`

Example output

```
$ blogwatcher blogs
Tracked blogs (1):

  xkcd
    URL: https://xkcd.com
```

```
$ blogwatcher scan
Scanning 1 blog(s)...

  xkcd
    Source: RSS | Found: 4 | New: 4

Found 4 new article(s) total!
```

Notes

- Use `blogwatcher <command> --help` to discover flags and options.
