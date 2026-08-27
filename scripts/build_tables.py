#!/usr/bin/env python3
"""Regenerate docs/devices.md and data/qc_catalogue.csv from data/qc_catalogue.json.

Run from the repo root:  python3 scripts/build_tables.py
"""
import csv
import json
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "qc_catalogue.json"
MD = ROOT / "docs" / "devices.md"
CSV = ROOT / "data" / "qc_catalogue.csv"

CATEGORY_ORDER = [
    "Guitar amps", "Guitar cabinets", "Guitar overdrive", "Compressor", "EQ",
    "Delay", "Reverb", "Modulation", "Pitch", "Filter", "Wah", "Morph",
    "Utility", "Synth",
]


def control_text(dev):
    if dev.get("controls"):
        parts = []
        for c in dev["controls"]:
            s = c["name"]
            extras = []
            if c.get("type") and c["type"] != "knob":
                extras.append(c["type"])
            if c.get("range"):
                extras.append(str(c["range"]))
            if c.get("default") is not None:
                extras.append(f"default {c['default']}")
            if c.get("page"):
                extras.append(f"p{c['page']}")
            if extras:
                s += " (" + ", ".join(extras) + ")"
            parts.append(s)
        return "; ".join(parts)
    if dev.get("controls_unverified"):
        return "_unverified:_ " + ", ".join(dev["controls_unverified"])
    return ""


def status(dev):
    if dev.get("verified"):
        return "verified"
    if dev.get("controls_unverified"):
        return "unverified"
    return "missing"


def main():
    cat = json.loads(DATA.read_text(encoding="utf-8"))
    devices = cat["devices"]
    groups = OrderedDict((c, []) for c in CATEGORY_ORDER)
    for d in devices:
        groups.setdefault(d["category"], []).append(d)

    total = len(devices)
    verified = sum(1 for d in devices if d.get("verified"))
    unverified = sum(1 for d in devices if not d.get("verified") and d.get("controls_unverified"))

    lines = [
        "# Quad Cortex device database",
        "",
        f"Generated from `data/qc_catalogue.json` (schema v{cat.get('schema_version')}, updated {cat.get('generated')}).",
        "",
        f"**{total} devices**: {verified} verified, {unverified} unverified (wiki-sourced), {total - verified - unverified} still missing controls.",
        "",
        "Status legend: **verified** = transcribed from the Cortex Control parameter editor and checked; "
        "**unverified** = taken from quadcortex.wiki, not yet checked against the device; **missing** = no control data yet.",
        "",
    ]
    for catname, devs in groups.items():
        if not devs:
            continue
        lines += [f"## {catname}", "", "| Device | Based on | Plugin | CorOS | Status | Controls |", "|---|---|---|---|---|---|"]
        for d in sorted(devs, key=lambda x: x["name"].lower()):
            lines.append(
                f"| {d['name']} | {d.get('based_on') or ''} | {d.get('plugin') or ''} | {d.get('added_in_coros') or ''} | "
                f"{status(d)} | {control_text(d)} |"
            )
        lines.append("")
    MD.write_text("\n".join(lines), encoding="utf-8")

    with CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "category", "based_on", "plugin", "added_in_coros", "status", "controls"])
        for d in devices:
            w.writerow([d["name"], d["category"], d.get("based_on") or "", d.get("plugin") or "",
                        d.get("added_in_coros") or "", status(d), control_text(d).replace("_unverified:_ ", "")])
    print(f"Wrote {MD.relative_to(ROOT)} and {CSV.relative_to(ROOT)}: {total} devices, {verified} verified.")


if __name__ == "__main__":
    main()
