# Demo-flight penetration census — a completed MOC Roofing job in Texas
## DJI flight photos, Mon Nov 2, 2026 — Meta hackathon demo reads

- **Model:** Muse Spark 1.3 (`muse-spark-1.3`, Meta Model API, image_url data-URIs)
- **Harness:** existing spark-roofing set — prompt imported verbatim from `run_pipes.py`;
  driver `run_demo_flight.py`; per-photo raw JSON + answers in `demo-flight-nov2/`
- **Taxonomy applied:** Brett's labels.md, incl. the Oct 31 correction — a louvered
  hood/box vent of that style is a **dryer vent**, not a generic exhaust cap.
- **Seen-only rule:** only what is actually visible is counted. Nothing inferred,
  no damage claimed unless plainly visible. Ambiguous items are flagged, not guessed.

### Prompt used (verbatim from run_pipes.py)

> You are the vision inspector for MOC Roofing's estimating system.
>
> STANDING RULE: never manufacture anything. Identify ONLY what is clearly visible
> in the photo. If an item is too small, faint, or ambiguous to identify with
> confidence, do not guess it into a category - leave it out or note it as
> unidentifiable. This is recognition, not forensics.
>
> Inspect the attached roof photo. The assignment: IDENTIFY EVERY ROOF PENETRATION.
>
> A penetration is anything that passes through or mounts through the roof deck:
> plumbing vent pipes (with pipe jack flashing: a metal flashing base with a rubber
> boot/donut sealing the pipe), dryer vents (a louvered hood vent - low louvered box
> with a hooded opening; do NOT call it a generic exhaust cap), louvered static
> vents, turbine vents, exhaust flues or caps, attic fans, chimneys, skylights,
> conduit, other.
>
> For EACH penetration report: type (as specific as the image allows; a "3-in-1 pipe
> jack" is a plumbing vent flashed with a one-size flashing, metal base + rubber
> boot), location, count_contribution 1 each, condition only if visible.
> Then totals by type. Do NOT count shadows, vents on neighboring structures, or
> items not on this roof. Output JSON + one short summary paragraph.

---

## (a) Per-photo census (Spark's reads)

### Photo 1 — top-down wide (whole roof)
4 features, all **unidentifiable** at this distance: 2 on the central slope
(left/right of center, upper third), 2 on the right (north-wing) mass near the
ridge. No types assigned — resolution too low. No condition readable.

### Photo 2 — top-down wide (near-duplicate of 1)
3 features, all **unidentifiable** small round penetrations (1 central, 2 on the
right mass). Same roof, same features as photo 1 — one dot not resolved in this frame.

### Photo 3 — top-down wide (near-duplicate)
4 features, all **unidentifiable** (2 central slope, 2 right mass below ridge).
Consistent with photos 1–2. No types, no condition.

### Photo 4 — slope close-up (main/central slope) — best view of this slope
3 penetrations:
- **Round vent cap** — center-right, just below ridge (Spark: "exhaust cap";
  round flat cap, louvers/turbine detail not resolvable — see ambiguity note)
- **Small vent, unidentifiable** — center-left, just below ridge (too small to
  type as static/dryer/exhaust)
- **Plumbing vent pipe** — far right edge near ridge (flashing/boot not resolvable)

### Photo 5 — oblique (main mass from rear)
2 penetrations on the main slope:
- **Turbine vent (probable)** — lower, on the ridge (backlit; "probable" per Spark)
- **Round vent cap, type unconfirmed** — center-upper, just below ridge
Position-consistent with photo 4's small vent + round cap seen from the other side.

### Photo 6 — top-down, north wing
4 penetrations, all on the lower (south-facing) hip of the north wing:
- **Turbine vent ×2** — just below the ridge, left and left-center
- **Skylight ×1** — mid-slope, square glass + frame, intact
- **Pipe jack (plumbing vent w/ flashing) ×1** — mid-slope, left of the skylight
(Tiny dots elsewhere excluded by Spark per the seen-only rule — those are the
main-mass features at distance.)

### Photo 7 — close top-down (north wing) — best view of this wing
4 penetrations:
- **Pipe jack ×3** — one upper-left of the skylight; two grouped lower-center
  (one short, one tall) near the hip; flashing bases + boots appear intact
- **Skylight ×1** — left-center; dome intact; **lower curb flashing shows exposed
  fasteners** (visible detail noted by Spark — a flashing detail, not damage)

