# Power amplifier history

> **Lifecycle: HISTORY.** Superseded intermediate evidence; do not use as current build instructions. The [current amplifier authority](../POWER_AMPLIFIER.md) owns the rev0 selection and checks.

## 1 Interim layout reviews

#### 1.1.1 Partial PCB layout review, 17 October 2026

This scoped review uses the later saved `diptrace/main_board.dipxml` snapshot
(SHA-256 `389DD99BB87C6C677D456D136A3D1DE6C2FCE311C0A73FBAFE4D3C675892D5C9`).
It supersedes the initial same-day layout snapshot (SHA-256
`1EACC84D71C0D4E66B5274B59D91BD749946774151944548C70A006004424088`),
which had only bottom-layer copper pours. The assessment is from saved XML
geometry and filled copper near U3, not DipTrace DRC, fabrication output or a
physical measurement. The other board sections remain early placement, and
many nets are deliberately unrouted. The schematic and PCB place the selected
Würth `885012208124` 2.2 µF, 100 V, 1206 capacitors at C21/C22/C24/C25;
their 36 V biased performance is model-based and mechanical fit is still open.

**Local PVDD loop — promising, still to verify in the finished board.** The
four ceramics and four 33 nF bootstrap capacitors are on the IC side. Each
PVDD bank has two capacitors between bottom-side 36 V and GND copper close to
its U3 pins. The local copper appears to connect both terminals directly to
the corresponding pins, including the adjacent U3 GND pins. This is the
critical high-frequency commutation loop; a distant bulk capacitor or via
count cannot repair a detour here. The new Inner 1 36 V and Inner 2 GND pours
also connect to local via fields. Their saved fills have clearance openings
but no obvious complete cut through the amplifier region; continuity and
local neck widths still need checking after the rest of the routing settles.

The saved 0.20 mm-wide bootstrap traces are approximately 5.3 mm for A/D and
9.2/9.0 mm for B/C, measured along their routed centre lines. **Correction to
the initial review:** this length difference is not a length-matching defect
and is not, by itself, grounds to move B/C. With an illustrative 35 µm copper
thickness, 4 mm of extra 0.20 mm-wide copper adds about 10 mΩ at room
temperature: `R = ρl/(wt) ≈ (1.7 × 10⁻⁸ Ω·m)(0.004 m) /
(0.0002 m × 35 × 10⁻⁶ m) ≈ 0.010 Ω`. The associated `RC` contribution with
33 nF is about 0.33 ns. Trace inductance cannot be inferred from length alone;
it depends on the complete BST-capacitor-OUT loop and the proximity of its
outgoing and returning paths. TI specifies a local 33 nF capacitor between
each BST and OUT pin, not equality of the four connection lengths. Retain the
current same-side placement unless the completed loop has a clearly excessive
area, a plate-clearance problem, or observed switching-related trouble. Keep
the capacitor and its switching-node pads out of the eventual grounded metal
contact area. [TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).

**Output paths and via fields — directionally sound.** Each U3 switching
output runs through bottom-side copper and a local via group into a top-side
switching-node pour reaching its own inductor input pad. The saved groups have
six A, eight B, eight C and six D vias. **Correction to the earlier review:**
that snapshot has one via style, a 0.40 mm land and 0.20 mm hole, used by
the placed via components; the former 0.50/0.25 mm description was wrong.
The B/C pours have short narrow throats near U3 before widening. The
0.40 mm bottom traces on these output nets connect bootstrap capacitor pads;
they are not the sole speaker-current route. L1/L3 outputs join `SPK+` and
L2/L4 join `SPK-`, matching the intended post-filter parallel topology. The
80 `SPK+` vias are grouped by its two output pads; the saved inner 36 V and
GND fills route around their clearance openings and remain broad between the
inductors. Their number alone does not identify a fault, nor does this XML
inspection prove current sharing or fabrication suitability. Check the final
drill/plating, annular rings, clearance and local copper widths against the
selected fabricator and stack-up.

**470 µF bulk integration — unfinished.** C20 and C26 are currently unrouted.
C20's top-side positive and ground pads project into the local 36 V and GND
inner pour outlines, respectively; broad, short pad-to-plane connections with
local vias appear feasible. C26 sits roughly 40 mm farther across the board and
outside those local pours. Its placement therefore needs either an extension
of both low-impedance rail and return copper or a move nearer the amplifier
region. There is no need to force either large capacitor's terminals directly
beside the 2.2 µF pads: the ceramics supply the very short switching-current
loop, while the bulk parts support the rail over longer intervals. Keep the
bulk feed and return together and avoid a thin, long single rail trace with a
remote return. TI calls for bulk capacitors close to the device with wide,
direct connections and ceramics at the pins in its
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).

Finish C20/C26 rail and return connections, then inspect the filled copper
around local antipads and run DipTrace connectivity/DRC. Review the resulting
manufacturing outputs once the layer stack and via construction are chosen.
This partial snapshot establishes neither an open or short nor fabrication
readiness.

#### 1.1.2 Via barrel resistance estimate, 17 October 2026

This is an illustrative DC estimate for the then-saved via style, not a
measured value or via-current rating. That XML snapshot contained one
`ViaStyle` with a 0.40 mm land and 0.20 mm hole; all 202 placed via
components referenced it. **Correction, 17 October:** 129 bottom-layer route
points also carried a `ViaStyle` attribute, but this attribute is present on
ordinary same-layer trace points and does not establish another 129 drilled
vias. The placed via components are ordinary through vias, so a connection between two
layers uses only the intervening length of the same plated barrel. For a
thin copper cylinder, the conducting cross-section is approximately its
circumference times wall thickness, `A ≈ πdt`; hence
`R ≈ ρℓ/(πdt)`. Use copper resistivity `ρ = 1.724 × 10⁻⁸ Ω·m` at 20 °C,
effective barrel diameter `d ≈ 0.20 mm`, and JLCPCB's published **average**
hole plating `t = 18 µm`. The diameter approximation sits between treating
0.20 mm as the drill size or as the finished hole; either interpretation
changes this thin-wall result by roughly 10%.

