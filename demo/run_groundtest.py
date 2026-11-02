#!/usr/bin/env python3
"""Ground test set (Nov 2): 6 photos Brett took standing on the roof —
clean shingle field, vent domes, turbines, unlabeled. Blind protocol:
one identical prompt for all six covering (1) deposits on any surface
and (2) dents in metal vents. Brett holds the ground truth and reveals
it after the run. Same auth/model pattern as run_demo_flight.py.
"""
import base64
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

HOST = "api.meta.ai"
URL = f"https://{HOST}/v1/chat/completions"
MODEL = "muse-spark-1.3"
MAX_TOKENS = 12000

PROMPT = """You are inspecting a close-range photo taken on a residential roof. Examine every surface in the photo — the shingles and any metal hardware (vent domes, wind turbines, flashing).

Answer two things:

1) DEPOSITS: List any surface deposit, streak, stain, or discoloration you can actually see, on any surface. For each one give: where it is, what it most likely is — name it specifically if you can (for example bird droppings, algae, rust, dirt, oxidation, sealant) — and a classification of DAMAGE or NOT DAMAGE with a one-line reason.

2) DENTS: If the photo shows a metal vent (a dome or a turbine), inspect the metal for dents, creases, dings, or bent vanes. List each one you can genuinely see, with its location. If the metal shows no dents, say so plainly.

Only report what is genuinely visible in the image. Never invent a deposit or a dent that is not there. If a surface is clean and undamaged, say so plainly."""

FILES = Path.home() / "workspace" / "user" / "files"
ITEMS = [
    ("g1-dome-blurry", FILES / "DED51BB4-5C8F-44B7-9CC6-13D6B6C1DE7F-photo-3840C87B-9082-4231-8265-8269BFC62023.jpg"),
    ("g2-dome-close-a", FILES / "7AA61544-D94B-4C2F-8116-FFA94EF0C853-photo-CF89B3DD-73FD-4C26-B93D-A5A0E0713F51.jpg"),
    ("g3-dome-close-b", FILES / "854FC03A-E0F7-434E-9BDC-7241BAE68678-photo-2962916E-B45C-4705-AC6F-B6EED137EC3E.jpg"),
    ("g4-turbine-top", FILES / "C0F9CF92-2462-400A-A98B-C2B89BC0A2E1-photo-EAE23D29-B83C-4C1E-9475-F3033C3713B1.jpg"),
    ("g5-turbine-side", FILES / "18C3745F-E6F3-496A-BBE9-002D1F92BAE0-photo-1169D179-77D4-4A7A-86A7-4E41336F3D1D.jpg"),
    ("g6-field-clean", FILES / "B8ECCE5B-3BF2-4EBC-9F88-1C12E7D60136-photo-86997B99-8F23-48F4-A093-BABBA816C943.jpg"),
]


def run_one(slug, img_path, out_dir):
    b64 = base64.b64encode(img_path.read_bytes()).decode()
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
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = read_json_response(resp)
    (out_dir / f"ground-{slug}-raw.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    choice = (data.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content") or ""
    (out_dir / f"ground-{slug}.answer.md").write_text(content, encoding="utf-8")
    print(f"[{slug}] finish={choice.get('finish_reason')} usage={data.get('usage')}")
    print(content)
    print("=" * 70)
    return content


def main():
    out_dir = Path(__file__).parent / "demo-flight-nov2"
    out_dir.mkdir(exist_ok=True)
    for slug, path in ITEMS:
        try:
            run_one(slug, path, out_dir)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:800]
            print(f"[{slug}] HTTP {e.code}: {detail}")


if __name__ == "__main__":
    main()
