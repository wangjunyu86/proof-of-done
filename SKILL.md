---
name: proof-of-done
description: Verify that software an agent or developer claims is finished is genuinely buildable, installable, usable, and deliverable. Use for release acceptance, handoff verification, core-flow testing, real-vs-mock classification, and evidence-backed completion reports; do not use as a general code review or as a substitute for specialized security/compliance audits.
---

# Proof of Done

Prove completion from observable behavior and reproducible evidence. Treat “the code exists,” “the build passed,” and “the product is ready for a person to use” as different claims.

## Operating rule

Never report a feature as working because its code, route, button, or test name exists. A completion claim needs an executed check and retained evidence. If a check cannot be run, label it **unverified** and explain exactly what is missing.

Do not silently repair the product while auditing it. Establish a baseline first. If the user also asks for fixes, preserve the failed evidence, make the smallest justified repair, then rerun the same checks and record before/after results.

## Start with the promised outcome

Identify:

- the product and intended user;
- the artifact the user expects to receive;
- the supported platform and environment;
- the promised core journeys;
- required external services, credentials, devices, or paid accounts;
- which requirements are release-blocking.

Convert vague promises into a claim matrix. Each required claim must have an observable pass condition. If no requirements were supplied, infer a minimal set from the product entry points and clearly label them as inferred.

For a reusable evidence-pack skeleton, run:

```bash
python3 scripts/init_evidence_pack.py <output-directory> --product "<name>"
```

## Verification sequence

Adapt the depth to the release risk, but keep these distinctions:

1. **Inventory** — identify source root, documented entry point, expected artifact, version, target platform, and current repository state.
2. **Clean build** — build from declared source and dependencies rather than trusting an existing artifact. Record exact commands, environment, exit status, and logs.
3. **Artifact identity** — verify the artifact exists, opens as the expected format, has a version/package identity, and can be uniquely identified by hash.
4. **Install or launch** — test the user-facing installation or startup path in the cleanest practical environment. A developer server alone does not prove end-user delivery.
5. **Core journeys** — execute the smallest complete journeys that create user value, including state changes and expected outputs.
6. **Persistence and recovery** — restart or reload where relevant; check that committed data survives and failed operations recover honestly.
7. **Failure behavior** — exercise representative invalid input, permission denial, unavailable service, and offline/timeout behavior when relevant.
8. **Integration reality** — classify login, payment, upload, messaging, AI, maps, and other integrations as real, simulated, or unverified using runtime evidence.
9. **Delivery clarity** — identify one recommended artifact or entry point and write instructions a non-developer can follow.
10. **Verdict** — issue only the verdict supported by the claim matrix.

Read [references/platform-probes.md](references/platform-probes.md) only for the platform being verified. Read [references/evidence-and-verdicts.md](references/evidence-and-verdicts.md) when constructing the manifest or issuing the final verdict.

## Real, simulated, and unverified

Use these labels consistently:

- **Real** — the full operation reached its intended external or persistent boundary and the result was independently observed.
- **Simulated** — fixtures, local stubs, hard-coded success, demo accounts, fake timers, mock servers, or UI-only state produced the result.
- **Unverified** — evidence is insufficient, credentials are unavailable, the environment cannot reach the dependency, or the boundary is ambiguous.

A polished interface is not evidence that an integration is real. Do not attempt real charges, messages, destructive writes, production deployments, or account changes without the user’s explicit authorization immediately before the action.

## Evidence requirements

Prefer evidence another person can inspect or replay:

- command logs with exit codes;
- screenshots or short recordings tied to scenario IDs;
- test traces, network traces, or device logs;
- artifact hashes and metadata;
- persisted records before and after restart;
- environment and dependency versions.

Record secrets only as redacted identifiers. Never place tokens, cookies, payment data, or personal data in an evidence pack.

## Final output

Produce an evidence pack containing at least:

```text
VERDICT.md
proof-manifest.json
claim-matrix.csv
evidence/
logs/
```

The human-facing report must begin with:

1. **Verdict:** Verified / Conditional / Rejected / Inconclusive.
2. **Use this:** the single recommended file, URL, or launch command.
3. **What was actually tested:** environments and journeys.
4. **Release blockers:** failures and unverified required claims.
5. **Reality map:** which integrations are real, simulated, or unverified.
6. **Evidence index:** paths and hashes.
7. **How to reproduce:** concise commands or steps.

Do not say “everything works” when only a subset was tested. State the coverage boundary.

Validate a completed pack with:

```bash
python3 scripts/validate_proof_pack.py <evidence-pack-directory>
```

Use `--allow-draft` only while evidence is still being collected; a final delivery should pass without it.
