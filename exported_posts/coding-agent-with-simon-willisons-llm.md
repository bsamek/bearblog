---
title: "Coding agent with Simon Willison's llm"
date: 2025-05-28
slug: coding-agent-with-simon-willisons-llm
published: true
discoverable: true
type: post
---
Simon Willison [released](https://simonwillison.net/2025/May/27/llm-tools/) tool calling in his [llm](https://llm.datasette.io/) CLI. A tool is just a python function. Inspired by [Coding agent in 94 lines of Ruby](https://radanskoric.com/articles/coding-agent-in-ruby), I wrote a coding agent in Python. Here's the [code](https://github.com/bsamek/llm-tools-editor/blob/c26911127fe16a7d475fcccc6d9c43ecc47ae7d4/llm_tools_editor.py).

aider helpfully [explains](https://aider.chat/docs/more/edit-formats.html) the various editing formats people use for LLMs:

1. **whole** returns an entirely new document.
2. **diff** is a series of search and replace blocks.
3. **diff-fenced** is like diffs but puts the filename inside the fence. gemini models prefer this.
4. **udiff** is a more familiar diff format, but only used for GPT-4 Turbo.

So I picked diff.

I implemented `read_file`, `list_files`, and `apply_diff`. Or rather, o4-mini did. Cloning other tools examples and passing them as fragments worked well.

Here's what it looks like. Adding `--td` shows the tool calls that the tools is making. My default model is gpt-4.1.

```
$ llm -t editor "Add me as an author to the pyproject.toml" -T read_file -T list_files -T apply_diff --td

Tool call: read_file({'path': 'pyproject.toml'})
  [project]
  name = "llm-tools-editor"
  version = "0.1"
  description = "Edit code with the llm CLI"
  requires-python = ">=3.9"
  dependencies = [
      "llm>=0.26"
  ]

  [project.entry-points.llm]
  llm_tools_editor = "llm_tools_editor"


You are not currently listed as an author in the pyproject.toml file. Could you please provide the name and optionally an email you would like to use for the author entry? This way, I can add you correctly.
```

It's nice that `llm -c` (continue conversation) preserves the tool calls originally passed to the conversation.

```
$ llm -c "Brian Samek, no email please" --td

Tool call: read_file({'path': 'pyproject.toml'})
  [project]
  name = "llm-tools-editor"
  version = "0.1"
  description = "Edit code with the llm CLI"
  requires-python = ">=3.9"
  dependencies = [
      "llm>=0.26"
  ]

  [project.entry-points.llm]
  llm_tools_editor = "llm_tools_editor"



Tool call: apply_diff({'diff': 'pyproject.toml\n<<<<<<< SEARCH\n[project]\nname = "llm-tools-editor"\nversion = "0.1"\ndescription = "Edit code with the llm CLI"\nrequires-python = ">=3.9"\ndependencies = [\n    "llm>=0.26"\n]\n=======\n[project]\nname = "llm-tools-editor"\nversion = "0.1"\ndescription = "Edit code with the llm CLI"\nrequires-python = ">=3.9"\ndependencies = [\n    "llm>=0.26"\n]\nauthors = ["Brian Samek"]\n>>>>>>> REPLACE\n'})
  Applied diff to: pyproject.toml

You have been added as an author to the pyproject.toml file as "Brian Samek" without an email. If you need any further updates or want your email added later, just let me know!
```

And there's the line.

```
$ git diff
diff --git a/pyproject.toml b/pyproject.toml
index 7b9676f..0737215 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -6,6 +6,7 @@ requires-python = ">=3.9"
 dependencies = [
     "llm>=0.26"
 ]
+authors = ["Brian Samek"]

 [project.entry-points.llm]
 llm_tools_editor = "llm_tools_editor"
```