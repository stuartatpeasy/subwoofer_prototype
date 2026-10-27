# Power amplifier

> **State — current amplifier authority; reviewed 2026-10-26.** Owns the
> TPA3251 stage and RESET topology. Two 36 V-powered TPS3762-Q1 supervisors
> monitoring PVDD and `17V3` are selected. The dedicated 130 kΩ/7.5 kΩ,
> 1% E24 buck SENSE divider is selected. The now-placed L78M12 12 V regulator
> may sag briefly before the lowest calculated RESET trip; loaded buck-trough,
> return-offset and start/stop checks remain open. Würth `885012208124` PVDD
> bypass capacitors are selected. Their 36 V biased performance remains a
> model-based estimate. The current saved U3 output and supply copper has a
> promising scoped layout review: C20/C26 now feed broad 36 V and GND planes,
> while their solder-mask and mechanical clearances and prototype switching
> behaviour remain open. The 18 October Bottom-layer same-priority
> copper-pour warning cleared after the output pours were reprioritised;
> the 19 October power-stage copper review provisionally supports standard
> 35 µm outer / 15.2 µm inner copper for the 150 W into 4 Ω design point;
> the user reports that final-board DRC and net-connectivity checks pass;
> the reports were not independently inspected.
> D4 is now a green `ACTIVE` indicator driven by U11's N-channel directly
> from `AMP_nRESET`: lit when RESET is released and dark when it is asserted.
> The former false RESET-indication issue SR-001 is closed in the saved design;
> assembled brightness and polarity remain checks.
> The two-position Mini-Fit Jr speaker-output pair is selected; placement and
> finished harness routing remain open.

## 1 TPA3251 output stage

Configuration:

- PBTL
- use TI post-filter-parallel topology
- follow TI layout guidance closely

Critical layout requirements:

- very short PVDD decoupling loops
- compact bootstrap loops
- minimise switching-node area
- short high-current paths
- correct return-current routing
- keep analogue and switching grounds controlled
- on the combined PCB, face the TPA3251 input pins toward the analogue/power
  placement corridor and keep switching nodes and output inductors on the
  opposite side
- use the four-layer partition and layer intent defined in
  [Power and grounding](POWER_AND_GROUNDING.md); TI's 2-layer EVM establishes
  device feasibility, but two layers are not a project fallback

### 1.1 Rear-mounted IC and local support components

The TPA3251 faces the machined rear plate. Reliefs around its thermal land now
permit selected support components on the same PCB side as the IC. Prefer that
placement for PVDD ceramic decoupling and bootstrap capacitors when it gives
the shortest complete supply/return or BST/OUT loop. TI's PBTL layout guidance
places close ceramic bypass parts by the IC pins and calls for direct, broad
PVDD/ground connections without a via in the main current path. The exact
placement still depends on the pin map, component heights and plate reliefs.

Layout requirements:

- keep each local PVDD-to-GND decoupling loop compact and use broad same-side
  copper where practical; use local paired/parallel vias only where a layer
  transition is actually required;
- keep each complete BST-to-capacitor-to-OUT loop extremely small;
- keep AVDD, DVDD, GVDD, VBG, VDD, C_START, and other local bypass loops short;
- preserve symmetry through the via transitions for the differential input;
  and
- determine any high-current via drill, plating, count, and geometry from both
  current capacity and high-frequency inductance; do not size from DC ampacity
  alone.

The former mandatory opposite-side capacitor/via arrangement is superseded.
Use the layout review to choose which remaining components belong on each side.

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

### 1.2 Protection, fault response, and RESET control

