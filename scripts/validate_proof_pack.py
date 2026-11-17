#!/usr/bin/env python3
"""Validate Proof of Done manifest consistency and referenced evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

VERDICTS = {"verified", "conditional", "rejected", "inconclusive"}
STATUSES = {"verified", "failed", "partial", "unverified", "not-applicable"}
PRIORITIES = {"required", "optional"}
CLASSIFICATIONS = {"real", "simulated", "unverified"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    errors: list[str] = []

    for required in ("VERDICT.md", "claim-matrix.csv", "proof-manifest.json", "evidence", "logs"):
        if not (root / required).exists():
            errors.append(f"missing required path: {required}")

    manifest_path = root / "proof-manifest.json"
    if not manifest_path.is_file():
        print("INVALID\n- " + "\n- ".join(errors))
        return 1
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"INVALID\n- cannot parse proof-manifest.json: {exc}")
        return 1

    verdict = data.get("verdict")
    if verdict not in VERDICTS:
        errors.append(f"invalid verdict: {verdict!r}")

    requirements = data.get("requirements")
    if not isinstance(requirements, list):
        errors.append("requirements must be a list")
        requirements = []
    seen: set[str] = set()
    required_statuses: list[str] = []
    for index, item in enumerate(requirements):
        if not isinstance(item, dict):
            errors.append(f"requirements[{index}] must be an object")
            continue
        rid = item.get("id")
        if not isinstance(rid, str) or not rid.strip():
            errors.append(f"requirements[{index}] has no id")
        elif rid in seen:
            errors.append(f"duplicate requirement id: {rid}")
        else:
            seen.add(rid)
        if not item.get("claim"):
            errors.append(f"requirement {rid or index} has no claim")
        priority = item.get("priority")
        status = item.get("status")
        if priority not in PRIORITIES:
            errors.append(f"requirement {rid or index} has invalid priority: {priority!r}")
        if status not in STATUSES:
            errors.append(f"requirement {rid or index} has invalid status: {status!r}")
        if priority == "required" and status in STATUSES:
            required_statuses.append(status)
        for rel in item.get("evidence", []):
            if not (root / rel).is_file():
                errors.append(f"requirement {rid or index} references missing evidence: {rel}")

    for index, item in enumerate(data.get("integrations", [])):
        if item.get("classification") not in CLASSIFICATIONS:
            errors.append(f"integrations[{index}] has invalid classification")
        for rel in item.get("evidence", []):
            if not (root / rel).is_file():
                errors.append(f"integration {item.get('name', index)} references missing evidence: {rel}")

    for index, artifact in enumerate(data.get("artifacts", [])):
        rel = artifact.get("path")
        digest = artifact.get("sha256")
        path = root / rel if isinstance(rel, str) else None
        if path is None or not path.is_file():
            errors.append(f"artifacts[{index}] references missing file: {rel!r}")
            continue
        if not isinstance(digest, str) or not HEX64.match(digest):
            errors.append(f"artifacts[{index}] has invalid sha256")
        elif sha256(path) != digest:
            errors.append(f"artifacts[{index}] sha256 mismatch: {rel}")

    if not args.allow_draft:
        if not requirements:
            errors.append("final pack has no requirements")
        if verdict == "verified" and any(s != "verified" for s in required_statuses):
            errors.append("verified verdict requires every required claim to be verified")
        if verdict == "rejected" and "failed" not in required_statuses:
            errors.append("rejected verdict should identify at least one failed required claim")
        if verdict == "conditional" and "failed" in required_statuses:
            errors.append("conditional verdict cannot contain a failed required claim")
        if verdict == "inconclusive":
            errors.append("final pack cannot remain inconclusive")
        if not data.get("recommended_entry") and verdict in {"verified", "conditional"}:
            errors.append("verified/conditional pack needs recommended_entry")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
