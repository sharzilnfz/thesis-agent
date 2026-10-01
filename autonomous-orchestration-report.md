# Autonomous Long-Running Orchestration Report

## 1. Project Context
Role: design record for autonomous multi-agent thesis research.
Scope: orchestration layer only. This file is not a thesis chapter. It makes no literature claims and proposes no thesis findings. It therefore requires no ledger backing and triggers none of Gates 1-4.
Tone: academic, rigorous, skeptical, precise, formal.

## 2. Desired Goals
- Run autonomous long-running agents for 1 to 3 days continuously.
- Support orchestration where one agent calls another.
- Terminate only on goal predicate or explicit human stop.
- Apply hill climbing for continuous improvement rather than early stopping.
- Research an LLM thesis without fixing the subtopic prematurely.
- Explore multiple research paths in parallel in a tree structure.
- Avoid fixation on a single path. Prototype several paths, then select on evidence.
- Target a genuine improvement to current LLMs, possibly combining memory, context, retrieval, evaluation, and multi-agent coordination.
- Run locally on the operator machine.
- Use CLI Proxy API to pool multiple subscriptions for token supply.
- Remain fully open to the best outcome.

## 3. Outcomes Definition
Done is defined as three artifacts for at least one path:
1. Problem statement with pain evidence from papers and systems.
2. Proposed solution with mechanism, scope limits, and falsifiable claims.
3. Verification bundle with novelty search, holdout evaluation, and critic report.
No branch is marked done without files on disk. Generation and judgment are separated.

## 4. Proposed Solution Stack
Herdr supplies process survival and visibility. Each agent receives a real terminal. States are blocked, working, done, and idle. The server persists across detach and SSH. The socket API and CLI permit agent-driven spawning and pane reads.

Hermes Agent Kanban supplies the durable work queue. Profiles isolate config, memory, sessions, and gateway per agent. Boards persist tasks in SQLite through triage to done states. The dispatcher reclaims stale claims and crashed workers, promotes ready tasks, and auto-blocks after the failure limit. Workers use board tools for show, heartbeat, complete, block, comment, and attach. Parent links forward handoff summaries. Agent-to-agent protocol permits later cross-machine calls.

OMP, a fork of the Pi coding agent, supplies fast parallel execution. Its task tool fans out subagents under semaphore-bounded concurrency. Isolation uses APFS clones, overlay filesystems, or git worktree fallback. Per-agent model overrides and background jobs are supported. The swarm extension adds YAML DAGs for unattended runs.

Git plus progress files supply cross-context memory, following the Anthropic long-running harness pattern. An initializer writes init.sh, PROGRESS.md, a claims list in JSON, and a baseline commit. Workers read progress plus git log on start. Work is scoped to one claim per session. Each session ends with a commit and progress update.

OpenClaw is excluded as core. It fits operations automation with boards, cron, and browser flows. It adds weight without improving research durability.

OpenCode is excluded as core queue. It fits coding with primary and short-lived subagents. It is weaker than Hermes for multi-day reclaim and audit.

## 5. Tree and Hill-Climbing Design
Single-incumbent hill climbing is rejected. It converges early. The GEAR, fluid search, and AutoResearch literature supports a frontier.

A frontier of 3 to 5 active thesis paths is maintained. Each node holds score, evidence bundle, parent identifier, and run history. Each iteration writes a hypothesis file before search or edit. Each evaluation uses a fixed metric and fixed budget. Keep-or-discard decisions are written to disk. Follow-up work uses new child cards. Completed cards are not reopened.

Budget follows observed progress under a bandit-style portfolio over hill-climbing chains. Weak paths park to idle. Strong paths receive more workers.

## 6. Local Machine and Proxy Wiring
All agents point to one local proxy URL. The proxy owns multi-account round robin and credential refresh. OMP owns role fallback chains for orchestrator, planner, worker, and judge roles. The orchestrator uses a frontier model. Workers use a small model. The judge uses an independent model or setting. Quota and cooldown are tracked in the proxy dashboard.

Local risks are sleep termination, RAM-bounded concurrency, disk growth from transcripts, and rate limiting despite pooled tokens. Mitigations are sleep inhibition during runs, concurrency set from RAM, transcript pruning with summaries retained, and fallback chains with backoff retries.

## 7. Verification Checks
Evidence is split into an optimization set and a holdout set. Workers improve against the optimization set. The judge checks the holdout set. The judge shares no evaluation code with the worker where possible. A critic checks completeness and contradictions. Contradiction rate, staleness, coverage, latency, and token cost are tracked. A default-fail contract requires evidence files before done. Writes to result records require prior reads to prevent false claims.

Memory requires an explicit write path and read path. The write path filters, canonicalizes, dedupes, and scores. The read path uses a fast filter then a reranker and skips retrieval when not needed. Consolidation from episodic to semantic records requires probation and re-verification. Forgetting quality is tested or retrieval precision decays.

## 8. Improvements Under Open Constraints
- Add a nightly distiller that updates the strategy record from all branch logs.
- Add disconfirming-evidence workers that seek refuting papers.
- Add cross-branch merge that combines complementary edits from different branches.
- Add routing by measured cost per verified claim.
- Add a novelty oracle that queries scholarly indexes before promotion.
- Add a one-command rerun artifact per top path.
- Add claim-to-source provenance for every statement advanced toward the thesis.
- Add crash-recovery drills that terminate random workers to prove requeue safety.

## 9. Gate Compliance Statement
- Gate 1: no broad search sweep is launched by this file.
- Gate 2: no evidence is extracted from papers by this file.
- Gate 3: no thesis chapter is written by this file.
- Gate 4: no draft is finalized by this file.
- Citation rule: this file contains no citation commands. All future thesis claims require ledger backing before citation commands are emitted.
- LaTeX integrity: no included files are modified by this file.

## 10. Provenance
Decisions in this file were shaped by poteto-mode principles: guard the context window (summaries at root, transcripts in branches); model the domain (explicit Task, Run, Node, Score schemas); separate before serializing shared state (single writer plus worktrees); make operations idempotent (requeue safety); sequence verifiable units (commit plus eval per loop); prove it works (evidence gate); exhaust the design space (frontier search).
