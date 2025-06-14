---
title: "Model Context Protocol, simply"
date: 2025-05-01
slug: model-context-protocol-simply
published: true
discoverable: true
type: post
---
I keep seeing descriptions of Model Context Protocol (MCP) that are either vague metaphors or get too specific too quickly.

From the [official docs](https://modelcontextprotocol.io/introduction):

> MCP is an open protocol that standardizes how applications provide context to LLMs. Think of MCP like a USB-C port for AI applications. Just as USB-C provides a standardized way to connect your devices to various peripherals and accessories, MCP provides a standardized way to connect AI models to different data sources and tools.

So it's an adapter of some kind, but what does it actually **do**? The docs define terms and provide starter code, but I wanted a high-level overview. So here's mine.

The MCP client asks the MCP server what APIs are available (but it calls them *tools*). Then, instead of your LLM having to produce a payload that works with some arbitrary API, your LLM produces a payload in a standard format, which is just JSON. The MCP client adds some metadata and sends it to the MCP server, which replies back to the MCP client, which hands the data back to the LLM.

![mcp-client-server](https://bear-images.sfo2.cdn.digitaloceanspaces.com/samek/mcp-client-server.svg)

That's the core idea, except it's not just tools. There's three:

* **Tools**, which you request for side effects.
* **Resources**, which don't have side effects.
* **Prompts**, which are parameterized prompt templates.