For nominal layer spacing, JLCPCB's 1.6 mm four-layer
`JLC04161H-7628` stack has 0.2104 mm outer prepreg on each side and a
1.065 mm central core, with 0.035 mm outer and 0.0152 mm inner copper. Taking
the centre of each copper layer as the barrel connection point gives these
resistances in **mΩ per via**:

| From / to | Top (L1) | Inner 1 (L2) | Inner 2 (L3) | Bottom (L4) |
| --- | ---: | ---: | ---: | ---: |
| **Top (L1)** | — | 0.36 | 2.01 | 2.36 |
| **Inner 1 (L2)** | 0.36 | — | 1.65 | 2.01 |
| **Inner 2 (L3)** | 2.01 | 1.65 | — | 0.36 |
| **Bottom (L4)** | 2.36 | 2.01 | 0.36 | — |

For example, top-to-bottom uses approximately 1.551 mm of barrel and
`A ≈ π(0.20 mm)(0.018 mm) = 0.0113 mm²`, giving about 2.36 mΩ at 20 °C.
At an illustrative 15–25 µm plating thickness, that full-length result
would be about 2.8–1.7 mΩ; these thicknesses are a sensitivity check, not
JLCPCB's guaranteed limits. A 40 °C copper temperature rise increases
resistance by roughly 16%. Pad entry, plane spreading and uneven sharing
between parallel vias are outside the table. For the output transitions,
six or eight perfectly sharing bottom-to-top vias would contribute roughly
0.39 or 0.30 mΩ of barrel resistance per output path. Their high-frequency
loop inductance and the copper approaching them still matter separately.

