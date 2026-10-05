---
name: dometrain-notes
description: Turn Dometrain lesson pages (dometrain.com/take/course/...) into faithful Simplified Chinese Markdown notes written to a file the user names. Use whenever the user gives one or more Dometrain lesson URLs and asks for notes, a translation, or a Markdown version of the lesson content.
argument-hint: <lesson-url> [<lesson-url> ...] <output-path-or-dir>
---

# Dometrain lesson to Chinese Markdown

Scripts live in `.claude/skills/dometrain-notes/scripts/` and run with the skill's own venv:
`.claude/skills/dometrain-notes/.venv/bin/python` (paths are relative to the repo root).
If the venv is missing (fresh clone), create it: `python3 -m venv .claude/skills/dometrain-notes/.venv && .claude/skills/dometrain-notes/.venv/bin/pip install -r .claude/skills/dometrain-notes/requirements.txt`.
The login session lives in the gitignored `.profile/` next to this file; on a fresh clone it must be created with `import_cookies.py` (see below).

## 1. Fetch the English Markdown

```bash
.claude/skills/dometrain-notes/.venv/bin/python .claude/skills/dometrain-notes/scripts/fetch.py <url> [<url> ...] > <scratchpad>/lesson.en.md
```

- It extracts only the lesson's Instructions panel (`#quiz-instructions-content`) and converts it to Markdown, one document per URL after a `<!-- lesson: URL -->` marker.
- Exit code 2 means the saved session expired.
  Ask the user to re-export `dometrain.com` cookies from their Windows Chrome with the "Get cookies.txt LOCALLY" extension, copy the file into the VM, then run `scripts/import_cookies.py <cookies.txt>` and retry.
  Never print or echo cookie values.
- Any other failure (selector not found) means the page layout differs, for example a video-only lesson.
  Dump the page HTML to the scratchpad, find the new content container, and update `fetch.py` rather than working around it.

## 2. Translate

Apply this instruction to the fetched content exactly, which is the user's original prompt:

> 把提供的内容整理成Markdown 版本，这样我可以直接复制到 Notion、GitHub、Obsidian 等地方。不要擅自更改内容，就是变成markdown格式!!!

The output is Simplified Chinese.
Rules, matching the user's existing notes in `python/00-interview-questions/`:

- Translate faithfully: no added explanations, summaries, examples, or omitted sentences.
- Keep the source's Markdown structure: same headings (levels as fetched), lists, code blocks, and their order.
- Translate prose and code comments; keep code, identifiers, output values, and inline code unchanged.
- For a key technical term, give the English in parentheses on first use when it helps, e.g. `不可变（immutable）`.
- Do not add a title heading the source does not have.
- Put each full sentence on its own line, without inserting blank lines inside a paragraph.
- Never use em dashes.

## 3. Write

- One URL and a file path: write the translation to that file (overwrite only if it is empty or the user asked).
- Several URLs and a directory: write one file per lesson, continuing the directory's `NN-kebab-name.md` numbering, named after the lesson.
- Report the written path(s) and a one-line summary per lesson.
