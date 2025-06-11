# 🧠 ad_copy_bot — Logic Overview

This agent generates compelling ad copy structured for digital marketing platforms using a context-aware algorithm. It balances emotional triggers, keyword embedding, and character constraints to optimize performance.

---

## Core Method: `run(context)`

### Input JSON Schema

```json
{
  "product_name": "str",
  "description": "str",
  "target_audience": "str",
  "platform": "str"
}
```

### Output JSON Schema

```json
{
  "headline": "str",
  "body": "str",
  "cta": "str"
}
```

---

## Execution Flow

1. Extracts product and audience details from context.
2. Builds a dynamic `headline` using a persuasive structure.
3. Formats the `body` to be emotional yet informative.
4. Selects a `CTA` based on the platform type.
5. Returns a dictionary payload ready for UI display or campaign insertion.

---

## Auto-Scheduling

While currently a manual-invoke agent, future upgrades will allow it to:
- Auto-generate weekly campaign variants
- Tune messages based on click-through and conversion data
