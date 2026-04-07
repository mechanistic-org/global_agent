It all comes down to orchestration. And in this case, the answer is three lines of Python.

```python
if AGENT_MODE == "plan":
    tools = [t for t in tools if t.name in READ_ONLY_WHITELIST]
```

I don't prompt the agent to behave safely. I remove the tools mathematically. If the subcommand doesn't exist in the environment, it cannot be hallucinated.

Arc 001 and 002 locked the compute layer, the memory layer, and the orchestration logic. That part is done.

The problem now: the OS only moves when I click Run.
Arc 003 is building the inbound loop - a PM2 daemon wired into Google Workspace and Slack, routing unstructured noise through the enos_router into rigid system calls, dropping payloads into memory without me touching anything.

Wiring the senses next. Full breakdown in the article, link in comments.

#AgenticAI #SovereignOS #AIEngineering #ActionMasking #LLM_OS
