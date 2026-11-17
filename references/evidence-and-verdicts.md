# Evidence and verdict model

## Claim matrix

Each claim should contain:

- `id`: stable identifier such as `FLOW-LOGIN-01`;
- `claim`: one observable promise;
- `priority`: `required` or `optional`;
- `status`: `verified`, `failed`, `partial`, `unverified`, or `not-applicable`;
- `method`: command, scenario, or inspection method;
- `environment`: where it was checked;
- `evidence`: one or more relative paths;
- `notes`: limitations and interpretation.

Keep one claim per row. “The app works” is not a valid claim.

## Verdicts

- **Verified** — every required claim is verified. Optional gaps may be disclosed but cannot contradict the release description.
- **Conditional** — no required claim is known to fail, but one or more required claims are partial or unverified. State the exact condition before use.
- **Rejected** — at least one required claim failed, the advertised artifact is absent, or the user cannot complete a core journey.
- **Inconclusive** — the available environment or evidence is too incomplete to reach one of the other verdicts. This is not a pass.

A build failure normally makes the verdict Rejected. Missing credentials can justify Conditional or Inconclusive, not Verified.

## Manifest shape

`proof-manifest.json` uses this minimum structure:

```json
{
  "schema_version": "1.0",
  "product": "Example",
  "verdict": "conditional",
  "recommended_entry": "dist/example.apk",
  "environments": ["Android 15 emulator"],
  "requirements": [
    {
      "id": "FLOW-01",
      "claim": "A new user can create an account",
      "priority": "required",
      "status": "verified",
      "evidence": ["evidence/FLOW-01.mp4"],
      "notes": "Used a test environment"
    }
  ],
  "artifacts": [
    {
      "path": "artifacts/example.apk",
      "kind": "android-apk",
      "sha256": "<64 lowercase hex characters>"
    }
  ],
  "integrations": [
    {
      "name": "Payment",
      "classification": "simulated",
      "evidence": ["evidence/payment-trace.txt"]
    }
  ],
  "limitations": ["Production payment was not authorized"]
}
```

All paths are relative to the evidence-pack root. Hash delivered artifacts, logs that establish a decisive result, and mutable evidence files when practical.
