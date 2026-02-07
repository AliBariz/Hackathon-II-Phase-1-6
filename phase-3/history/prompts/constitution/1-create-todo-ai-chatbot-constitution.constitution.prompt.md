---
id: 1
title: Create Todo AI Chatbot Constitution
stage: constitution
date: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-chatbot
branch: master
user: AGICO
command: /sp.constitution
labels: [constitution, spec-driven-development, mcp, ai-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Create a constitution file for the Todo AI Chatbot project based on the provided requirements. The constitution should govern Phase III of the Todo project, which introduces an AI-powered chatbot interface that allows users to manage tasks using natural language. The implementation must use Model Context Protocol (MCP), OpenAI Agents SDK, Claude Code, and Spec-Kit Plus, following a strict agentic, spec-driven workflow.

## Response snapshot

Created a comprehensive constitution file for the Todo AI Chatbot project that includes core principles, system architecture, MCP tools specification, agent behavior rules, and governance guidelines. The constitution enforces the spec-driven workflow, locked technology stack, stateless architecture, and proper MCP tool usage as required by the project specifications.

## Outcome

- ✅ Impact: Created initial constitution file governing the Todo AI Chatbot project
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with complete constitution
- 🔁 Next prompts: Continue with spec generation for the chatbot features
- 🧠 Reflection: The constitution properly enforces the required agentic development workflow and technology constraints

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec generation for the chatbot features