**Via-size clarification, checked against JLCPCB on 17 October 2026.** For
multilayer boards, JLCPCB lists a 0.15 mm hole / 0.25 mm land as its minimum;
the 0.10/0.20 mm option is limited to boards at most 1 mm thick and requires
ENIG or OSP. JLCPCB separately *prefers* a minimum 0.20 mm hole and a land
diameter at least 0.15 mm larger than its hole. The then-saved 0.40/0.20 mm via
exceeds both dimensions and is within the stated multilayer capability. Its
nominal radial annular width is `(0.40 − 0.20)/2 = 0.10 mm`. The separate
pricing note says a 0.20 or 0.25 mm hole with a land below 0.45 mm costs
more, so this style may incur that order option; this is a cost distinction,
not a manufacturability objection. The saved PCB snapshot now has the
JLC-style 0.2104/1.065/0.2104 mm dielectric spacing and 0.5 oz inner copper
(SHA-256 `81FB8DBE754FB401DD005EFAB417E5D4240B270DEFCB242BD370080CF0DC4902`),
matching the cited stack-up at the nominal-design level. The resistance grid
remains an estimate based on JLCPCB's published finished-layer figures.
Check the order options and final DFM result before release.
[JLCPCB layer stack](https://jlcpcb.com/impedance);
[JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-).

#### 1.1.3 Via-field current and plane review, 17 October 2026

**Saved snapshot at this review:** `diptrace/main_board.dipxml`, SHA-256
`99E9B07AEE658C687996786E875CDE4C5B4482044383EEC3E1AC2DB2078DAB10`.
It has 202 placed plated-through vias. Their one style is now **0.45 mm land /
0.20 mm hole**, superseding the 0.40 mm land in the earlier snapshots. At
0.5 mm pitch, neighbouring lands are only 0.05 mm apart, and their clearance
openings in other-net planes merge. JLCPCB's special-price condition for a
0.20 mm hole is a land *below* 0.45 mm, so the current nominal size sits at
that boundary. The barrel-resistance grid above remains approximately valid
because the drill and assumed plating have not changed; the annular width is
now 0.125 mm.

The following are **illustrative operating currents**, not via-current
ratings. At 150 W into a nominal, resistive 4 Ω speaker,
`I_speaker,rms = sqrt(150/4) = 6.12 A` and
`I_speaker,peak = sqrt(2) × 6.12 = 8.66 A`. Equal sharing by the two PBTL
inductors on each side gives 3.06 A RMS and 4.33 A audio peak per output
branch. The approximate 1.5 A peak-to-peak switching ripple in each 10 µH
inductor raises a coincident branch peak to roughly 5.1 A. These are design
point estimates, not a bound on real loudspeaker-impedance dips or a fault.
At an illustrative 90% amplifier efficiency, average 36 V input current is
`150/(0.90 × 36) = 4.63 A`; the selected supply is rated 5.56 A continuous.
Neither number bounds instantaneous rail current supplied by the bulk and
ceramic capacitors. TI's 22 kΩ OC_ADJ example lists a 16.3 A cycle-by-cycle
threshold **per half-bridge**, followed by shutdown for persistent overload;
that is a short fault pulse case, not continuous via-current demand.

| Field in current XML | Via count and likely transition | Credible design-point current through field | Assessment |
| --- | --- | --- | --- |
| `AMP_OUT_A/D` | 6 each, bottom to top | Approximately 3.06 A RMS and 5.1 A combined audio/ripple peak per branch | Keep. Six spread connections give nominal 0.39 mΩ barrel resistance and about 3.7 mW total barrel loss at 3.06 A RMS. Their location and switching-loop geometry matter more than saving two vias. |
| `AMP_OUT_B/C` | 8 each, bottom to top | Same branch estimate | Keep. Eight give approximately 0.30 mΩ and 2.8 mW at the design point. The narrow copper throats nearer U3 remain the more useful item to inspect. |
| `SPK+`, beside L1 and L3 | 40 in each field, top to bottom | Ideally 3.06 A RMS from its inductor; use 6.12 A RMS as a conservative one-field current-transfer check | Electrically well past diminishing returns. Eight well-connected vias would have about 0.30 mΩ barrel resistance and 11 mW barrel loss even at 6.12 A; 12–16 well-spread vias per field offer geometric margin. The two current 40-via patterns make joined clearance openings in both inner planes. Reduce them if the final 36 V or GND copper is narrowed or return paths are diverted; retaining them is reasonable if the filled planes remain broad and continuous. |
| Local `36V` | 19, mainly bottom to Inner 1 | Up to the 5.56 A continuous supply rating as a conservative shared-feed check; transient current is higher and local capacitors carry switching pulses | DC resistance does not justify 19. Eight spread vias would add only about 0.045 mΩ and 1.4 mW at 5.56 A, against 0.019 mΩ and 0.6 mW for 19. This field forms an approximately 4 mm opening in the inner GND fill near U3; favour about 8–12 distributed connections if more ground-plane width is needed. Keep the same-side ceramic-to-pin loops intact. |
| Local U3 `GND` | 40, bottom to Inner 2 | The DC return is of order the 36 V input current, but the local ceramic commutation and heat flow are distributed and cannot be assigned to individual vias from this XML | Keep the distributed group for now. Its value is low-inductance local return and thermal spreading as well as DC conductance. Do not reduce it merely by dividing 5.56 A by 40; inspect actual GND and 36 V fill continuity when routing is complete. |
| Output-network `GND` | 11 near C19/C28; 12 each near R20/R21 | Not the 6.12 A speaker path. The 1 nF shunts carry small current; even an exaggerated 18 V RMS carrier across one gives `2πfCV ≈ 0.068 A` at 600 kHz. A 10 nF/3.3 Ω branch would carry about 0.67 A RMS with the same exaggerated 18 V carrier, before LC attenuation. | Barrel count is generous. The R20/R21 fields may also spread resistor heat; keep unless their clearance openings cause a meaningful 36 V neck. The central 11-via field is the easier reduction candidate if its opening becomes troublesome. Actual residual-carrier and ringing currents remain unmeasured. |

The saved Inner 1 `36V` and Inner 2 `GND` fills still route around the
`SPK+` fields; local scan lines show openings of roughly 1.6 mm through
the two-column parts and up to about 4.5 mm through the broad rows, but do
not prove a complete plane severance. The 19-via `36V` field likewise opens
roughly 4 mm of the inner GND fill in one cross-section. The layout choice
is to preserve local return geometry and copper width first, then leave
surplus vias where they do no harm. Final connectivity/DRC and filled-plane
inspection are still required once C20/C26 and the remaining routes are in
place.

[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[JLCPCB PCB capabilities](https://jlcpcb.com/capabilities/pcb-).

**Subsequent saved layout state:** the later PCB snapshot analysed in §1.1.4
has 220 placed vias. The two `SPK+` fields have been reduced to 17 each;
the local 19-via `36V` and 40-via U3 `GND` fields remain in the same places.
The 40-per-field `SPK+` figures and associated advice in the table above
describe the earlier saved snapshot, not this later count. Other added vias
are outside the local C21/C22/C24/C25-to-U3 paths.

#### 1.1.4 Local PVDD ceramic copper-parasitic estimate, 17 October 2026

**Read-only, provisional calculation** from the saved
`diptrace/main_board.dipxml` (SHA-256
`08570142D36572376F033A51A17DDBA5EB13527BC557627AFEE8E53D1D097699`).
The root is `DipTrace-PCB` 5.3.5.1 in millimetres. The embedded footprint
geometry, placed pad nets and stored bottom copper fills put all four selected
Würth C21/C22/C24/C25 2.2 µF capacitors on the same side as U3's PVDD and
GND pins. Each capacitor has direct copper-pour connections to both pin
groups; no through-via is in this shortest capacitor-to-pin path. The saved
fills are evidence of geometry, not a connectivity/DRC result.

| Capacitors | 36 V pad centre to PVDD pins | GND pad centre to relevant GND pins | Approximate pad-edge copper gap per leg |
| --- | ---: | ---: | ---: |
| Nearer C22 (AB), C24 (CD) | 2.4–2.5 mm | about 2.5 mm | about 0.9–1.0 mm |
| Farther C21 (AB), C25 (CD) | about 5.0 mm | about 5.0 mm | about 3.4 mm |

The capacitor rail and ground pad rows are separated by about 2.8 mm.
The rail pour is broad over most of each path but narrows to roughly 1.6 mm
beside the U3 PVDD pins; the corresponding ground pours remain roughly
1.2–2 mm wide in their useful corridors. The shortest return can flow on
the bottom ground pour. The Inner 2 GND plane and local vias may provide
parallel return current, but there is no ground via directly at every
capacitor pad, so a plane-over-trace formula alone would understate the
complete same-side loop.

At 20 °C, 34.8 µm bottom copper has sheet resistance
`R_sheet = ρ/t = 1.724×10⁻⁸/34.8×10⁻⁶ ≈ 0.495 mΩ/square`.
Treating both outgoing and return legs as simple strips of effective width
1.2–2 mm gives `R_loop ≈ 2 R_sheet ℓ/w`. Using the pad-edge gaps gives
roughly 0.45–0.8 mΩ for each near capacitor and 1.7–2.8 mΩ for each far one.
To allow for pad-entry spreading, the narrow PVDD throat and non-uniform
current division, use **approximately 0.5–2 mΩ near and 1.5–4 mΩ far** as
planning ranges for the *copper connections only*. These are neither measured
resistances nor worst-case fabrication limits; hotter copper raises them.

Inductance requires the complete outgoing/return current distribution, which
the XML cannot establish uniquely. For this roughly 2.8 mm-separated,
2.5 or 5 mm-long same-side pair, a broad-strip self-inductance calculation
gives order 1 nH per near leg or 2–3 nH per far leg. Mutual coupling reduces
the loop total while pad turns and the finite return path add to it. A useful
**rough planning allowance for copper loop inductance** is **2–5 nH** at
C22/C24 and **4–9 nH** at C21/C25. These are not extracted 3D parasitics or
guaranteed bounds. In particular, they exclude capacitor ESL, solder joints,
U3 package inductance and the switching FET/output portion of the loop.
TI's trace-inductance treatment explains why physical loop area and return
proximity matter more than DC resistance alone.

For a scale check, the selected capacitor's previously modelled typical
capacitance is about 1.13 µF at 36 V. Its ideal magnitude at 600 kHz is
`1/(2πfC) ≈ 0.235 Ω`. The estimated copper inductance contributes only
`2πfL ≈ 0.008–0.019 Ω` for a near part or 0.015–0.034 Ω for a far part at
that frequency. This supports the current placement as **unlikely to be
limited by copper resistance or 600 kHz fundamental-frequency inductance**.
At several megahertz, however, the inductive term rises and may dominate
after the capacitor resonates; the exact Würth part has no specified ESL or
installed impedance curve in its data sheet. Treat the nearer part as the
primary fast bypass in each bank, with the farther part providing additional
capacitance. A small model for each branch is
`Z ≈ (ESR_cap + R_copper) + j[2πf(ESL_cap + L_copper) − 1/(2πf C_effective)]`,
with the two branches sharing some copper near U3 rather than being perfectly
independent. This calculation does not assure switching-edge overshoot or
finished-board behaviour. Retain the placements unless final copper changes
introduce a neck or via detour; use the existing prototype rail-waveform and
thermal checks to resolve the remaining uncertainty.

**Interpreting the resonance number.** Four nominal 1.13 µF biased capacitors
sum to 4.52 µF only for a sufficiently common electrical node. The 9 nH
above is an allowance for *one farther capacitor's individual copper loop*,
not a 9 nH inductor in series with all four capacitors. Combining 4.52 µF
with a hypothetical **shared** 9 nH yields
`1/(2π√(9 nH × 4.52 µF)) ≈ 0.79 MHz`, but that is a different circuit.
If four identical, independent 9 nH + 1.13 µF branches were instead in
parallel, their equivalent inductance would be 9/4 = 2.25 nH and their
capacitance 4.52 µF; the ideal series-resonant frequency would stay at
about 1.58 MHz. The nearer branches have lower estimated copper inductance
and the two U3 PVDD groups occupy different positions, so there is no one
well-defined four-capacitor series resonance from the saved geometry.
Moreover, a capacitor branch's *series* resonance is an impedance **minimum**,
limited by its resistance; it is not by itself an impedance peak. A separate
inductance shared by the supply feed and local capacitance could create a
parallel impedance peak, but its value, the capacitor ESR/ESL and the bulk
feed are not established by this copper-loop estimate. Do not infer such a
peak at 600 kHz from the 9 nH figure.

[TI power-supply-layout seminar, parasitic inductance discussion](https://www.ti.com/lit/ml/slup224/slup224.pdf);
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[Würth 885012208124 data sheet](https://www.we-online.com/components/products/datasheet/885012208124.pdf);
[TI decoupling resonance explanation](https://www.ti.com/lit/an/sloa069/sloa069.pdf).

#### 1.1.5 Four-layer output and supply review, 17 October 2026

**Current read-only snapshot:** `diptrace/main_board.dipxml`, SHA-256
`B276EA8D8CD94814C7944F0CD8F798F645BC29510993AF5243388214B66086F8`;
`DipTrace-PCB` 5.3.5.1 in millimetres. This supersedes the *layout state* in
§1.1.1 and §1.1.3, while retaining their dated reasoning. The four matched
screenshots show Top, Inner 1, Inner 2 and Bottom filled copper. No live DRC,
connectivity check, solder-mask Gerbers or assembled-board measurement was
available for this review.

The four Würth ceramics C21/C22/C24/C25 remain on U3's side. The nearer
C22/C24 rail-pad centres are now 2.24–2.34 mm from the PVDD pin-centre line;
the farther C21/C25 are 4.64 mm away. Each bank also has a direct bottom-side
ground return to its adjacent U3 GND pins. The 0.2–0.4 mm position changes
slightly shorten the earlier estimated loops; they do not justify a new
inductance figure or suggest a problem at the nominal 600 kHz carrier.

C20 and C26 (470 µF each) are now placed at `(42.09, 57.3)` and
`(42.09, 8.7)` mm, respectively. Their top pads connect through 12 vias per
terminal into the broad Inner 1 36 V and Inner 2 GND pours. The two capacitors
are roughly 24 mm either side of U3's centre, and the local bottom ceramic
bank still completes the shortest switching-current loop. The three-plane
arrangement gives the bulk charge a wide feed and a nearby return; do not
judge it by pad-to-pad distance from each 470 µF capacitor to a 2.2 µF part.
The two inner fills look continuous around the output and supply via fields
in the screenshots, but their effective necks and connectivity need the
completed fill/DRC check.

The output topology remains post-filter parallel: A/C feed L1/L3 into
`SPK+`, while B/D feed L2/L4 into `SPK-`. Each U3 output has six or eight
bottom-to-top switching-node vias. The two `SPK+` top-to-bottom fields have
17 vias each, down from 40 each in the earlier snapshot. At the illustrative
3.06 A RMS per inductor of §1.1.3, the via-barrel resistance of a 17-via
top-to-bottom field is about `2.36/17 = 0.14 mΩ`, before entry/spreading
resistance, and the six-via switching fields are about `0.39 mΩ`. This is
ample DC conductance for that design point; no further via reduction is
required merely to save barrel resistance. Keep the broad copper entering
each field and inspect the filled inner planes after any changes.

**Fabrication and fit items to resolve:**

1. C20/C26 use 6.5 × 2.5 mm *surface* solder lands. Each row of 0.45 mm
   land / 0.20 mm drill vias is just outside the long pad edge: the nominal
   copper gap is `(1.60 - 1.25 - 0.225) = 0.125 mm`. With the saved 0.05 mm
   solder-mask swell, the opening-to-via copper gap is only about 0.075 mm.
   These are not literally vias inside the solder pad, but ordinary mask
   tenting/plugging beside it needs checking in the actual Gerbers and
   fabricator review. JLCPCB lists a 0.10 mm minimum mask bridge for its
   applicable standard-colour 1 oz process and at least 0.35 mm clearance
   from a solder-mask opening for ink-plugged vias. A merged opening or
   exposed hole beside a solder land could wick solder. Six appropriately
   spaced vias would give nominal barrel resistance of about
   `0.36/6 = 0.06 mΩ` from Top to Inner 1 on 36 V, or
   `2.01/6 = 0.34 mΩ` from Top to Inner 2 on GND. Twelve would halve
   those figures; moving/reducing the rows is electrically inexpensive if
   the mask output warrants it. [JLCPCB rigid-PCB capabilities](https://jlcpcb.com/capabilities/pcb-);
   [via covering guidance](https://jlcpcb.com/help/article/pcb-via-covering).
2. C26's saved 17 mm-tall footprint/courtyard spans down to `y = 0.2 mm`
   against the `y = 0` board edge. Both bulk-capacitor courtyards come within
   0.3 mm of the 6 mm-diameter mounting-hole envelopes at `(44, 20.5)` and
   `(44, 45.5)` mm. Panasonic specifies a nominal 16.0 mm body diameter for
   `EEVFK1J471M`: a perfectly centred circular body would leave about
   0.7 mm to the lower board edge, and about 1 mm to each mounting-hole
   envelope. These are nominal drawing clearances, not an assured physical
   collision, but they leave little room for placement, washer and plate
   tolerances. Check the chosen fasteners and actual body in the mechanical
   arrangement; give them deliberate margin before freezing the board.
   [Panasonic part data](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEVFK1J471M).

The large Top switching-node pours are functional current paths to L1–L4;
their area also increases capacitive coupling into Inner 1. There is no
evidence here that they need rerouting. If an assembled prototype shows
switching noise or EMI trouble, inspect their area and return geometry before
changing the four-inductor topology.

#### 1.1.6 Bottom copper-pour priority warning, 18 October 2026

**Warning and inspected saved evidence:** DipTrace's Update All Copper Pours
warns of possible DRC clearance errors for Bottom `36V`–`AMP_OUT_B`,
`36V`–`AMP_OUT_C`, and `AMP_OUT_A`–`GND`. The read-only saved PCB snapshot is
`diptrace/main_board.dipxml`, SHA-256
`7B2FD64935D09AD24334D11734F09151DE72DE7233521E2A999AD971BB8D1E3F`;
root `DipTrace-PCB` 5.3.5.1, millimetres. This is a focused check of the
warning, not a full repeat of the preceding layout review.
A later same-day save (SHA-256
`51FBEDDE8125B49305632D9A6D8A7E62E4113FE7EC3984195FC8F13CDCDC3947`)
retained the named pour priorities and outlines;
neither snapshot establishes a current DRC pass.

The named pours are Bottom IDs 0 (`36V`), 4 (`AMP_OUT_B`), 6
(`AMP_OUT_C`), 3 (`AMP_OUT_A`) and 1 (`GND`). **All have pour priority 0.**
Their stored outline-to-outline minimum separations are about 0.20,
0.14 and 0.20 mm, respectively, for the warning's three pairs. The saved
filled contours appear separated, but their coordinates are not a substitute
for a current DipTrace DRC or fabricated Gerber clearance. The warning is
therefore a possible rule/priority conflict, not proof of a short. DipTrace's
[tutorial](https://www.diptrace.com/support/tutorials/tutorial_html/)
states that a lower priority number wins and different-net pours at the same
priority can intersect; its [PCB help](https://diptrace.com/books/help/PCBHelp.pdf)
also notes that *Use Net Clearance* does not set the clearances of neighbouring
objects.

**Proposed reversible resolution:** In Bottom view, open each pour border's
Properties → Pouring. Keep the local `36V` and `GND` pours at priority 0,
and try priority 1 for the four `AMP_OUT_A/B/C/D` Bottom switching-node
pours. Updating all pours then gives the adjacent different-net pours an
explicit order. Inspect the narrow output entries to U3 and their via fields,
the C21/C22/C24/C25-to-U3 36 V/GND connections, and the filled Inner 1/2
planes. If any useful copper disappears or narrows, reshape the local pour
borders and repeat rather than accepting a worse current path. Run
Verification → Design Rules with copper-pour checks and Verification →
Check Net Connectivity on the repoured board; review the final copper/Gerbers.
Do not reduce electrical clearances or disable the check merely to remove the
warning. The exact priority choice remains a layout trial until those checks
pass.

**User-reported result, 18 October:** The warning cleared after the proposed
priority change. The later saved XML (SHA-256
`9EFE42FA405D043F4FE39AC0DB39AE35B4D40D1764AAB171043B8E1724CF29A4`)
shows Bottom `AMP_OUT_A/B/C/D` pours at priority 1 and local Bottom `36V`
and `GND` pours at priority 0. This confirms the saved priority arrangement
and the user's observed warning result; it does not establish a DRC pass or
prove that every output and supply neck retained adequate copper.

#### 1.1.7 Power-stage copper review, 19 October 2026

**Saved evidence:** `diptrace/main_board.dipxml`, SHA-256
`CB3261210CCF36BA2C1D5AD9CF3072E0B054400B01D0324119B4BC37FF434839`,
`DipTrace-PCB` 5.3.5.1, millimetres, and the user's four same-scale screenshots
with filled Top, Inner 1, Inner 2 and Bottom layers. This is a focused
power-stage review, not a live DRC, connectivity result, Gerber inspection or
assembled thermal measurement. The rest of the PCB remains in progress.

The retained same-side U3 PVDD ceramics C21/C22/C24/C25 and short Bottom
PVDD/GND paths still provide the closest commutation loops. C20/C26 feed a
broad Inner 1 `36V` pour and Inner 2 `GND` pour through distributed vias. The
new broad Bottom GND pour adds a parallel local return without an apparent
severance of either inner pour in the screenshots. Each U3 switching output
still uses six or eight Bottom-to-Top vias into a broad Top path to L1–L4.
`SPK+` uses two 17-via transitions and a roughly 9.5 mm-wide Bottom trunk;
`SPK-` remains on a broad Top pour with a roughly 4.5 mm-wide longitudinal
section beside the SPK+ transition. The 0.4 mm Bottom `AMP_OUT` traces are
bootstrap pickoffs, not the sole inductor-current paths. These geometric
observations require confirmation against the final filled Gerbers if the
pours change again.

At 150 W into a resistive 4 Ω load, `sqrt(P/R) = 6.12 A RMS` in the speaker
pair; ideal sharing gives `3.06 A RMS` per inductor. The selected 36 V source
is rated 5.56 A continuously. Using copper resistivity
`rho = 1.724e-8 ohm m` at 20 °C and `R = (rho/t)(length/width)`, JLCPCB's
published 35 µm outer / 15.2 µm inner construction gives approximately
0.493 / 1.134 mΩ per square. The following are deliberately conservative
*strip illustrations*, not extraction of the actual non-uniform pours:

| Path illustration | Assumed length × width | Current | R at 20 °C | Drop / loss |
| --- | ---: | ---: | ---: | ---: |
| Bottom `SPK+` trunk | 25 × 9.5 mm, 35 µm | all 6.12 A RMS | 1.30 mΩ | 7.9 mV / 49 mW |
| Top `SPK-` corridor | 30 × 4.5 mm, 35 µm | all 6.12 A RMS | 3.28 mΩ | 20 mV / 123 mW |
| Inner 1 `36V` feed scale check | 40 × 5 mm, 15.2 µm | all 5.56 A | 9.07 mΩ | 50 mV / 281 mW |

The complete speaker current does not traverse either output illustration
for its full assumed length: the two parallel branches join near J5. The
actual 36 V pour is much broader over most of the route and divides current
between C20/C26 and the local ceramics. The last row therefore checks the
scale of a deliberately narrow hypothetical feed rather than the plane's
measured resistance. Copper at 80 °C would raise these resistances by about
23%; the illustrated losses would still be small and spread over broad copper.
The current via fields also have low calculated barrel losses (§1.1.3).
At the 600 kHz carrier, copper skin depth is about 85 µm, greater than either
specified foil thickness, so the simple sheet-resistance estimate remains
useful at the fundamental; faster edge harmonics and loop inductance need
separate treatment.

**Copper-weight judgement:** Standard 35 µm outer / 15.2 µm inner copper is
the preferred starting construction for this approximately 150 W / 4 Ω,
four-layer, plate-cooled board. The present visible widths do not show a
resistive or Joule-heating reason to purchase heavier copper. TI nevertheless
recommends 70 µm copper generally for the TPA3251 to improve output-power,
thermal and EMI margin. That recommendation is relevant but is not an
absolute minimum for this lower-power, four-layer implementation. Reopen the
weight only if a final filled neck is materially narrower than the
illustrations, the intended continuous load/current rises, or prototype
temperature/rail/ringing evidence calls for it. JLCPCB also specifies a
larger 0.16 mm minimum line/space for its 70 µm process, so an upgrade would
need a design-rule check. The saved DipTrace stack still names 17.4 µm on
each inner layer; JLCPCB's published `JLC04161H-7628` construction shows
15.2 µm. Use the latter for conservative resistance estimates and reconcile
the design stack with the actual order before fabrication. Via-barrel plating
is a separate specification; changing layer copper weight does not by itself
establish a thicker via barrel.

| ID | Finding | State | Next check |
| --- | --- | --- | --- |
| PA-19-1 | The nearest bulk-capacitor via-to-pad copper gap is now about 0.225 mm at both C20 and C26, up from the earlier 0.125 mm geometry. | Confirmed in saved pad/via geometry; solder-mask result unverified | Inspect the final top mask and drill/Gerber outputs for solder wicking or an inadequate mask bridge. |
| PA-19-2 | C26's 17 mm footprint/courtyard still reaches about 0.2 mm from the lower board edge; the earlier drawing inspection estimated at least 0.7 mm for the capacitor body itself. | Confirmed nominal geometry; physical fit unverified | Inspect the board outline, actual body envelope and mounting-hardware clearance with the final fabrication outputs under PR-010. Do not treat the courtyard line alone as a physical interference. |
| PA-19-3 | The four Top switching-node pour outlines cover roughly 107–141 mm² each above the 36 V inner pour. They are functional current paths, and extra area could increase switching displacement current. | Geometry confirmed; EMI/ringing effect unverified | Avoid enlarging them for copper-weight reasons; use the planned prototype waveform/EMI checks if symptoms arise. |

[TI TPA3251 data sheet, §§10.2.1.2.3 and 12](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[JLCPCB published four-layer stack-up](https://jlcpcb.com/impedance);
[JLCPCB copper-weight and minimum-line guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight).


## 2 Superseded supervisor analyses

#### 1.2.1 Superseded supervisor analyses (decision record)

The following earlier candidates and calculations are retained for provenance
only. They do not specify the current RESET circuit.

The Nisshinbo `R3160N310A-TR-FE` was evaluated as an alternative to the
TPS3842. Its SOT-23-6 package has 0.95 mm lead pitch
and it can directly sense the 36 V PVDD branch: its falling threshold is 31.0 V
nominal (30.535–31.465 V across −40 to 105 °C), with approximately 32.33 V
nominal rising release from its 4.3% typical hysteresis. Pin 5 (`TAB`) must be
connected to ground as well as pin 6. Its active-low open-drain `DOUT` requires
a pull-up to a suitable low-voltage logic source: the detector output has a
7 V absolute maximum, while the TPA3251 `RESET` input has a 4.2 V absolute
maximum. A 3.3 V pull-up through about 4.7–10 kΩ is a starting point, subject
to confirming the actual logic-rail source and power sequence. A resistor
divider from the 12 V amplifier rail is another possible logic-level source,
but must be checked against both voltage extremes and the TPA3251 RESET
input's leakage. Do not pull either pin directly up to 12 V or 15 V.

The R3160 also requires a capacitor at `CD`. Its specified 10 nF release delay
is 9–27 ms at 25 °C, and the manufacturer's *typical* timing equation is
`t = 1.8 × 10⁶ s/F × CD`. Extrapolating the 10 nF minimum would require at
least 444 nF of **effective** capacitance for 400 ms; the published timing
plot only covers 100 pF–47 nF and does not guarantee that extrapolation or the
full-temperature delay. A local supply bypass is prudent on the switching
36 V branch and is specifically recommended by Nisshinbo if a series input
resistor is used, so a capacitor-count saving is not established. Monitoring
36 V alone cannot assert RESET for a failed or collapsed 17V3 buck or either
downstream LDO while 36 V remains healthy. This was a reason to select the
second TPS3762-Q1. Neither selected monitor independently detects both
downstream LDO faults. [Nisshinbo R3160N data
sheet](https://www.nisshinbo-microdevices.co.jp/en/pdf/datasheet/r3160-ea.pdf)
and [TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).

The following calculation records the superseded 15 V-buck/two-LM2937
baseline; neither divider seed applies to the revised supply tree. The earlier
182 kΩ over 10.0 kΩ seed was rejected. Its nominal 13.44 V falling
threshold can leave only 0.84 V across a worst-high 12.6 V LM2937 output, even
before PCB distribution loss, while the regulator guarantees dropout only at
50 mA (250 mV maximum) and 500 mA (1 V maximum), not at the 120 mA project
allocation. A lower-resistance 47.0 kΩ over 2.49 kΩ, both 0.1%, was the later
calculation seed:

```text
0.700 V x (1 + 47.0 kΩ / 2.49 kΩ) = 13.91 V nominal
```

This was not a locked divider. Worst-case TPS3842 threshold,
hysteresis and SENSE-current tolerances leave only a small window between
asserting RESET before a pessimistic 1 V LM2937 dropout and reliably releasing
RESET at the STH0548S15's pessimistic minimum output. The 0 Ω default amplifier
prefilter link preserves that window; fitting its reserved 3.3 Ω option would
require this calculation and the startup/down sequence to be repeated.

Primary sources:

- [Texas Instruments TPS3842 data sheet](https://www.ti.com/lit/ds/symlink/tps3842.pdf)
- [Mouser TPS3842A011DRLR listing](https://www.mouser.co.uk/ProductDetail/Texas-Instruments/TPS3842A011DRLR)


## 3 Superseded PVDD bypass candidates

**2026-10-12 PVDD bypass review (placed choice unqualified).** The saved
schematic now places Murata `GRJ21BC72A105ME11L` 1 µF, 100 V X7S capacitors
C21/C22/C24/C25 on `CAP_0805` patterns. The earlier Würth 0805 part on a
0603 pattern was a real mismatch in a preceding schematic state; that specific
problem is superseded, not an open error in this snapshot. The nearby 470 µF
capacitors supply lower-frequency energy and do not replace short-loop PVDD
bypass. TI calls for a 1 µF ceramic at each PVDD node, close to the IC. The
placed part's nominal 1 µF and 100 V rating do not establish its effective
capacitance or impedance under 36 V bias and switching peaks. At 600 kHz,
ideal 1 µF and 0.5 µF capacitors have approximately 0.27 Ω and 0.53 Ω
reactance respectively; above self-resonance, package and layout inductance
matter increasingly. Check exact-part biased capacitance, impedance over the
switching harmonics, voltage peaks, short-loop placement and rear-plate
clearance before qualifying the placed choice. The RSP-200-36 output is
adjustable to 39.6 V and its overvoltage trip range reaches 48.6 V; the
TPA3251 PVDD pin itself has a 50 V absolute maximum including peaks, so the
capacitor's higher rating does not relax the rail-voltage limit.
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[RSP-200 data sheet](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf);
[Murata MLCC part list](https://www.murata.com/-/media/webrenewal/tool/library/common-pdf/dynamic-model/component-list-d-mlcc-2504.ashx?cvid=20250523010405000000&la=en).

**2026-10-13 DC-bias evidence and selection (open).** Murata's supplied
simulation for the placed part reports −58.3% capacitance change at 36 V DC,
25 °C and 1 V RMS AC: approximately 0.42 µF per nominal 1 µF part. This is a
modelled operating-point result, not a guaranteed minimum or impedance curve.
The TPA3251 data sheet recommends a 1 µF ceramic close to each PVDD node; its
[EVM BOM](https://www.ti.com/lit/ug/slau751/slau751.pdf) actually fits nominal
1 µF, 50 V X7R 1206 MLCCs (`GRM31MR71H105KA88L`). Thus the reference
implementation strongly indicates that TI's 1 µF is a nominal component value,
not an explicit requirement for 1 µF *after* DC bias. It does not demonstrate
that this different 0805 part at 0.42 µF has the same margin. At 600 kHz the
ideal capacitive reactance for 0.42 µF is about 0.63 Ω, versus 0.27 Ω for
1 µF; real impedance also includes ESR, ESL and the PCB loop.

Consider replacing all four with an exact, layout-compatible 2.2 µF part to
recover margin. A hypothetical 2.2 µF part with the same 58.3% loss would
provide about 0.92 µF at 36 V, but the new part's bias curve must be checked
individually. Extra local capacitance itself has no identified adverse effect
on the TPA3251; the selection gate is adequate effective capacitance and
low impedance near switching frequencies, voltage/ripple suitability, and a
short PVDD-to-ground loop within the rear-plate clearance. Do not change the
placed MPN or footprint on nominal capacitance alone.

**2026-10-13 0805 comparison (selection still open).** Murata's supplied
simulation for 2.2 µF, 100 V, 0805 X7T `GRM21BD72A225KE01L` reports a
−69.6% change at 36 V DC, 25 °C and 1 V RMS AC, and displays 0.707 µF.
Multiplying nominal 2.2 µF by the displayed percentage gives 0.669 µF;
use roughly 0.7 µF for this comparison and check the simulator's reference
value before relying on a more precise figure. Either value is a material
improvement over the placed part's approximately 0.42 µF, but remains below
1 µF in this model. The TI EVM's nominal 1 µF PVDD parts use 1206 packages.
Investigate a 1206 replacement as the next practical option, comparing exact
parts' biased capacitance and impedance at 36 V and checking the larger land
pattern, package height, short bypass loop and rear-plate clearance. Larger
package alone does not guarantee a particular effective capacitance; 1210 is
an option only if a suitable 1206 cannot meet these constraints. Retain
adequate voltage margin for PVDD peaks rather than treating a 50 V rating as
automatically interchangeable with the placed 100 V rating.

**2026-10-13 1206 candidate (not yet placed).** Würth Elektronik
`885012208124` is a 2.2 µF ±10%, 100 V X7R 1206 MLCC, not a nominal 1 µF
part. Its supplied DC-bias plot indicates approximately −48.5% at 36.2 V:
`2.2 µF × 0.515 = 1.13 µF` typical, or approximately `1.02 µF` if −10%
initial tolerance is applied to the same bias ratio. The plotted bias ratio
is not a guaranteed worst-case specification; temperature dependence (X7R
±15% over its rated range) and ageing can reduce the operating value further.
No 1 µF *effective* minimum is established by TI, so the approximately 1 µF
estimate is a useful margin comparison, not an acceptance threshold. The
manufacturer's package dimensions are 3.2 × 1.6 mm with maximum height
1.9 mm. At the proposed, still-unverified 4 mm PCB-back-to-finished-pocket
clearance, this leaves about 2.1 mm before solder height and assembly
tolerances. The CNC pocket makes vertical space a secondary concern; retain
the short supply/return loop and the continuous TPA3251 thermal land.
Qualify the candidate's switching-frequency impedance/ripple behaviour and
the final pad geometry before changing C21/C22/C24/C25 in DipTrace.
[Würth part data sheet](https://www.we-online.com/components/products/datasheet/885012208124.pdf).


## 4 Previous RESET indicator

**Superseded 25 October analysis of the former RESET-indicator circuit:**
The D4 RESET indicator has a distinct off-state margin problem. R31/R34 form
a 30 kΩ/10 kΩ divider from `12VAMP`, so released `AMP_nRESET` is nominally
`12 V × 10/(30+10) = 3.0 V`. U11's P-channel source is the internal DVDD,
nominally 3.3 V; its gate therefore sits 0.3 V below its source even when
RESET is high. At 11.5 V on the regulated 12 V rail, 1% resistor extremes
and 3.6 V DVDD, the high RESET node can be
`11.5 × 9.9/(30.3+9.9) = 2.832 V`, making `VGS ≈ −0.768 V`. The onsemi
P-channel threshold spans −0.45 to −1.0 V at the specified 250 µA test
current. This divider-only estimate omits the TPA3251 RESET input's specified
leakage, so it is not a guaranteed lower bound on the high level. The MOSFET
threshold test does not establish the drain current at this particular
gate bias, but partial turn-on and a false RESET indication while the TPA3251
remains enabled are plausible. The RESET input's specified 1.9 V high
threshold is satisfied; the concern is D4's diagnostic truth, not amplifier
reset itself. Check the released LED state across practical rail and thermal
corners, or alter the indicator bias/topology before fabrication if a reliable
RESET indication is required. Do not interpret the user's acceptance of the
small DVDD load as acceptance of a misleading indication.

**Provisional resolution options, 25 October:** The smallest circuit change
that retains a useful LED is to make D4 indicate `RESET RELEASED`: connect
the existing U11 N-channel gate directly to `AMP_nRESET`, retain its
grounded source and LED-sinking drain, and isolate the unused P-channel
(tie its gate to its source). R39 is then unnecessary because R34 already
pulls `AMP_nRESET` low. Keep R31/R34 unchanged until the full RESET-node
corner is checked: TI specifies up to 100 µA RESET input leakage, whose
direction is not stated. With the present 30 kΩ/10 kΩ divider and the
11.5 V low rail/1% resistor corner, 100 µA sinking leakage could reduce
released RESET from 2.832 V by about
`100 µA × (30.3 kΩ || 9.9 kΩ) = 0.746 V`, to 2.086 V. This remains above
TI's 1.9 V logic-high threshold, though it is below the 2.5 V N-channel
gate-drive point at which onsemi specifies on-resistance, so LED brightness
at that extreme is not yet guaranteed. Raising the divider output by
lowering R31 alone is not a complete cure: an unknown-sign leakage current
can also raise the high node towards the 4.2 V RESET absolute maximum.
The active-high option removes this indicator's DVDD load; it requires a
silkscreen/truth-table change and schematic/PCB checks after rework.
If the LED must mean `RESET ASSERTED`, use a separate first transistor
driven by `AMP_nRESET` to invert it before the existing N-channel LED sink;
derive that stage from `12VAMP` with a gate voltage within the selected
device's rating and check power-up states. This costs parts and routing.
Deleting D4 and relying on the existing RESET test pad was the least complex
diagnostic option. These were proposals for the former circuit; the direct
N-channel ACTIVE circuit above is now implemented.

**R34 = 11 kΩ candidate, 25 October:** The user's BOM-common substitution
would raise the nominal released RESET level to
`12 V × 11/(30 + 11) = 3.220 V`. It improves the nominal P-channel
`VGS` from about −0.30 to −0.08 V, but does not close SR-001. At the
11.5 V rail, R31 high by 1%, R34 low by 1%, and DVDD at 3.6 V, RESET is
`11.5 × 10.89/(30.3 + 10.89) = 3.040 V`, giving `VGS = −0.560 V` even
without RESET input leakage. That overlaps the P-channel's −0.45 to −1.0 V
threshold range at its specified 250 µA test; the threshold figure cannot
guarantee an extinguished LED at smaller drain currents. If the specified
100 µA RESET input leakage sinks current, the divider's approximately
8.01 kΩ Thevenin resistance could lower RESET by another 0.801 V to
2.239 V, making `VGS ≈ −1.361 V`. Conversely, leakage sourcing 100 µA at
the 12.5 V rail and opposite 1% resistor extremes could raise RESET from
3.403 V by `0.100 mA × 8.085 kΩ ≈ 0.809 V` to 4.212 V, marginally above
the TPA3251 RESET pin's 4.2 V absolute maximum. The data sheet does not
state the leakage direction, so these are conservative independent corners,
not a prediction that either will occur in the prototype. Retain 11 kΩ as
an evaluated candidate only; prefer a topology change if reliable indication
is needed.