Use the TPA3251's internal undervoltage, overcurrent, short-circuit, and thermal
protection. Supply undervoltage may recover automatically. A persistent
overload or overtemperature shutdown may remain latched until the user switches
the complete subwoofer off and on. Do not add an automatic fault-retry circuit.
The partial schematic draws `R18 = 22 kΩ` from `OC_ADJ` to GND, matching the
[TI PBTL reference circuit](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).
TI's protection table assigns 22 kΩ to cycle-by-cycle current control (CB3C)
and lists a 16.3 A OC threshold; its electrical-characteristics table separately
lists 14 A nominal peak current for a 1 Ω test load at 22 kΩ. These are
different published descriptions, not a guaranteed 16.3 A trip point in this
board. The IC senses individual half-bridge FET current. At 150 W into a
nominal 4 Ω resistive load, the speaker current is
`sqrt(2 × 150 W / 4 Ω) = 8.66 A peak`; ideal sharing gives about 4.33 A peak
through each of the two parallel output paths on either bridge side. Real
speaker impedance, filter ripple, sharing error, and faults change those
currents. The 22 kΩ value therefore follows TI's starting example but is not
yet proven to protect this driver's voice coil or the output inductors. The
[Vishay inductor data sheet](https://www.vishay.com/docs/34337/ihlp5050fd-5a.pdf)
lists 7.8 A typical DC current for an approximately 20% inductance drop in the
10 µH part. That criterion is not a destructive limit, but it is below even
TI's 12.3 A table threshold at 30 kΩ; IC overcurrent protection cannot be
treated as an inductor saturation guard. CB3C
can limit individual overcurrent cycles and later latch off after persistent
overload; it is not a continuous output-power limiter. Retain R18 provisionally
while checking the chosen inductor's current limits and the 22–30 kΩ CB3C
options against the finished output stage. The
[TPA3251EVM guide](https://www.ti.com/lit/ug/slau751/slau751.pdf) lists
24, 27, and 30 kΩ as progressively lower nominal CB3C thresholds.

The former test-point-only indicator plan is superseded: the current saved
schematic and PCB have board-level diagnostic LEDs D2 (red, `FAULT`), D3
(orange, `CLIP_OTW`) and D4 (green, `ACTIVE`). No front-panel indicator is
required. The current board also has Top-side TP9/TP10/TP11 on
`AMP_nRESET`/`AMP_nFAULT`/`AMP_nCLIP_OTW`, with local rail and ground pads;
see the [current PCB review](PCB_LAYOUT.md#1-reviewed-design-state-and-scope).
The LEDs do not themselves qualify short-pulse diagnostics.
Each active-low FAULT and CLIP_OTW output drives the gate of a P-channel half of an onsemi
`NTJD4105CT2G` complementary pair (U4/U10). Its source is on `AMP_DVDD`; its
drain drives the paired N-channel gate and a 130 kΩ pull-down to GND. When the
status pin falls, the P-channel turns on, raising the N-channel gate and
sinking LED current from `12VAMP` through a 1.5 kΩ resistor. Saved net and
symbol numbering matches onsemi's S1/G1/D1 = 1/2/6 and S2/G2/D2 = 4/5/3;
the selected six-pad pattern has 0.65 mm pitch. The chosen Kingbright LED
symbols put anode on pad 1 and cathode on pad 2; confirm the actual package
polarity mark and land geometry before assembly. The earlier 18 October PCB
did not yet contain those indicators; the current saved PCB does.

**26 October ACTIVE revision:** D4 is Kingbright green
`APHCM2012CGCK-F01`. R40 connects `12VAMP` to its anode (pad 1); its cathode
(pad 2) connects to U11's N-channel drain (pad 6). U11's N-channel source
(pad 1) is at GND and gate (pad 2) is directly on `AMP_nRESET`. The unused
P-channel's source, gate and drain (pads 4, 5 and 3) are all at GND. R39 has
been removed. These nets and physical pad numbers agree in the saved
schematic and PCB, and Top silkscreen reads `ACTIVE`. RESET released turns on
the sink and lights D4; RESET asserted leaves it dark. `ACTIVE` reports RESET
release, not proof of fault-free operation or amplifier output. Confirm the
actual LED polarity mark, land dimensions and visible brightness on assembly.

The earlier 1 kΩ/100 mW selection exceeded its continuous rating at a
plausible high regulated rail, so the user selected 1.5 kΩ in R36/R37/R40. The
placed part is TE `CRGCQ0603F1K5`, 0603, 1%, 100 mW; its manufacturer and
Mouser part fields match the published identity. At a nominal 12 V rail and
illustrative 2 V LED drop, each branch draws `(12 − 2) / 1.5 kΩ ≈ 6.67 mA`
and the resistor dissipates `(12 − 2)^2 / 1.5 kΩ ≈ 66.7 mW`. The L78M12A's
specified regulated upper output is 12.5 V over its stated load/input range.
With an illustrative 1.8 V LED drop and a 1%-low 1.485 kΩ resistor, the
current is about 7.2 mA and dissipation is
`(12.5 − 1.8)^2 / 1.485 kΩ ≈ 77.2 mW`. This is a useful design corner, not a
formal absolute maximum: the Kingbright sheets specify typical LED forward
voltages at 20 mA, with no guaranteed minimum at this roughly 7 mA current.
Lower forward voltage or rail overshoot increases the resistor's power. TE
rates the resistor at 100 mW through 70 °C ambient and requires derating
above that temperature. The selection is reasonable if the local resistor
ambient stays within the un-derated range; check the eventual hot local
temperature if an indicator may remain continuously lit during a fault. The Kingbright
parts' intensity specifications are given at 20 mA, so actual board-level
visibility at 6–7 mA remains to be checked. The 26 October saved schematic
and PCB agree on the corrected R2/R10 `Mfr part` `CRGCQ0603F1K0` and Mouser
SKU `279-CRGCQ0603F1K0`. They also agree on Yageo `Mfr part`
`RC0603FR-0710KL` and Mouser SKU `603-RC0603FR-0710KL` for all five 10 kΩ
parts R19/R27/R30/R33/R34. The former purchasing-identity mismatches are
closed; these metadata edits did not change their electrical values.
The MOSFET ratings have ample voltage and current margin in the drawn circuit:
N-channel `VDS` is at most approximately the 12 V rail versus 20 V rating;
P-channel `VDS` and both `VGS` values remain within the roughly 3.3 V DVDD
domain versus the P-channel's 8 V limits. Both channels' guaranteed
`RDS(on)` points at 2.5 V gate drive are adequate for these small currents.

Each of the D2/D3 asserted branches adds up to
`3.6 V / 130 kΩ ≈ 0.028 mA` of external DVDD draw at nominal resistance.
With both status outputs low, their pull-down load is about 0.055 mA; the
two built-in pull-ups can each draw up to `3.6 V / 20 kΩ = 0.180 mA`, giving
approximately 0.415 mA total DVDD-sourced status-circuit current. The new
U11/D4 ACTIVE branch has no external static DVDD connection; the user's
earlier risk acceptance of the additional RESET-branch DVDD load is no longer
needed for this circuit. D4's approximately 6–7 mA LED current is sourced
from `12VAMP` and adds roughly 35 mW to U9's pass loss at the nominal
17.36 V input, subject to the actual LED voltage and load.
The selected 130 kΩ value supersedes both the original 47 kΩ and the examined
180 kΩ candidate. At the specified 25 °C P-channel off-leakage test value of
1 µA, it would develop 0.13 V versus 0.18 V for 180 kΩ. The built-in
20–32 kΩ pull-up range changes the two asserted-pin currents at 3.6 V by
0.135 mA; this is larger than the additional 0.055 mA through both 130 kΩ
pull-downs. That comparison describes current scale, but does not qualify
external loading of the DVDD reference node.
When the P-channel is off, its specified 1 µA maximum drain leakage at 25 °C
and −6.4 V test bias corresponds to 0.13 V across 130 kΩ, if applied as a
conservative estimate at the actual approximately −3.3 V bias. The N-channel
threshold is at least 0.6 V at 25 °C under its specified 250 µA test, but that
threshold is not a guaranteed zero-current boundary. The P-channel leakage
limit is not given over operating temperature, so false illumination at the
hot corner is not formally excluded by these data. The N-channel's specified
46 pF maximum input capacitance at its 20 V test point gives an illustrative
`130 kΩ × 46 pF ≈ 6 µs` discharge constant; actual capacitance and PCB
coupling can differ. For diagnostic LEDs the selected value appears reasonable,
subject to checking that D2/D3 remain dark in the inactive state on the
assembled board, including when warm.
TI nevertheless says DVDD/AVDD are not external supplies, and gives no
guaranteed external-load allowance. Treat this small draw as an explicit
design deviation pending measurement of DVDD under asserted conditions, not
as a data-sheet-qualified feature. Do not confuse the approximately 7 mA LED
current, which comes from `12VAMP`, with the DVDD load. Also, TI forces
`FAULT` high while RESET is low; D2 therefore cannot show a supervisor-held
reset or every protection event. D3 combines clipping and overtemperature
warning, and brief assertions may be too short for the eye without a latch.

**SR-001 — Medium, closed in saved schematic and PCB on 26 October:** The
original P-channel RESET LED could light while RESET was released. The saved
ACTIVE revision uses the N-channel connection described above, so a high
`AMP_nRESET` lights D4 and a low one extinguishes it. R31/R34 remain
30 kΩ/10 kΩ. At the 11.5 V rail, opposing 1% divider tolerances and a
conservative 100 µA sinking RESET-pin leakage give approximately 2.086 V at
the released node, above the TPA3251's 1.9 V high threshold. LED brightness
at that extreme is not guaranteed by the transistor's 2.5 V on-resistance
specification; check it on the prototype. Physical LED polarity and changed-
board DRC/connectivity remain separate fabrication checks.

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
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[NTJD4105C data sheet](https://www.onsemi.com/pdf/datasheet/ntjd4105c-d.pdf);
[red LED](https://www.kingbrightusa.com/images/catalog/spec/aphcm2012surck-f01.pdf);
[orange LED](https://www.kingbrightusa.com/images/catalog/spec/aphcm2012seck-f01.pdf);
[green LED](https://www.kingbrightusa.com/images/catalog/spec/aphcm2012cgck-f01.pdf);
[TE CRGCQ resistor](https://www.te.com/en/product-2-2176339-5.html);
[ST L78M regulator](https://www.st.com/resource/en/datasheet/l78m.pdf).

The selected analogue RESET topology uses two 36 V-powered Texas Instruments
`TPS3762-Q1` undervoltage supervisors. The fixed-30 V
`TPS3762EUVF4DDFRQ1` senses the local TPA3251 PVDD branch directly. The
adjustable-0.8 V `TPS3762EUV02DDFRQ1` senses the approximately 17.36 V buck
output through a divider, preferably at the amplifier-side `17V3` feed to
the 12 V LDO so no additional signal need cross the PCB partition. Each
active-low open-drain RESET output connects to the same TPA3251 `RESET` node:
either fault holds it low, and release requires both rails to recover. Both
parts use the 0.65 mm-pitch SOT-23-thin-8 package. No separate 3.3 V supply,
logic gate, 12 V supervisor, MCU, or automatic fault retry is selected.

Fit at least 0.1 µF of effective local VDD bypass capacitance at each device.
Tie each BIST_EN pin low; leave BIST and fixed-delay CTS pins unconnected.
Fit a separate timing capacitor from each CTR pin to its local ground. C0G is
not required by this circuit: TI limits CTR to 5.5 V in operation, so a 50 V
X7R is electrically suitable if its **minimum effective capacitance** after
initial tolerance, temperature, DC bias and ageing remains at least
`0.400 s / 2.96 MΩ = 135 nF`. A nominal 220 nF, ±10% X7R loses at most 10%
initially and 15% over the X7R temperature range, leaving `220 nF × 0.90 ×
0.85 = 168 nF` before bias and ageing. The placed KEMET base part
`C0805C224K5RAC` has the same nominal 220 nF, ±10%, 50 V X7R specification
as the cited `C0805C224K5RACTU` packaging variant. The latter part's data
show a small typical DC-bias change at the CTR pin's
at-most-5.5 V operating voltage and specify 3% ageing loss per decade-hour,
with capacitance tolerance referred to 1,000 hours after the last heating
above the ceramic's Curie point. Ten years after that event is about 1.94
decades beyond the reference, or approximately 5.8% further ageing loss. For
illustration, allowing 5% bias loss as well as the full 15% X7R temperature
change and the initial 10% tolerance gives `220 nF × 0.90 × 0.85 × 0.95 ×
0.942 ≈ 151 nF`, corresponding to approximately 446 ms at TI's minimum
2.96 MΩ timing resistance. The bias plot is typical, not a guaranteed
part-by-part bound, so this is a credible design margin rather than a formal
400 ms guarantee. Retain the placed 220 nF parts and check RESET release
timing on the prototype; consider 330 nF only if that check fails or more
margin becomes necessary. At nominal values, 330 nF would lengthen the
delay to about 1.22 s instead of 0.81 s. A single, provisional 30 kΩ/10 kΩ,
1%-resistor divider from the existing 12 V amplifier rail supplies the shared
RESET pull-up, subject to confirmation of the finished 12 V rail limits and
ground offsets. The 12 V rail supplies a logic level, not a precision sense
threshold. Do not load the TPA3251 DVDD reference as an external supply.

The selected dedicated buck SENSE divider is **130 kΩ** from `17V3` to
SENSE and **7.5 kΩ** from SENSE to the supervisor's local ground. Both are E24,
1% resistors with TCR no worse than 100 ppm/°C. The purpose is to detect a
falling buck rail and assert RESET while the 12 V amplifier supply is still
usable, while allowing some droop of the 15 V analogue rail during a buck
fault. With the now-placed L78M12, a brief 12 V sag before RESET assertion
remains possible at the lowest threshold. The
15 V rail is not itself monitored. With a nominal 0.8 V falling SENSE threshold,

```text
VBUCK,fall = 0.8 V × (1 + 130 kΩ / 7.5 kΩ) = 14.667 V nominal.
```

Using TI's ±0.9% threshold accuracy, ±200 nA as a conservative SENSE-current
bound, independent resistor initial tolerances and worst-opposed 100 ppm/°C
drift over 100 °C from 25 °C, the rail trip is calculated from
`VBUCK,fall = VITN × (1 + Rtop/Rbottom) + ISENSE × Rtop` (positive ISENSE into
the pin). Each resistor's combined worst-case initial and temperature change
is 1% + 100 °C × 100 ppm/°C = 2%. Opposed resistor extremes give a calculated
falling threshold of about **13.97–15.40 V**. With maximum 2.5% hysteresis,
the highest rising release is about **15.78 V**. The calculated lowest healthy
buck output is 16.78 V, so the rising threshold leaves about **1.00 V** for
buck ripple, transients, and sense/return offsets. ST specifies the placed
L78M12A's 12 V output over 5–350 mA with VIN from **14.5 to 27 V**. The lowest
calculated falling threshold is therefore **0.53 V below** its specified
minimum input. Brief 12 V sag before RESET assertion cannot be excluded, even
without buck ripple or feed drop. The 2 V dropout figure is typical at 25 °C,
not a guaranteed limit at this board's load and temperature. The
analogue 15 V LDO may already be out of regulation when RESET asserts; no
pre-dropout mute is claimed for that branch. At a fully specified 3 V RMS
input, the OPA167x first-buffer common-mode margin disappears if its supply
falls below approximately 12.5 V; smaller programme signals need less
headroom (see [analogue front end](FRONT_END.md)). Implement the chosen
divider at the amplifier-side `17V3` feed; confirm loaded buck trough,
amplifier-feed and return drops, and start/stop behaviour. RESET-before-any-
12 V-sag is not a design claim.

The current partial schematic's MP4541GN feedback divider (`R24 = 180 kΩ`,
`R28 = 11 kΩ`) is not a substitute for this separate SENSE divider. Its FB
node is regulated near 1.0 V; the TPS3762's 0.8 V falling threshold would
represent only `0.8 V × (1 + 180/11) = 13.89 V` nominal at the buck output.
With the same conservative ±0.9% TPS threshold, ±200 nA SENSE current, 1%
resistor initial tolerance and opposed 100 ppm/°C drift over 100 °C used
above, its calculated minimum trip falls to about 13.22 V, below the
L78M12's 14.5 V specified input minimum even before ripple or feed losses.
If the extra SENSE current were 200 nA, the static shift in the buck's regulated
output would be about `200 nA × 180 kΩ = 36 mV`: small, but not zero. The
added SENSE input and long branch would also expose the buck's
feedback node to coupling and capacitance; MPS calls for the feedback
resistors beside FB and away from SW. Sensing the `17V3` feed near the
amplifier LDO also covers a drop in that feed which the buck-local FB node
cannot see. Retain the separate divider.

The intended verification is RESET low for at least 400 ms after PVDD
application or either detected fault, prompt assertion on each monitored
rail's decay, and acceptable post-filter loudspeaker transients on normal
start-up, shutdown, and rapid off/on. The two monitors do not independently
detect failure of either downstream LDO while both monitored rails stay
healthy; the TPA3251 retains its internal supply protection.

Primary sources: [TI TPS3762-Q1 data sheet](https://www.ti.com/lit/ds/symlink/tps3762-q1.pdf),
[KEMET C0805C224K5RACTU specification](https://search.kemet.com/download/specsheet/C0805C224K5RACTU),
[KEMET X7R series test methods](https://content.kemet.com/datasheets/KEM_C1002_X7R_SMD.pdf),
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf), and
[Torex XC6701 data sheet](https://product.torexsemi.com/system/files/series/xc6701.pdf),
and [ST L78M data sheet](https://www.st.com/resource/en/datasheet/l78m.pdf).

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

The [TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf)
states that its DC-speaker protection is disabled in PBTL mode. Rev A will not
add an external differential-DC detector, speaker relay, series output MOSFETs,
or switched-PVDD protection. This deliberately accepts the residual risk that
a rare amplifier-output failure could damage the internally connected driver.
The decision is proportionate to the fixed internal speaker wiring: there are
no user-accessible speaker terminals, and the cable and sealed feed-through
must remain insulated, supported, and protected from abrasion and earthed
metalwork. `RESET` control is thump suppression and functional shutdown; it is
not claimed as independent protection against a physically shorted output
transistor.

### 1.3 Speaker-output connection

Selected board-to-driver pair (2026-10-12): Molex Mini-Fit Jr `39-28-1023`
two-position, vertical through-hole, tin-plated PCB header and `215326-1023`
two-position female-to-pigtail assembly. The assembly has two factory-terminated
16 AWG (approximately 1.31 mm²), **600 mm** conductors; its housing and
contacts are supplied as part of the assembly, so no separate pins or crimp
tool are required. Connect the two positions to the filtered PBTL speaker
outputs, not to chassis or `GND`. The selected parts have a positive latch and
are distinct in position count from the six-position 36 V input connector.

At the approximately 150 W into 4 Ω output target, speaker current is
`sqrt(150 W / 4 Ω) = 6.12 A RMS`. Molex's two-position, 16 AWG brass-contact
guideline is 9 A per contact, subject to PCB copper, ambient temperature, and
the completed cable termination. Confirm the 600 mm route, pin numbering,
header footprint and clearance, strain support, polarity, and the driver-end
termination during layout and assembly. Recheck Mouser UK availability,
normal-stock status, MOQ, and price before ordering.

Manufacturer sources: [Mini-Fit Jr product specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/555/5556/PS-5556-001-001.pdf),
[header](https://www.molex.com/en-us/products/part-detail/39281023), and
[600 mm pigtail series](https://www.molex.com/en-us/products/series-chart/215326).

## 2 Output inductors

Locked part:

- Vishay-Dale `IHLP5050FDER100M5A`
- 10 µH
- four required

Reasons:

- low DCR
- ample current margin
- acceptable bias behaviour
- published L/Q vs frequency
- provisionally suitable for the specified nominal 600 kHz operation; confirm
  loss and temperature in the assembled amplifier

Prototype validation required:

- idle temperature
- sustained-load temperature
- contribution to idle PVDD current

## 3 Output capacitors

> **State:** First-prototype capacitor selection, reviewed 2026-10-26. Owns the
> output-filter capacitor choice. The 10 µH inductors are locked in Section 2.
> The canonical schematic now draws two TDK `B32701P4684K000` film capacitors,
> one on each combined speaker-output side. Next gate: check response/damping,
> carrier ripple and capacitor temperature in the prototype. The TDK series has
> a published 600 kHz current allowance.

The [TPA3251 data sheet's differential PBTL example](https://www.ti.com/lit/ds/symlink/tpa3251.pdf)
draws four 10 µH inductors but only **two** 680 nF post-filter shunts: one
on each combined speaker-output side. Its accompanying design-requirements
table describes the filter as 10 µH + 1 µF, so the figure and table should
be treated as example values rather than an exact capacitor mandate. The
[TPA3251 EVM](https://www.ti.com/lit/ug/slau751/slau751.pdf) instead has four
680 nF positions and 7 µH inductors; that different LC implementation was the
source of the previous four-position assumption.

In the current XML, L1 and L3 join at `SPK+`, while L2 and L4 join at `SPK-`.
C17 and C30 each provide one 680 nF shunt to GND. Each same-side pair of
10 µH inductors is ideally 5 µH in parallel, giving the simple LC scale
`f0 = 1/(2π√(5 µH × 680 nF)) ≈ 86 kHz`. This is not a measured loaded
response; speaker impedance, filter loss, layout, and the Zobel network alter
damping. The earlier 12 × 220 nF MLCC arrangement, with six shunts per side,
was superseded by the two film parts; its idealised scale was about 62 kHz.

**Capacitance trade-off (idealised):** for differential operation into a
purely resistive 4 Ω speaker, symmetry lets each combined output side be
modelled with 5 µH series inductance, its shunt capacitor, and 2 Ω to a
virtual ground. The low-pass denominator is
`1 + sL/R + s²LC`, so `f0 = 1/(2π√(LC))` and `Q = R√(C/L)`.

| Capacitance per side | Implementation example | Ideal f0 | Ideal Q | Additional ideal attenuation at 600 kHz versus 680 nF |
| --- | --- | ---: | ---: | ---: |
| 680 nF | one 680 nF | 86 kHz | 0.74 | reference |
| 1.0 µF | one 1.0 µF | 71 kHz | 0.89 | about 3 dB |
| 1.36 µF | two 680 nF in parallel | 61 kHz | 1.04 | about 6 dB |
| 2.04 µF | three 680 nF in parallel | 50 kHz | 1.28 | about 9.5 dB |

The 680 nF value gives Q close to the 0.707 Butterworth value in this simple
4 Ω model. Larger capacitance reduces carrier voltage ripple, but raises Q
and can increase response peaking around the lowered LC frequency. The real
speaker is not a 4 Ω resistor at tens of kilohertz, and the Zobel and loss
change the result; this table is a sensitivity calculation, not a predicted
measured response. At 100 Hz and 150 W into 4 Ω, each side carries only about
5 mA RMS of audio-frequency current in a 680 nF shunt (about 10 mA for
1.36 µF), so extra capacitance offers little benefit within the intended
subwoofer passband. At the carrier, inductor ripple is set mainly by rail
voltage, inductance and switching period; extra capacitance chiefly lowers
the shunt voltage ripple. Paralleling identical parts shares that ripple
current, but the selected single TDK part already has substantial published
current allowance. Retain one 680 nF per side as the prototype baseline;
increase capacitance only if measured residual carrier or response warrants
the accompanying damping and layout review. TI's PBTL figure uses 680 nF,
while its accompanying table gives 1 µF as another example.

**Drawn provisional prototype choice:** two TDK `B32701P4684K000`
metallised-polypropylene through-hole capacitors, C17 from `SPK+` to GND and
C30 from `SPK-` to GND. Each is 680 nF ±10%, 450 V DC, with a 13 × 6 × 12 mm
maximum body and 10 mm lead pitch (0.6 mm leads). The alternative TDK
`B32702P4684K000` has the same capacitance and voltage, a 18 × 5 × 10.5 mm
body and 15 mm pitch (0.8 mm leads). The smaller-pitch part occupies about
78 mm² of body plan area versus 90 mm² for the 15 mm version, but is 1.5 mm
taller; verify actual plate clearance. Both have a clear manufacturer drawing,
unlike the conflicting distributor pitch for the earlier Panasonic candidate.
The two-capacitor arrangement follows the data-sheet PBTL figure and avoids
the MLCC bank's uncertain DC-bias capacitance. Place each close to its
inductor join with a compact ground return. The 2026-10-11 six-MLCC proposal
and subsequent Panasonic film proposal are superseded as preferred candidates;
they remain alternatives if the TDK part fails prototype checks.

At idle, each output shunt sits near half of the 36 V rail; audio and
switching ripple add to this. The 450 V DC rating has ample nominal margin,
subject to measured overshoot. For a first-order carrier
current estimate, each 10 µH inductor sees about 18 V for half a 600 kHz
period: `ΔI ≈ 18 V / (2 × 600 kHz × 10 µH) = 1.5 A` peak-to-peak. If the
two same-side PBTL currents add, the single shunt sees about 3 A peak-to-peak,
or `3/(2√3) ≈ 0.87 A RMS` for a triangular ripple at idle. This is an
idealised estimate, not a measured worst case over modulation and load.

TDK's 680 nF permissible-current curves extend to 1 MHz, unlike Panasonic's
published ECWFD plot, which stops around 250 kHz and omits the exact
15 mm-pitch 680 nF variant. Reading TDK's **sinusoidal** curves at 600 kHz
gives approximately 3 A RMS for `B32701P4684K000` and 2.5 A RMS for
`B32702P4684K000` at ambient temperature at most 85 °C and no more than
15 °C self-heating. The 10 mm part thus has both the smaller plan area and
the higher published current allowance. These curves are stronger selection
evidence than either part's isolated-pulse dV/dt limit (60 V/µs and
25 V/µs respectively), but a PWM waveform has harmonics and its actual
current changes with modulation and load. Verify the waveform, capacitor case
temperature at representative maximum output, residual carrier and loaded
filter response on the prototype. At the final PCB stage, confirm lead pitch,
orientation, clearance and mechanically secure mounting. The nominal 450 V
rating alone is not the approval criterion.

Sources: [TDK B3270*P data sheet](https://www.tdk-electronics.tdk.com/inf/20/20/ds/mkp_b32701p_b32703p.pdf),
[TDK B32701P4684K000 product page](https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32701P4684K000),
[TDK B32702P4684K000 product page](https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32702P4684K000),
[Panasonic ECWFD technical data](https://industrial.panasonic.com/cdbs/www-data/pdf/RDI0000/ABD0000COS113.pdf),
[TI TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf), and
[TI LC filter design guidance](https://www.ti.com/lit/an/slaa701a/slaa701a.pdf).

## 4 Zobel/output damping network

**2026-10-12 output-small-capacitor rating review (historical analysis;
selection updated 2026-10-26).** C19/C28 are 1 nF directly from the two post-inductor
speaker-output nodes to GND. C16/C31 are 10 nF in series with R20/R21
(3.3 Ω) from those same nodes to GND. Each capacitor therefore sees its
own output-to-ground voltage, not the full differential speaker voltage.
In an ideal symmetrical 36 V PBTL stage delivering 144 W into 4 Ω, the
differential 24 V RMS output corresponds to about 12 V RMS per side around
an 18 V midpoint: roughly 1–35 V per node. Add switching ripple and any
LC/output-wiring overshoot to that estimate; the actual peak is unverified.
Thus the formerly drawn 250 V ratings were not required by the nominal waveform.
100 V ceramic parts provide substantial
nominal margin, subject to the final voltage waveform, dielectric/impedance,
and capacitor and resistor temperature. A 50 V 10 nF X7R/3.3 Ω pair is used
in TI's output-network guidance, but choosing 100 V here leaves more room
for post-filter ringing. The TPA3251's 50 V output-pin absolute maximum
does not itself bound overshoot at the post-inductor nodes. The earlier option
to retain 250 V parts was superseded by the saved 100 V selection. The 1 nF
parts are small high-frequency shunts:
at 600 kHz their ideal reactance is about 265 Ω versus 0.39 Ω for the
680 nF film shunts. The 10 nF/3.3 Ω branch starts to become resistive near
4.8 MHz, making its high-frequency damping and heating more important than
the nominal voltage rating alone.
[TPA3251 data sheet](https://www.ti.com/lit/ds/symlink/tpa3251.pdf);
[TI output-network guidance](https://e2e.ti.com/support/audio-group/audio/f/audio-forum/492175/question-about-tpa3251d2-diodes-at-output).

**First-prototype saved selection, 26 October 2026:** C19/C28 use Würth
`885012207116` 1 nF, 100 V; C16/C31 use Würth `885012207122` 10 nF,
100 V. R20/R21 use Yageo `RC2512FK-7W3R3L` 3.3 Ω, 2.2 W, 2512.
The nominal voltage argument supports trying these values; it does not
establish the actual overshoot, high-frequency damping or heat dissipation.

Prototype validation:

- temperature at idle
- temperature under sustained high output

## 5 General amplifier-board passives

### 5.1 Resistors

Default:

- SMD preferred; allow through-hole with justified layout and plate clearance
- 1%
- choose the package and power rating for the actual voltage, dissipation,
  assembly method, and placement; 0603 is suitable for the low-level input
  resistors R16/R17

Exceptions:

- precision signal networks
- Zobel/power resistors

### 5.2 Ceramics

Use voltage rating appropriate to node.

Guideline:

- 12 V rails: 16–25 V X7R
- bootstrap: 50–100 V
- PVDD bypass: 50–63 V minimum; 100 V is acceptable when the chosen part
  retains sufficient capacitance and low impedance under 36 V bias
- output filter: provisional 680 nF TDK metallised-polypropylene film
  shunt per combined speaker side; see Section 3 for qualification
- use C0G/NP0 for small precision/HF values where appropriate

Do not blindly use 100 V parts everywhere.

**Selected choice, confirmed by the user 2026-10-17; operating margin still to
verify.** Both saved DipTrace XML files place Würth `885012208124` 2.2 µF,
100 V X7R 1206 at C21/C22/C24/C25. The substitution was made to target at
least 1 µF per part at 36 V DC bias, which the prior placed Murata 0805 model
did not achieve. The supplied typical bias plot implies approximately
`2.2 µF × 0.515 = 1.13 µF` at 36.2 V and 25 °C. Applying the specified
−10% initial tolerance to that *typical* ratio gives about 1.02 µF, but this
is not a guaranteed minimum: the data sheet specifies nominal capacitance at
its 1 kHz test condition, not a minimum at 36 V DC bias. For illustration,
also applying the X7R −15% temperature extreme to 1.02 µF yields about
0.87 µF before ageing. That is a conservative margin illustration, not a
measured capacitance at an operating temperature. Keep the Würth MPN selected;
verify its exact-part biased impedance/ripple at the switching harmonics,
assembled pocket clearance, and finished capacitor-to-U3 supply/ground loops.
The dated Murata and unplaced-Würth descriptions below record earlier states
and are superseded as descriptions of the saved design.

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

### 5.3 Bulk electrolytics

- SMD aluminium electrolytic
- 63 V preferred for 36 V PVDD
- low ESR
- suitable ripple-current rating
- nominal 470 µF reference positions

**17 October 2026 comparison — retain the selected 63 V parts at C20/C26.**
The saved schematic and PCB place Panasonic FK `EEV-FK1J471M` (catalogue
`EEVFK1J471M`), 470 µF/63 V, at both positions. Panasonic lists its body as
16.0 mm diameter × 16.5 mm
length, with 1.41 A RMS rated ripple at 100 kHz and 105 °C. The direct FK
470 µF/50 V alternative `EEVFK1H471M` has the *same* 16.0 × 16.5 mm body;
it therefore solves no placement problem. Its 100 kHz ripple rating is
1.61 A RMS, but that is not a reason by itself to lose voltage margin. The
36 V PSU can be adjusted to 39.6 V, and its overvoltage-shutdown threshold
extends to 48.6 V; 63 V gives useful room for rail peaks while adding no
body size within this direct comparison. These PSU limits are not permission
to operate the TPA3251 near its 50 V PVDD absolute maximum. A genuinely
smaller 36 V bulk part would require a separate exact-part comparison of
capacitance, ripple heating, lifetime, footprint and actual rail peaks.

The bulk terminals need a broad, paired supply/return connection into the
amplifier rail. They need not sit adjacent to the C21/C22/C24/C25 ceramic
pads, whose local U3 loop handles the fast switching current. C20's current
placement is promising for plane connection; C26's more distant position
remains an open routing choice, not a reason to change voltage rating.
[Panasonic 63 V part](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEVFK1J471M),
[Panasonic 50 V part](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEVFK1H471M),
[RSP-200 specification](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf).
