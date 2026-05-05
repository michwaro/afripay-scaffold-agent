# Capstone Spec — AfriPay Security Scaffold Agent

## Problem statement
Every African software engineer has written the same M-Pesa, Paystack, 
or Flutterwave integration multiple times — usually unsafely: no webhook 
signature verification, no idempotency, no structured retry logic, and 
no tests. The result is production incidents, duplicate charges, and 
security gaps. AfriPay Security Scaffold Agent solves this by accepting 
a natural-language integration request and generating production-ready, 
security-hardened scaffolds for the major African payment and 
communications APIs — complete with tests — in under 60 seconds.

Target users: African backend engineers (Python/Node) building fintech 
or e-commerce products who need battle-tested integration code fast.

## What success looks like (acceptance criteria)
- [ ] Given a CLI prompt like "Generate an M-Pesa STK Push integration 
      for FastAPI", the agent produces a complete scaffold: auth, push 
      initiation, callback handler, webhook signature verification, 
      idempotency key handling, and structured error mapping.
- [ ] The scaffold includes a test file (pytest or vitest) covering the 
      happy path and at least two error cases (network timeout, 
      invalid signature).
- [ ] The agent supports at least three providers: M-Pesa Daraja, 
      Paystack, and Africa's Talking SMS.
- [ ] All generated code passes its own test suite when run against 
      provider sandbox credentials.
- [ ] The agent produces a README section explaining the security 
      decisions made (why signature verification, why idempotency keys).

## Architecture sketch
- A CLI entry point (Typer) that accepts provider name + framework + 
  optional feature flags (e.g., --with-retries, --with-tests)
- A Codex agent loop that reads a provider spec file (JSON describing 
  endpoints, auth, webhook format) and generates the scaffold
- A security rules layer: a structured YAML file encoding required 
  security checks per provider (signature header names, HMAC algorithms)
- An output formatter that writes clean, annotated code to ./output/

## Tech stack
- Language: Python 3.11
- Key libraries: openai, typer, rich, httpx, pytest
- External services: M-Pesa Daraja sandbox, Paystack test mode, 
  Africa's Talking sandbox
- Codex surface: VS Code extension (dev) + Codex Cloud (Week 3 builds)

## Task list (in order)
1. [ ] Set up repo: pyproject.toml, CLI skeleton with `scaffold` command 
       that accepts --provider and --framework flags, placeholder output
2. [ ] Create provider spec files (JSON) for M-Pesa Daraja, Paystack, 
       Africa's Talking — encoding endpoints, auth type, webhook schema
3. [ ] Create security rules YAML: signature algorithms, required headers, 
       idempotency key strategy per provider
4. [ ] Build the Codex agent loop: reads provider spec + security rules, 
       generates scaffold code, writes to ./output/
5. [ ] Add test generation step: agent appends a test file covering 
       happy path + signature failure + timeout scenarios
6. [ ] Add README generation step: agent explains the security decisions 
       made in plain English
7. [ ] End-to-end test: run scaffold for all three providers, confirm 
       generated tests pass in sandbox mode
8. [ ] Polish CLI output with Rich (progress, diff preview, success summary)

## Out of scope (MVP)
- Web UI or dashboard
- More than three providers (Flutterwave, Termii, etc. — post-MVP)
- Real transaction execution (sandbox only for the demo)
- OAuth flows (API key auth only for MVP)

## Open questions
- Which framework to default to if --framework is omitted (FastAPI vs 
  Express)? Decision: FastAPI (Python-first audience)
- How to handle providers that change their webhook signature algorithm? 
  Store in spec file, flag as "verify before use"