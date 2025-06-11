# 🧠 agent_core

**Role:** Central execution and memory engine for all CommandCoreOS agents  
**Version:** 2.0  
**Maintainer:** CommandCore Intelligence Team  
**Status:** ✅ Fully Operational

---

## Purpose

The `agent_core` is responsible for coordinating all registered agents in the CommandCore suite. It performs context routing, shared memory syncing, and agent injection to ensure seamless modular intelligence across the fleet.

---

## Features

- Memory injection from active tasks
- Routing to target agent via `context['target_agent']`
- Live call to `core.upgrader.py` for logic expansion
- Integration with `agent_registry.py` for central dispatch

---

## Usage

```python
from logic.agent_core import AgentCore

core = AgentCore("commandcore")
response = core.run({
    "target_agent": "value_prop_bot",
    "product_name": "TogetherWe",
    "target_audience": "couples in therapy"
})
```

