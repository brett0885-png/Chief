#!/usr/bin/env python3
"""Bird-poop discrimination test (Nov 2): frames from the 89s demo flight
(clip 2, 29482DE5) over the demo job roof. Blind protocol: Brett never said
which video/timestamp holds droppings; his reference image only defined
what droppings look like (grayish smeared streak, low contrast). This
prompt does NOT mention bird droppings — Spark names what it sees, cold.
Reuses auth + endpoint pattern from run_demo_flight.py.
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

PROMPT = """You are inspecting a drone photo of a residential asphalt-shingle roof.

List every surface mark, deposit, streak, stain, or discoloration you can actually see ON the shingle surface itself. Do not count roof hardware (vents, turbines, skylights, pipe jacks, flashing) and do not count shadows.

For each mark you list, give:
1. Where it is in the frame
2. What it most likely is
3. A classification: DAMAGE or NOT DAMAGE, with a one-line reason

Only report marks that are genuinely visible in this image. Never invent a mark that is not there. If the shingle surface is clean and unmarked, say so plainly."""

SRC = Path("/tmp/poop_test")
ITEMS = [
    ("birdpoop-t36-full", SRC / "clip2_t36.jpg"),
    ("birdpoop-t36-skylight-field", SRC / "crop_skylight_field.jpg"),
    ("birdpoop-t36-turbines", SRC / "crop_turbines.jpg"),
    ("birdpoop-t27-control", SRC / "clip2_t27_control.jpg"),
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
    (out_dir / f"{slug}-raw.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    choice = (data.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content") or ""
    (out_dir / f"{slug}.answer.md").write_text(content, encoding="utf-8")
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
