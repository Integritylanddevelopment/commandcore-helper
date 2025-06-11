# 🧠 upgrader

The `upgrader` injects behavior into agents dynamically before they are executed.  
It can be used to modify inputs, enhance memory, or track analytics.

---

## Features

- Wraps agent in a dynamic behavior layer
- Adds traceable context flags (`"upgraded": true`)
- Modular enhancement architecture

---

## Usage

```python
from logic.injector import inject

agent = get_agent("dummy_agent")
enhanced = inject(agent)
enhanced.run({"message": "test"})
```
