#!/usr/bin/env python3
"""Spark penetration-ID test: identify and type every roof penetration
in a photo (Muse Spark 1.3, Meta Model API). Usage: run_pipes.py IMAGE
Auth per custom.meta-model-api CONNECTOR.md (surrogate helpers, api.meta.ai only).
"""
import base64
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

HOST = "api.meta.ai"
URL = f"https://{HOST}/v1/chat/completions"
MODEL = "muse-spark-1.3"
MAX_TOKENS = 12000

PROMPT = """You are the vision inspector for MOC Roofing's estimating system.

STANDING RULE: never manufacture anything. Identify ONLY what is clearly visible
in the photo. If an item is too small, faint, or ambiguous to identify with
confidence, do not guess it into a category - leave it out or note it as
unidentifiable. This is recognition, not forensics.

Inspect the attached roof photo. The assignment: IDENTIFY EVERY ROOF PENETRATION.

A penetration is anything that passes through or mounts through the roof deck:
plumbing vent pipes (with pipe jack flashing: a metal flashing base with a rubber
boot/donut sealing the pipe), dryer vents (a louvered hood vent - low louvered box
with a hooded opening; do NOT call it a generic exhaust cap), louvered static
vents, turbine vents, exhaust flues or caps, attic fans, chimneys, skylights,
conduit, other.

For EACH penetration report:
- type: from the list above, as specific as the image allows. A "3-in-1 pipe jack"
  is a plumbing vent flashed with a one-size flashing (metal base + rubber boot).
- location: where in the image (e.g. "center-left of slope, mid-height")
- count_contribution: 1 each
- condition: anything notable (damage, sealant, rust, boot condition) only if visible

Then give totals: total penetration count and count by type.
Do NOT count shadows, vents on neighboring structures, or items not on this roof.
If you cannot process the image, reply exactly NO_IMAGE.

Output a JSON object in this shape, then one short plain-language summary paragraph:
{
  "penetrations": [
    {"type": "...", "location": "...", "condition": "..."}
  ],
  "total_count": 0,
  "count_by_type": {"...": 0}
}"""


def main():
    img_path = Path(sys.argv[1])
    out_dir = Path(__file__).parent
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
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = read_json_response(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:1500]
        print(f"HTTP {e.code}: {detail}")
        sys.exit(2)
    (out_dir / "pipes-raw-output.json").write_text(
        json.dumps(data, indent=2), encoding="utf-8")
    choice = (data.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content") or ""
    print(f"finish_reason={choice.get('finish_reason')} usage={data.get('usage')}")
    print("=== SPARK CONTENT ===")
    print(content)
    (out_dir / "pipes-answer.md").write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
