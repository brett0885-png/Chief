# Spark roofing-vision test harness

The test harness behind the Chief demo: Muse Spark 1.3 (Meta Model API)
reading real roof photos for MOC Roofing's estimating work, scored against
ground-truth labels written by the roofer himself.

## The standing rule

> **Never manufacture anything. Only what is actually seen is counted.**
> Recognition, not forensics. If an item is too small, faint, or ambiguous to
> identify with confidence, it is left out or flagged — never guessed into a
> category.

This rule is baked into every prompt in this folder, and the results below
are what it produces: conservative counts that a contractor can defend.

## The tests

| Test | Script | What it does | Result |
|---|---|---|---|
| Penetration ID | `run_pipes.py` | Identify and type every roof penetration in a photo | A plumbing vent typed exactly "3-in-1 pipe jack"; after the owner's correction, the louvered vent typed exactly "dryer vent" (`pipes-answer.md`) |
| Hail counts | `run_hail.py` | Count chalk-marked hail hits in close-ups | Spark vs labels: 0, 1, 1, 1, 3, 2, 6, 8, 1, 1 — close-ups exact, wide shots conservative by design (`hail/`) |
| Flat/commercial census | `run_flat.py` | Census HVAC, stacks, vents, hatches, drains on commercial roofs | Trap photos (clean finished roofs) came back clean — nothing invented; distant aerial counts flagged low-confidence and excluded (`flat/`) |
| Demo-flight census | `run_demo_flight.py` | The penetration prompt over 8 drone photos of one completed job | Deduplicated whole-roof census: 9 penetrations, checked against the job's written scope (`demo-flight-nov2.md`, outputs in `demo-flight-nov2/`) |
| Bird-droppings discrimination | `run_birdpoop*.py` | Blind protocol: the prompt never mentions droppings; Spark names what it sees, cold | Droppings named outright and classified **not damage** at every distance tested |
| Ground truth sets | `run_groundtest*.py` | Blind sets shot standing on the roof: deposits on surfaces, dents in metal vents | Droppings identified on both ridge angles; no damage invented on controls |

Ground truth lives in `labels.md` — the owner's labels, verbatim, including
the correction that taught the taxonomy (a louvered hood/box vent of that
style is a **dryer vent**, not a generic exhaust cap) and the adjudication
that Spark's conservative hail counts stand.

`VISION-ROADMAP.md` is the design note: Tier 1 (recognition — what ships)
and Tier 2 (forensics — cause determination from whole-slope pattern plus
close-up evidence, designed, not yet claimed).

## Running it

Python 3, no third-party dependencies for the core scripts (standard library
only). Each script sends photos to the Meta Model API
(`api.meta.ai`, model `muse-spark-1.3`) as base64 image content and writes
the model's raw JSON plus a readable answer next to the inputs.

Authentication is **not** included in this public copy: the originals attach
credentials through a local helper (`add_surrogate_to_request`). To run them
yourself, replace that call with your own Meta Model API key sent as an
`Authorization: Bearer <key>` header.

The eight full-resolution demo-flight originals are not in this repo (they
live in the owner's uploads); `demo-flight-nov2/` holds the frame extracts,
crops, raw API responses, and answers from those runs, and
`demo-flight-nov2.md` is the reconciled write-up.

**Repository contents note:** the JPG test photos themselves are not
mirrored in this GitHub copy — the photos are the job photos shown in the
demo video. Everything else from the runs is here: the scripts and prompts,
the owner's ground-truth labels, every answer file, and the raw API
response JSONs.