### Photo 8 — oblique (north wing)
4 penetrations:
- **Turbine vent ×2** — just below ridge, left and right of center (louvered
  vanes visible here — confirms photo 6's turbine read)
- **3-in-1 pipe jack ×1** — lower-center, just above the skylight; metal base +
  rubber boot visible
- **Skylight ×1** — bottom-right edge, partially cropped; frame + glass intact

---

## (b) Deduplicated whole-roof census

The 3 wide shots are the same roof (not triple-counted). Photos 6/7/8 are three
views of the **north wing**; photos 4/5 are two views of the **main/central mass**;
the wides reconcile as 2 dots on the central slope + 2 dots (the turbines) on the
north wing. Subsets across views were merged by position, taking the clearest
view's type.

### North wing (photos 6 + 7 + 8 — high confidence, 3 corroborating views)
| Type | Count |
|---|---|
| Turbine vents (whirlybirds) | **2** |
| Pipe jacks — plumbing vents w/ pipe-jack flashing (incl. 3-in-1) | **3** |
| Skylight | **1** |
| **Subtotal** | **6** |

### Main / central roof mass (photos 1–5)
| Type | Count | Confidence |
|---|---|---|
| Round vent cap (type not further resolvable) | **1** | seen in photos 4 + 5 |
| Small vent — probable turbine vent | **1** | type = moderate confidence (photo 5 read; unidentifiable in photo 4) |
| Plumbing vent pipe (flashing/boot not resolvable) | **1** | photo 4 only |
| **Subtotal** | **3** | |

### WHOLE ROOF — TOTAL: 9 penetrations
| Type | Count |
|---|---|
| Pipe jacks / plumbing vents | **4** (3 confirmed w/ flashing on north wing + 1 small pipe, main mass) |
| Turbine vents | **3** (2 confirmed + 1 probable) |
| Skylight | **1** |
| Round vent cap, type indeterminate | **1** |
| Dryer vent | **0** — none seen; no louvered hood/box vent appears in any photo |
| Chimney | **0** — none seen |

### Damage
**None claimed.** No damage is plainly visible in any of the 8 photos. Only
condition note: exposed fasteners on the skylight's lower curb flashing (photo 7)
— a visible flashing detail, reported as seen, not as damage.

---

## Ambiguous / low-confidence items (flagged, not guessed)
1. **Main-mass small vent** (photo 4 center-left / photo 5 lower ridge): typed
   "turbine vent" by Spark in photo 5 only, and only as *probable*; unidentifiable
   in photo 4. Counted once, type moderate-confidence.
2. **Main-mass round cap** (photos 4 + 5): Spark called it "exhaust cap" in
   photo 4. It is a round flat cap — NOT the louvered hood/box style Brett taught
   as a dryer vent, so it is **not** reclassified as a dryer vent; recorded as
   "round vent cap, type indeterminate."
3. **Main-mass plumbing pipe** (photo 4, far right): pipe seen; flashing base/boot
   not resolvable, so "pipe jack" typing is by form only.
4. **Wide shots (photos 1–3):** all features unidentifiable by type — used only
   for position reconciliation, never for typing. Counts vary 3–4 dots across the
   three frames (resolution), reconciled to the close-up views.
5. **Photo 6 note:** Spark excluded additional faint dots on the far slope per
   the seen-only rule; those correspond to main-mass features already counted.

## Files
- Raw API responses: `demo-flight-nov2/photo*-raw.json`
- Spark answers: `demo-flight-nov2/photo*.answer.md`
- Driver: `run_demo_flight.py` (prompt imported from `run_pipes.py`, unchanged)

## Ground-truth check — the census vs the job's written scope

The flight covered a roof MOC Roofing completed in Texas in 2026. The demo's
verification thesis: written scope → completed roof → a drone census checks the
finished work against the paper.

| Item | Written scope | Spark census (seen-only) |
|---|---|---|
| Pipe jacks | 8 | 4 |
| Turbine vents | 4 | 3 (2 confirmed + 1 probable) |
| Skylight | not a scope line | 1 seen |
| Chimney flashing | in scope | no chimney seen in these angles |
| Round vent cap | not a scope line | 1 seen, type indeterminate |

Reconciliation (inference, not fact): the unseen items most plausibly sit on
the outbuilding that is in the scope but was not covered by the flight photos,
on shadowed slopes, and in areas covered only by the wide shots where Spark
declined to type. The gap is the seen-only rule working as designed: Spark
reported what was visible and flagged uncertainty rather than matching the
paper. An aerial census pairs with scope/ground verification in the estimator;
it does not replace it.

**Correction (the owner, 2026-11-02):** the written scope's pipe-jack count of
8 was itself wrong — the paper is NOT ground truth on that line, and the
physical count is being settled from the carrier's estimate. Treat the
pipe-jack row as unresolved in both directions: census 4 seen vs scope 8
written. The census runs both ways: it catches work the paper claims that
isn't there, and paper that overcounts — the tool's job is to stop an
overcharge or an undercharge before it ships.
