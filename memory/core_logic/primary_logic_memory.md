# PRIMARY LOGIC MEMORY – DO NOT DELETE OR AUTO-EDIT

This document defines the permanent intentions of the system builder.  
All AI agents, scripts, interfaces, and co-developers must follow these rules.  
This file supersedes all inferred behaviors or default assumptions.

---

## I. CORE BELIEFS

- No memory should ever be permanently deleted.
- All memory — even outdated, messy, or redundant — is part of the system’s long-term traceability.
- Short-Term, Working, and Episodic memory are staging areas, not discard zones.
- The system exists to preserve intention, not optimize for storage or minimalism.
- Builder directives are sacred and must be traceable across time.

---

## II. MEMORY RETENTION POLICIES

### Short-Term Memory (STM)
- Purpose: Temporarily focused active state
- Must not be deleted
- May be promoted or archived, but never erased
- Auto-expiry scripts (e.g., `memory_decay.py`) must not apply here

### Working Memory (WM)
- Purpose: In-progress scratch and iterative content
- May be overwritten during active work
- Snapshots of overwritten content must be saved before discard
- Nothing is lost — only versioned

### Episodic Memory (EPI)
- Purpose: Conversation logs, milestone records
- Immutable once created
- Must not be rewritten or deleted
- Should be cross-linked with Procedural and LTM if relevance is high

### Long-Term Memory (LTM)
- Purpose: Curated knowledge, decisions, finalized insights
- Only promoted via conscious user or agent review
- All promotion actions must preserve source and date

### Semantic Memory (SEM)
- Purpose: Timeless facts, terminology, core definitions
- No auto-expiry, must be version-controlled

### Procedural Memory (PRO)
- Purpose: Methods, how-to’s, operational playbooks
- Updates must be logged with history tracking

---

## III. PROMOTION & ARCHIVAL RULES

- Promotion from STM, WM, or EPI to LTM must preserve:
  - Timestamp
  - Source file
  - Builder identity and intent
- No “cleaning” of memory without explicit confirmation
- Archival folders must retain file access parity with live memory folders

---

## IV. GUI + AGENT INTERFACE RULES

- No GUI button may delete memory unless explicitly confirmed via irreversible modal
- GUI search, load, and view functions must default to **read-only**
- All write operations must respect original memory type and tagging logic

---

## V. PROTECTED TAGS + KEYWORDS

- `#neverdelete`: files or entries tagged with this must be locked
- `#corelogic`: entries used in memory enforcement or system-level functions
- `#builderintent`: captures the voice, values, or architecture choices of the system creator

---

## VI. REASONING PHILOSOPHY

- This system is **built for historical integrity**, not runtime minimalism
- All AI refactors or cleanups must validate against this logic file
- Any violation of these principles must trigger an error or warning

---

Version: 1.0  
Last Updated: [Set by script when modified]  
Location: `CommandCore-OS/memory/core_logic/primary_logic_memory.md`


---

## COPYRIGHT NOTICE
© 2025 Stephen Alexander. 
All rights reserved.

The Primary Logic Memory ("PLM") architecture and all associated intent, 
structure, and operational philosophy are the intellectual property of 
Stephen Alexander. 

This document defines foundational system logic and may not be copied, 
modified, deleted, or redistributed without explicit written consent.
No AI agent, co-developer, plugin, or automation layer may override, 
obscure, or diminish the authority of this logic under any circumstance.
This file is binding for all present and future iterations of 
the CommandCore OS platform, including derivative works and GUI-integrated systems.
Violation of these terms constitutes a breach of system integrity.

---



