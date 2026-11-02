#!/usr/bin/env python3
"""Spark census test: roof-item census on a photo (flat/commercial or slope).
Usage: run_flat.py IMG [IMG ...]
"""
import base64
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

HOST = "api.meta.ai"
URL = f"https://{HOST}/v1/chat/completions"
MODEL = "muse-spark-1.3"
MAX_TOKENS = 8000

PROMPT = """You are the vision inspector for MOC Roofing's estimating system.

STANDING RULE: never manufacture anything. Count ONLY items you can clearly see
and identify. Never estimate counts for distant, tiny, or background items -
if a region is too far away to resolve, exclude it and say so in notes. A low
count of certain items beats a big count of guesses. This is recognition, not
forensics.

Census every distinct roof item visible in this photo. Count carefully; do not
double-count the same item.

Categories:
- hvac_units: rooftop condenser / packaged HVAC units
- vent_stacks: plumbing vent pipes or exhaust stacks sticking up from the roof
- roof_vents: attic vents of any kind (louvered slant-back, turbine, power vent, ridge)
- flues_chimneys: furnace/water-heater flues, chimney structures
- other_items: roof hatches, curbs, drains, skylights, line-set wall penetrations -
  name each kind with its count.

Also report: roof_system (e.g. white coating over membrane, TPO, shingle slope,
mixed) and work_in_progress (is coating/painting/install work visibly underway?
describe briefly), plus duplicate_note if the photo looks like a generic scene
with nothing countable.

Output ONLY a JSON object:
{"hvac_units": 0, "vent_stacks": 0, "roof_vents": 0, "flues_chimneys": 0,
 "other_items": {"kind": 0}, "items_total": 0, "roof_system": "...",
 "work_in_progress": "...", "confidence": "high|medium|low",
 "notes": "..."}"""


def run_one(img_path):
    p = Path(img_path)
    b64 = base64.b64encode(p.read_bytes()).decode()
    body = json.dumps({
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ],
        }],
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.meta-model-api", allowed_hosts=[HOST])
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = read_json_response(resp)
        content = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    except Exception as e:
        content = f"ERROR: {e}"
    out = Path(__file__).parent / "flat" / (p.stem + ".answer.md")
    out.parent.mkdir(exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return p.name, content


def main():
    results = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        for name, content in ex.map(run_one, sys.argv[1:]):
            results[name] = content
            print(f"--- {name} ---")
            print(content)
            print()
    (Path(__file__).parent / "flat" / "flat-results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
