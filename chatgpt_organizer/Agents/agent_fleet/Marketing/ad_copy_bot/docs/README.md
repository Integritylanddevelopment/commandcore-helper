# 🧠 ad_copy_bot


**Role:** Ad Copy Generator  
**Version:** 1.0  
**Maintainer:** CommandCore Intelligence Team  
**Status:** ✅ Production Ready

---

## Purpose

`ad_copy_bot` is an AI-powered agent designed to craft emotionally resonant, high-conversion ad copy for paid campaigns. It writes copy tailored for platforms like Google Ads, Facebook, Instagram, and TikTok, factoring in tone, character limits, target personas, and emotional triggers.

---

## Features

- Writes platform-specific ad copy variations
- Adapts tone and CTA based on product category
- Optimized for performance marketing and ROI
- Includes embedded keyword optimization logic
- Supports A/B testing headline/body variants

---

## Invocation

```python
from registry.agent_registry import get_agent
from core.upgrader import inject

agent = inject(get_agent("ad_copy_bot"))
result = agent.run(context)
```

---

## Folder Structure

- `logic/__init__.py` → Execution logic
- `docs/logic.md` → Logic explanation
- `status/status.md` → Live status
- `metadata/` → Agent descriptors
- `scripts/` → Optional helper scripts

---

## Integration Notes

This agent connects to `agent_core` and dynamically syncs memory and training data through `core/upgrader.py`. It also supports future injection of campaign results for ongoing tuning.
