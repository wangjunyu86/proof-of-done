#!/usr/bin/env python3
"""Create a minimal, non-destructive Proof of Done evidence pack."""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--product", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = args.output.expanduser().resolve()
    if root.exists() and any(root.iterdir()) and not args.force:
        raise SystemExit(f"Refusing to write into non-empty directory: {root}")
    root.mkdir(parents=True, exist_ok=True)
    for name in ("evidence", "logs", "artifacts"):
        (root / name).mkdir(exist_ok=True)

    manifest = {
        "schema_version": "1.0",
        "product": args.product,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "verdict": "inconclusive",
        "recommended_entry": "",
        "environments": [],
        "requirements": [],
        "artifacts": [],
        "integrations": [],
        "limitations": ["Evidence collection has not finished"],
    }
    (root / "proof-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with (root / "claim-matrix.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "claim", "priority", "status", "method", "environment", "evidence", "notes"])

    (root / "VERDICT.md").write_text(
        f"# Proof of Done — {args.product}\n\n"
        "## Verdict\n\nInconclusive — evidence collection has not finished.\n\n"
        "## Use this\n\nNot established.\n\n"
        "## What was actually tested\n\nNothing yet.\n\n"
        "## Release blockers\n\n- Verification is incomplete.\n\n"
        "## Reality map\n\nNot assessed.\n\n"
        "## Evidence index\n\nSee `proof-manifest.json`.\n\n"
        "## How to reproduce\n\nNot established.\n",
        encoding="utf-8",
    )
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
