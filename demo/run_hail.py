#!/usr/bin/env python3
"""Spark hail-count test: count chalk-marked hail hits per photo.
Usage: run_hail.py IMG [IMG ...]  (writes <name>.answer.md beside outputs + hail-results.json)
Auth per custom.meta-model-api CONNECTOR.md (surrogate helpers, api.meta.ai only).
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

STANDING RULE: never manufacture damage. Count ONLY what is clearly visible in
the photo. A faint, partial, or ambiguous mark is NOT counted - report it under
notes as "seen but not countable" if you mention it at all. This is recognition,
not forensics: identify what can actually be seen, nothing more.

Inspect the attached close-up photo of asphalt shingles. A human inspector has
already marked hail hits with chalk: light tan/white parenthesis pairs ( ),
circles, or X marks drawn around each hit.

Count the CHALK-MARKED hits:
- Each complete parenthesis pair, closed circle, or X = ONE marked hit.
- Chalk letters, numbers, or slope notes (e.g. "4-12") are NOT hits.
- A red paint dot, if present, counts as ONE marked hit; say so.

Separately, report any clear hail fracture you can see that is NOT chalk-marked
(crushed granule spot / dark fracture). If none, say none.

Output ONLY a JSON object:
{"marked_hits": 0, "markers": ["location + mark type", "..."],
 "unmarked_fractures": ["..."], "notes": "..."}"""


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
    out = Path(__file__).parent / "hail" / (p.stem + ".answer.md")
    out.write_text(content, encoding="utf-8")
    return p.name, content


def main():
    imgs = sys.argv[1:]
    results = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        for name, content in ex.map(run_one, imgs):
            results[name] = content
            print(f"--- {name} ---")
            print(content)
            print()
    (Path(__file__).parent / "hail" / "hail-results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
