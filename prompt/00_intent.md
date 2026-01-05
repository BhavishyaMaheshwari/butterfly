# 00_intent.md

## Butterfly — Product Intent

### What is Butterfly?

Butterfly is a **local-first machine learning application** that allows users to build, run, and understand ML pipelines through a clean visual interface, while retaining the ability to fully control and modify every part of the system using code.

Butterfly runs locally, launches as a local web application, and is designed to be packaged as a desktop app later.

It is not a CLI tool, not a notebook, and not a hosted AutoML platform.  
Butterfly is a **stateful ML execution environment**.

---

### Why Butterfly Exists

Machine learning tools today force users into tradeoffs:

- Ease of use vs flexibility  
- Automation vs transparency  
- Speed vs understanding  

Butterfly rejects these tradeoffs.

It is designed to:
- Work for beginners who want results quickly
- Empower advanced users who want full control
- Remain transparent, explainable, and reproducible

---

### Core Philosophy

Butterfly is built on five principles:

1. **Auto by Default**  
   The system should work without requiring ML expertise.

2. **Manual When Needed**  
   Any automated decision can be overridden by the user.

3. **Hackable Always**  
   Users can inject code, replace logic, or redefine behavior at any stage.

4. **Deterministic & Trustworthy**  
   Same input and same seed must always produce the same output.

5. **Visual, Not Magical**  
   The system must show what is happening and why.

---

### What Butterfly Is Not

Butterfly is explicitly not:
- A command-line tool
- A black-box AutoML service
- A cloud SaaS product (v1)
- A replacement for ML frameworks

Butterfly sits above ML frameworks and below hosted platforms.

---

### Long-Term Direction

Butterfly is intended to evolve into:
- A packaged desktop application
- A modular ML execution engine
- A foundation for experimentation and research tooling

This document defines intent, not implementation.
