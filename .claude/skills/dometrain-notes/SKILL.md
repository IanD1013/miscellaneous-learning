---
name: dometrain-notes
description: Turn Dometrain lesson pages (dometrain.com/take/course/...) into faithful Simplified Chinese Markdown notes written to a file or folder the user names. Use whenever the user gives one or more Dometrain lesson URLs, or a Dometrain course plus a module name such as "Hello World", and asks for notes, a translation, or a Markdown version of the lesson content.
argument-hint: <lesson-url> [<lesson-url> ...] <output-path-or-dir> | <course-or-lesson-url> "<module name>" <output-dir>
---

# Dometrain lesson to Chinese Markdown

Scripts live in `.claude/skills/dometrain-notes/scripts/` and run with the skill's own venv:
`.claude/skills/dometrain-notes/.venv/bin/python` (paths are relative to the repo root).
If the venv is missing (fresh clone), create it: `python3 -m venv .claude/skills/dometrain-notes/.venv && .claude/skills/dometrain-notes/.venv/bin/pip install -r .claude/skills/dometrain-notes/requirements.txt`.
The login session lives in the gitignored `.profile/` next to this file; on a fresh clone it must be created with `import_cookies.py` (see below).

## 0. Resolve a module to lesson URLs

Skip this when the user gave lesson URLs.
When they name a module instead, list its lessons in course order:

```bash
.claude/skills/dometrain-notes/.venv/bin/python .claude/skills/dometrain-notes/scripts/list_lessons.py <course-or-lesson-url> "<module name>"
```

- The first argument is the course URL (`dometrain.com/take/course/<course>/`) or any lesson URL in that course.
  If the user did not give one, ask which course rather than guessing.
- The module name matches the sidebar's chapter title, ignoring case; on no match the script prints every module title, so pick the intended one or ask.
- It prints one `URL<TAB>lesson title` line per lesson; pass all the URLs to step 1 in that order.

## 1. Fetch the lesson Markdown

```bash
.claude/skills/dometrain-notes/.venv/bin/python .claude/skills/dometrain-notes/scripts/fetch.py <url> [<url> ...] > <scratchpad>/lesson.md
```

- It extracts only the lesson's Instructions panel and converts it to Markdown, one document per URL after a `<!-- lesson: URL lang: en|zh -->` marker.
- Hands-on exercise lessons (`#exercise-instructions`) have a language dropdown; the script selects ZH, so they come back already in Simplified Chinese (`lang: zh`) without their Hints section.
- Exercise lessons are followed by a `<!-- task -->` ... `<!-- /task -->` block with the editor's code and the test cases. It is input for step 3, not lesson content: never translate it or copy it into the notes.
- Quiz lessons (`#quiz-instructions-content`) have no translation and come back in English (`lang: en`).
- Exit code 2 means the saved session expired.
  Ask the user to re-export `dometrain.com` cookies from their Windows Chrome with the "Get cookies.txt LOCALLY" extension, copy the file into the VM, then run `scripts/import_cookies.py <cookies.txt>` and retry.
  Never print or echo cookie values.
- Any other failure (selector not found) means the page layout differs, for example a video-only lesson.
  Dump the page HTML to the scratchpad, find the new content container, and update `fetch.py` rather than working around it.

## 2. Translate

Apply this instruction to the fetched content exactly, which is the user's original prompt:

> 把提供的内容整理成Markdown 版本，这样我可以直接复制到 Notion、GitHub、Obsidian 等地方。不要擅自更改内容，就是变成markdown格式!!!

The output is Simplified Chinese.

For a `lang: zh` lesson the site has already translated the prose: keep its wording verbatim and do not retranslate it.
Only translate what it left in English (typically headings, table cells, and code comments), then apply the formatting rules below (sentence per line, no em dashes, so `——` becomes a plain hyphen or a Chinese comma as the sentence needs).

Rules, matching the user's existing notes in `python/00-interview-questions/`:

- Translate faithfully: no added explanations, summaries, examples, or omitted sentences.
- Keep the source's Markdown structure: same headings (levels as fetched), lists, code blocks, and their order.
- Translate prose and code comments; keep code, identifiers, output values, and inline code unchanged.
- For a key technical term, give the English in parentheses on first use when it helps, e.g. `不可变（immutable）`.
- Do not add a title heading the source does not have.
- Put each full sentence on its own line, without inserting blank lines inside a paragraph.
- Never use em dashes.

## 3. Solve "Your Task"

Do this only when the lesson has a "Your Task" section (any heading level, English or translated).

- Start from the task block's editor code: keep its class, method signature, and provided variables, and replace only the "Your code here" part.
  The block lists every editor file; use `(read-only)` files as given and edit only the others.
- Make every test case pass exactly (output text, line breaks, return values).
- Use the simplest solution built from what this lesson teaches; avoid features the course has not reached.
- Verify it by running it locally against each test case when a toolchain exists (`python3` for Python, `g++` for C++, `dotnet` for C#).
  If none is installed (for example no `dotnet`), trace each test case by hand and tell the user it was not run.
- Never click Run or Submit on the site.
- Append it after the lesson's last section as a `解答` heading at the same level as the lesson's other headings, followed by the complete code of each edited file in its own fenced block (preceded by the file name when there is more than one file).
  Code comments in the solution are Chinese; add no prose beyond the heading.

## 4. Write

- One URL and a file path: write the translation to that file (overwrite only if it is empty or the user asked).
- Several URLs and a directory: write one file per lesson, continuing the directory's `NN-kebab-name.md` numbering, named after the lesson.
- A module and a directory: same, in the module's lesson order, with the kebab name taken from the lesson URL's slug without its trailing number (`console-printing-69955572` becomes `01-console-printing.md`).
  If the directory already has notes, report the conflict and ask before overwriting or renumbering.
- Report the written path(s) and a one-line summary per lesson.
