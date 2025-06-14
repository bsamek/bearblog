---
title: "Perplexity is still better at quick searches"
date: 2025-04-25
slug: perplexity-better-at-quick-searches
published: true
discoverable: true
type: post
---
Simon Willison [writes](https://simonwillison.net/2025/Apr/21/ai-assisted-search/) that "AI assisted search-based research actually works now." o3 and o4-mini agentic research is truly impressive, as are ChatGPT's and Gemini's Deep Research. 

But I consistently find queries where Perplexity gets it right, and ChatGPT and Gemini get it wrong.

An example: "how is chatgpt-4o-latest different from gpt-4o." Only Perplexity correctly identifies that the model is priced differently than gpt-4o. Gemini 2.5 Pro focuses entirely on gpt-4o being stable, while chatgpt-4o-latest changes. ChatGPT does the same. Only Perplexity figured out that its pricing is different from gpt-4o. I tried asking the question a few different ways, and Perplexity found *different* sources to explain that the March release improved in instruction following, coding, and creativity. I think this demonstrates that Perplexity didn't just get lucky with a source.

To its credit, o3 figured this all out too, but for a quick, correct answer, I keep being impressed by Perplexity over ChatGPT search and Gemini search.

This is also what the new [LMArena Search leaderboard](https://beta.lmarena.ai/leaderboard/search) finds. Perplexity is the best fast (non-reasoning) model. The leaderboard also finds that all reasoning models, including Gemini 2.5 Pro, are better than non-reasoning models, but Perplexity is the clear winner for my query over Gemini 2.5 Pro. (Poking at the first page of Google results also didn't answer my question.)