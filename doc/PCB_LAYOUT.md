# PCB layout review

> **Lifecycle:** `rev0` bare-board release review; fabrication order pending
>
> **Owns:** Whole-board PCB observations, finding IDs, and layout release gates
>
> **Does not own:** Circuit values, supply architecture, assembled performance, or historical reviews
>
> **Read when:** Changing routing, copper, stack-up, connector wiring, or preparing fabrication outputs
>
> **Current conclusion:** The `rev0` schematic and PCB match by reference, value, update identity and net names. The latest Gerber ZIP postdates the repoured PCB, has four copper layers and separate plated/non-plated drill files, and passes a bounded format and hole-count check. U9 retains the accepted larger-land `M` DPAK pattern. No remaining bare-board data defect was found.
>
> **Next gate:** On the JLCPCB upload preview, confirm four layers in order, outline/holes/masks/silks aligned, six mounting holes non-plated, and the selected standard four-layer 1.6 mm order options before placing the bare-board order.
>
> **Limitations:** The user reports zero DRC and connectivity errors after the latest refill; earlier ERC was zero and the schematic is unchanged. This reviewer could not inspect the DipTrace reports. The latest ZIP received a bounded check, not a full CAM preview. Saved files do not prove assembled fit, solder quality or thermal performance.
> **Last reviewed:** 2026-10-27

## 1 Reviewed design state and scope

**27 October `rev0` release checkpoint.** The canonical schematic
`diptrace/main_board.dchxml` is SHA-256
`D32DE55442534BC2B6AEB46371B348DD89A16E49C0881064982B35FEF5CE8A38`;
the repoured PCB `diptrace/main_board.dipxml` is SHA-256
`2566DC53B2800D2BB77E65392855E20AC70685DF370FEAFA871E9B888E80945`;
and the regenerated `diptrace/main_board_gerber.zip` is SHA-256
`B972AA8C73CF49E10C61E563714C4B6B9FCF4BA358B8F7B25F7A1E8C4075AA51`.
The schematic hash is unchanged from the preceding checkpoint; the user reports
only trace and via tidying in the PCB, followed by repour and zero-error DRC
and net-connectivity checks. The reports were not inspected here.

Both XML roots still identify DipTrace 5.3.5.1. Read-only comparison finds
the same 132 electrical references, placed values and update IDs, and 76 net
names in schematic and PCB, without a mismatch. The PCB retains a 90 × 100 mm
outline, four copper layers, 438 static vias and 41 pours marked poured. The
ZIP postdates the saved PCB and passes its CRC check. Its Gerber X2 headers
identify Top, Inner 1, Inner 2 and Bottom copper, profile, masks and silks;
the separate drill files have six non-plated mounting holes and 438 × 0.20 mm
plus 20 larger plated holes. These bounded checks found no regression in the
export structure. The preceding replacement-export checkpoint below contains
the deeper geometry and pad-alignment checks on the prior export; they are not
claimed afresh for this ZIP. The JLCPCB rendered upload preview remains the
final check before ordering.

**27 October replacement fabrication-export checkpoint (superseded export).** The replacement
`diptrace/main_board_gerber.zip` has SHA-256
`B9233717CB2C92A91CA7B3F771D91E44AA0DA703077C703DD6AB7ED8674E8F36`.
It was exported after the currently saved repoured PCB (SHA-256
`B8BAC7BB2FABF6BEB02CE63F7474623AD7DE197D6F06D93F16689F662F2DF207`).
The ZIP passes its internal CRC check. Gerber X2 functions identify copper
L1–L4 in order, both solder masks, both silks and a single closed 90 × 100 mm
profile. The files use millimetres and the same coordinate format, terminate
normally, and their drawn coordinates lie inside the profile. Top/Bottom
Assembly and empty Dimension drawings are also present; they are not required
for a bare-board order.

`NonPlated_Through.drl` has exactly the four 3.00 mm corner mounting holes
and two 2.50 mm internal mounting holes, at the saved component positions.
`Plated_Through.drl` contains 438 × 0.20 mm, 4 × 0.80 mm, 8 × 1.00 mm and
8 × 1.40 mm holes. All 438 small drilled positions match the saved layout's
438 placed vias within 0.005 mm, the rounding of the 0.01 mm Excellon
coordinates, and every via coincides with a copper-pad flash on all four
layers within the same tolerance. The larger plated holes coincide with
copper-pad flashes. No NPTH centre has a copper-pad flash. U9's two lead
lands and tab are present in Top copper and mask at the saved positions, and
six tab-paste windows remain. All eleven test pads still have Top paste
openings (PR-013).

This closes the drill-separation defect in the output data. The bare-board
package is ready to upload for the selected JLCPCB standard four-layer,
1.6 mm order. Check JLCPCB's rendered layer/drill assignment and order
options before payment; the online CAM preview and manufacturing outcome
were not independently observed. [JLCPCB upload guidance](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-9).

**26 October U9 and first fabrication-export checkpoint.** The repoured PCB is
`diptrace/main_board.dipxml`, SHA-256
`B8BAC7BB2FABF6BEB02CE63F7474623AD7DE197D6F06D93F16689F662F2DF207`.
The schematic is SHA-256
`D32DE55442534BC2B6AEB46371B348DD89A16E49C0881064982B35FEF5CE8A38`.
The user reports zero ERC, DRC and connectivity errors after this refill; the
reports were not independently inspected. The first
`diptrace/main_board_gerber.zip`, SHA-256
`7E797BD3ED3E2998814DE1FC6A4CB5131CE742752432E59B22088626E2D76DFE`,
predates the refill and is **not** a verified export of the latest saved PCB.

The saved U9 uses `DPAK3P228_972X240L100X77T510X540M_AP1`, with correct
`17V3` input, `12VAMP` output and GND-tab pad assignments. Its two lead lands
are nominally 2.43 × 1.32 mm each and its tab land is 6.04 × 5.63 mm. The
first Gerbers contain corresponding Top copper and mask apertures and six
separate tab-paste windows. The tab land remains smaller than ST's recommended
6.70 × 6.70 mm; the first-prototype choice is accepted as an assembly and
thermal qualification item rather than a reason to redesign the footprint
again before bare-board fabrication. [ST L78M datasheet](https://www.st.com/resource/en/datasheet/l78m.pdf).

The first ZIP identifies Top, two inner and Bottom copper layers, Top/Bottom
masks and silks, paste layers and one closed rectangular profile from
(10, 10) to (100, 110) mm. Its `Through.drl` contains 438 holes of 0.20 mm,
four of 0.80 mm, eight of 1.00 mm, eight of 1.40 mm, two of 2.50 mm and four
of 3.00 mm. The 2.50 and 3.00 mm positions match all six saved mounting-hole
components, which the user confirms are intended to be non-plated. The drill
file carries no plating distinction. All eleven 3 mm Top test pads also have
paste openings, relevant if a stencil is ordered, though not to bare-board
fabrication. This was a read-only geometry inspection, not a complete visual
CAM preview or independent DRC.

**26 October targeted checkpoint.** After the user's purchasing-field corrections,
the current `diptrace/main_board.dchxml` has SHA-256
`04CB0644DBC4263081CAAF9FE476A032DD047FD091834473BFBCBFC32E69034E`;
the current `diptrace/main_board.dipxml` has SHA-256
`3A94A42EA144EA97AB3F77DD89862332CFA31B0657CC3951DD64A756987B4463`.
Both declare DipTrace 5.3.5.1. Read-only comparison found matching mapped
schematic and PCB pad nets for the new U11/R40/D4 ACTIVE circuit. U11's
N-channel gate/source/drain are `AMP_nRESET`/GND/`LED_RESET_K`; D4's
anode/cathode are `LED_RESET_A`/`LED_RESET_K`; R40 feeds the anode from
`12VAMP`. U11's unused P-channel pads are grounded and R39 is absent.
Top Silkscreen has `ACTIVE` beside D4. The historical net names
`LED_RESET_A/K` do not change the indicator's active-high function. The
manufacturer's physical LED polarity marking and fabrication preview were
not established by this saved-file inspection. The user subsequently refilled
the current board and reported zero ERC, DRC and connectivity errors. Those
results were not independently observed; the later purchasing-field edits
did not change electrical values, nets, footprints or routing.

The user selected JLCPCB standard four-layer, 1.6 mm construction. The saved
34.8 µm outer / 15.2 µm inner copper and 0.2104/1.065/0.2104 mm dielectric
entries nominally match JLCPCB's published no-impedance-requirement example.
The final order options and fabrication outputs still need comparison.

**25 October whole-board checkpoint (superseded file state).**

The current release-candidate inspection applies to `diptrace/main_board.dipxml`,
SHA-256 `F55A863D50C3034E12C28E9968B09530AE61A29217930F923783F73DBF5ED8D2`,
and `diptrace/main_board.dchxml`, SHA-256
`53A4543C309785F299D004AA5E3C36947126B3C23A494457F259D0F2FCFC80C6`.
Both declare DipTrace 5.3.5.1. The rectangular outline remains 90 × 100 mm
and the board has four copper layers. Read-only XML comparison found the same
77 net names and 133 placed electrical component references, with matching
placed values and update identities; the PCB additionally has six mounting
holes and 440 static vias. Matching schematic library pin numbers through
the footprint's printed pad numbers (rather than DipTrace's internal pad IDs)
found 369 mapped pins with no missing pad or net mismatch, including U9 and
the new test pads/RESET indicator. This checks assignments, not the
manufacturer's package drawing or copper connectivity. All 42 saved copper
pours have `Poured=Y`; the
524 stored ratlines are all hidden. These flags do not prove connected fills.
The smallest stored trace width is 0.20 mm, and the via style is 0.45 mm pad
with a 0.20 mm drill; capability must be checked against the actual order.

At the 25 October checkpoint, TP1–TP11 were 3 mm circular exposed Top pads.
TP2 is `12VAMP`, TP3 `15VA`,
TP4 `VMID`, TP8 `17V3`, TP9 `AMP_nRESET`, TP10 `AMP_nFAULT`, and TP11
`AMP_nCLIP_OTW`; TP1/TP5/TP6/TP7 are `GND`. The former D4/R39/R40/U11 RESET
indicator was present with matching schematic and PCB net assignments;
the 26 October ACTIVE revision above supersedes it.
J6 pins 1–3 remain `36V` and 4–6 `GND`. The supplied layer screenshots show
the broad Inner 1 supply and Inner 2 ground regions, but the new fills have
not received a fresh geometric continuity extraction.

The saved DRC configuration checks clearance, size and pours, but disables
silkscreen, courtyard, keep-out and same-net checks. `DRCDone=Y` has no
inspectable dated result, and no `DesignErrors` block is saved. The running
PCB Layout process exposed no targetable window; a separate launch was checked
at the documented intervals and stopped after 30 seconds. This reviewer did
not obtain a live refill, connectivity or DRC report; the user subsequently
confirmed passing DRC and net-connectivity checks on this board (PR-009).
No Gerber, drill or manufacturing preview was found in the project.

### 1.1 Earlier whole-board copper checkpoint

This review applies to `diptrace/main_board.dipxml`, SHA-256
`160A46E1D6EC09E2FC837199050BA864772BA0605893DE76FB509E94B30DC855`,
and `diptrace/main_board.dchxml`, SHA-256
`376716B4471C3CCE27F6F3FA0B69D50D98FCC7D7C3686E60A50C53CC2DFC04FF`.
They declare DipTrace 5.3.5.1. The PCB is 90 × 100 mm and four-layer. The
user-supplied Top, Inner 1, Inner 2, and Bottom screenshots show the same
board view with stored fills visible. Apply the shared
[PCB review procedure](../../Hub/procedures/pcb-review.md) when refreshing this
checkpoint. Earlier focused reviews remain dated evidence in
[power amplifier](POWER_AMPLIFIER.md) and
[power and grounding](POWER_AND_GROUNDING.md).

During the 25 October test-access review, the PCB was saved again at 10:01:57
local time with SHA-256
`73B3166C6ECDA55AED1D494DB24EE6E3015BF960A1D83707B27CF3603F28A208`.
That intermediate file still had TP1 on `GND` and no TP2 or dedicated status pads.
The earlier copper, stack and connectivity findings below remain identified by
the earlier `160A46…` hash; the later save was not requalified as an unchanged
board.

Read-only XML comparison found all 119 placed electrical components represented
in the schematic, with matching reference, value, update identity, and all 351
physical pad-to-net assignments. The schematic and PCB contain the same 74
net names. This is evidence of netlist correspondence, not of copper
connectivity, footprint suitability, or correct circuit intent. The board has
43 pours and 435 placed static vias. The nominal stored stack is
34.8 µm outer and 15.2 µm inner copper, with a 1.065 mm core and 0.2104 mm
prepreg on each side; confirm the selected fabrication order before relying on
these entries.

All 510 stored ratline objects are hidden; none is visible. J6 pads 1–3
are assigned to `36V` and pads 4–6 to `GND`. The stored Inner 1 `36V` fill
reaches the three positive entry pads and the amplifier supply field; GND
remains joined locally across U3 and at the return pads. This supersedes
the immediately preceding 25 October snapshot, hash
`B26749BDA17BA4B56AF859A33D7AB2A2F7CEE790E415301B781D86B1F4347160`
(45 pours, 436 static vias, broad Inner 1 GND and Inner 2 36 V), and the earlier hashes
`DF2F318EA88851FE0CDF6A74571A23B4622AB4BBA13829EBCE0472407E80CE62`
(five visible GND and two 36 V links) and
`C7A941B778996B496750056CD12AB4532AE5C890717A33106776274D96DFB34E`
(two visible 36 V links). Hidden ratline objects are not a count of
unrouted connections. The user subsequently confirmed a passing
net-connectivity check on this board (PR-009).

The saved DRC configuration has clearance, copper-pour, and size checking
enabled, but silk, courtyard, keep-out, and same-net checking disabled. The
XML has a `DRCDone` flag without a dated, inspectable current error report.
DipTrace PCB was reported running but did not expose a targetable window
during this review. To avoid opening a second instance on the same file,
a live refill/connectivity/DRC pass was not performed by this reviewer.
The saved flag is not a release result; the user's later reported DRC and
connectivity passes close PR-009 for the current board.

## 2 Findings

Severity describes credible consequence; state describes evidence. Retain
these IDs in follow-up reviews. PR-001–PR-007 record the earlier `160A46…`
copper checkpoint and are not fresh connectivity or clearance results for
the earlier `F55A86…` file. PR-008–PR-014 state the later inspections.

| ID | Severity | State | Location | Finding and consequence | Action |
| --- | --- | --- | --- | --- | --- |
| PR-001 | Low | Needs verification | U9 `GND` tab and four layers | The 24 October missing local via/plane structure remains addressed geometrically. The Top GND pour outline is about 544 mm²; in a 20 × 20 mm square centred on the tab, stored GND fill is approximately 232, 393, 382 and 389 mm² from Top to Bottom. The Inner 1 local fill has grown from about 307 mm² in the preceding snapshot. Nineteen GND vias are within 10 mm of the tab centre, five within 5 mm. Cooling at actual load remains unmeasured. | Keep the broad direct tab connection and measure U9 case/copper and local air temperature at the actual sustained 12 V load. Do not add copper solely to meet an arbitrary area figure. |
| PR-002 | High | Confirmed resolved in saved copper | U3 ground region | The earlier seam through U3 has been joined in the later saved fills. No GND ratline remains visible. This restores a local PCB path between its ground-pin groups; its impedance and the exact current distribution are unmeasured. | Preserve this contiguous local copper and recheck it after any entry-wiring or pour change. |
| PR-003 | Medium | Closed on user-supplied fastener dimensions | C20/C26 and mounting holes 5/6 | The selected fastener assembly's largest part is its 5 mm-diameter washer inside a 6 mm-diameter keep-out: 0.5 mm nominal radial margin. The user confirms this resolves the mounting-fastener concern. The previously noted C26-to-board-edge clearance remains a nominal image-derived observation, not a measured interference. | Preserve the selected fastener and keep-out dimensions; revisit only if the hardware or board geometry changes. |
| PR-004 | Medium | Confirmed resolved in saved copper | Former internal GND links | The earlier via 254–R38 and via 245–via 244 visible links, along with the J6 GND link, are no longer visible. | Confirm the resulting GND connectivity in DipTrace after refill; retain the local control and decoupling return paths. |
| PR-005 | Medium | Confirmed resolved in saved copper; harness needs verification | J6 and 600 mm PSU harness | The three J6 positive pads now feed one `36V` field and the three return pads feed common GND. The former buck-only positive and parallel return imbalance is removed on the PCB. Actual PSU wiring and physical +/− pairing are not shown by the layout. | Connect the three positive leads to the common PSU +V and their three adjacent return leads to common -V as paired paths. Check pin numbering, polarity, cable routing, connector and pad necks; do not rely on equal current sharing. |
| PR-006 | Low | Confirmed resolved in saved copper | Inner 2 beneath U3 | The broad `GND` fill is again on Inner 2, 0.2104 mm from the rear Bottom layer, and is continuous across the U3 region in the stored fill. Bottom GND and 53 local GND static vias within 10 mm of U3's centre remain; the former adjacent `36V` tongue has moved to Inner 1. | Preserve the local Bottom capacitor-to-pin loops and check the actual ground continuity after refill. No extra U3-side GND patch is indicated by this review. |
| PR-007 | Low | Needs verification | Top analogue traces around x = 60–72 mm, y = 69–92 mm | The inner-layer swap also puts broad `15VA` copper on Inner 1 directly beneath parts of the buffered/filter and `VMID` routes. Inner 2 GND remains beneath them, but the Top-to-GND spacing is approximately 1.275 mm instead of 0.2104 mm. The short raw `R_IN`/`L_IN` routes beside J4 remain over the right-side Inner 1 GND strip. This is a reference/return-path trade-off, not evidence of audible noise. | Retain the present layout unless final route inspection or prototype noise reveals a problem. If refining it, give the sensitive Top routes a local Inner 1 GND reference without severing the low-current `15VA` distribution; do not swap the whole planes back merely for this point. |
| PR-008 | Low | Confirmed resolved in current saved assignments | Test access | The earlier board had only TP1. The current schematic and PCB place TP1–TP11, including the three status nodes, four rails/reference nodes and four GND pads. All are Top-side 3 mm pads. | Check probe approach after components and the rear plate are fitted. |
| PR-009 | High | Closed on user-reported checks | Current board after refill | The user reports zero DRC and net-connectivity errors after the 27 October trace/via tidying and repour. The prior ERC was zero and the schematic hash is unchanged. Reports were not independently inspected. The saved DRC configuration disables courtyard and keep-out classes; the pass applies to the checks as run. | Repeat affected checks if electrical design, routing, pours or rule configuration changes. Inspect final manufacturing outputs and relevant excluded rule classes under PR-010. |
| PR-010 | High | Export defect resolved; upload preview pending | Fabrication release | The prior 27 October replacement ZIP passed four-layer, outline, hole-count and coordinate-alignment checks. The current `rev0` ZIP postdates the new refill; bounded checks confirm its CRC, layer-function headers and separate six-hole NPTH and plated drill files. The deeper coordinate-alignment check has not been repeated on this export. No bare-board data defect is known. | Upload the `rev0` ZIP whose hash is recorded in §1 to JLCPCB. Confirm its preview maps Top, Inner 1, Inner 2 and Bottom in order, shows the 90 × 100 mm outline and all six NPTH mounting holes, with masks/silks aligned. Select standard four-layer 1.6 mm construction and inspect the order options before payment. If the viewer misassigns extra Assembly/Dimension drawings, omit those drawing layers from the upload. [JLCPCB upload guidance](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-9). |
| PR-012 | Medium | Saved geometry confirmed; prototype assembly verification open | U9 DPAK assembly lands | The placed `DPAK3P228_972X240L100X77T510X540M_AP1` pattern has 2.43 × 1.32 mm lead lands and a 6.04 × 5.63 mm GND-tab land. The lead lands are about 28% larger in area and the tab about 4% larger than the preceding `N` pattern. Copper, mask and six tab-paste windows appear in the first export. ST recommends 3.00 × 1.60 mm leads and a 6.70 × 6.70 mm tab; the present land is a documented smaller-land choice, not a datasheet match. | Retain for the first prototype, inspect lead and tab solder joints after assembly, then measure U9 temperature at sustained real load. Revisit the land only if assembly or thermal results warrant it. [ST L78M datasheet](https://www.st.com/resource/en/datasheet/l78m.pdf). |
| PR-013 | Low | Confirmed in replacement paste export | Top test pads TP1–TP11 | All eleven exposed 3 mm probe pads have matching 3 mm openings in `TopPaste.gbr`. This would deposit solder on the test pads if a stencil is made from this file. | No bare-board fabrication change is needed. Before ordering a stencil or assembly, suppress paste on these pads or omit them from the stencil. |
| PR-014 | Low | Saved geometry confirmed; noise outcome unmeasured | Copper beneath L5 and L1–L4 | At the L5 body, the Top has the intended switch/output copper; Inner 1, Inner 2 and Bottom have GND pour outlines, with no separately routed trace crossing the body. At L5's height the Inner 1 `15VA` pour begins near x = 39.5 mm, about 25 mm from its centre. The four shielded output inductors have 36 V pour outlines on Inner 1 and GND on Inner 2/Bottom. A Bottom `AMP_nRESET` route crosses the edge of L1's body, but Inner 2 GND lies between it and the inductor. Local magnetic/stray-capacitive currents are plausible; a harmful analogue-ground or 15 V disturbance is not established by this geometry. | Retain the continuous planes. Do not cut GND beneath L5 solely to prevent eddy currents; that could weaken the reference and return paths. On the prototype, compare `17V3` and `15VA` ripple and analogue-output noise at idle and representative load with short local probe returns; revisit the copper only if a material problem is measured. |
| PR-011 | Low | Confirmed geometry; access needs verification | Ripple-probing return | The nearest dedicated GND test pad is 16.6 mm from TP8 (`17V3`) and 17.0 mm from TP3 (`15VA`). That span creates an avoidable probe loop if used for switching-ripple measurements. | For ripple, use an accessible nearby capacitor GND pad and a short spring return; add another GND test pad only if those local pads prove inaccessible after assembly. |


PR-008 is resolved in saved assignments; physical probe access with the
assembled board and plate remains to be checked.

## 3 Engineering interpretation

At J6, all three positive pads now join the `36V` field and all three return
pads join GND. The Mean Well RSP-200-36 has one output rail brought to
multiple terminals, so the proposed three nearby +/− cables are parallel
distribution paths, not isolated amplifier and buck supplies. The
[power and grounding authority](POWER_AND_GROUNDING.md#4-36-v-distribution)
owns the final harness decision. The earlier same-day board left the buck
positive separate while GND was common, so its buck-labelled return could
carry amplifier current without a matching positive current. That specific
asymmetry is resolved in saved copper. Parallel paired conductors can still
carry unequal currents; route each +V close to its own -V and check actual
pin numbering and PSU termination. The current Inner 1 36 V pour forms a broad
J6-to-amplifier field. No obvious single narrow entry neck is visible in the
stored fill. A final manufacturing preview is still needed; the user has
confirmed passing current-board DRC and connectivity checks.

Each proposed 600 mm, 1.31 mm² conductor has about
`0.0172 Ω mm²/m × 0.6 m / 1.31 mm² = 7.9 mΩ` resistance at 20 °C before
contacts. A single paired cable at the PSU's 5.56 A rating would drop about
`5.56 × 2 × 7.9 mΩ = 0.088 V`; three equally sharing pairs would have roughly
one third of that cable drop, but sharing is not guaranteed. Molex's
[Mini-Fit Jr specification](https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/555/5556/PS-5556-001-001.pdf)
gives a 7 A per-contact guideline for the six-circuit 16 AWG brass-contact
arrangement under its reference conditions. The design does not depend on
equal sharing, but enclosure temperature, contacts and PCB copper still need
checking. The buck branch is now taken locally from the common 36 V field;
its close input capacitor, rather than the long PSU cable, must close the
high-frequency switching-current loop.

The latest revision restores broad GND to Inner 2 and broad 36 V to Inner 1.
At U3's centre, the Bottom GND remains local and the Inner 2 GND fill is
continuous through x = 38.1–70.6 mm at y = 33.7 mm, apart from local pad/via
clearances. Fifty-three GND static vias lie within 10 mm of U3's centre,
including 29 within 5 mm; the 19 local 36 V vias remain. A Bottom trace
needing the inner GND reference now sees 0.2104 mm of dielectric rather than
0.2104 + 1.065 = 1.2754 mm in the preceding revision, approximately a
sixfold reduction in trace-to-plane spacing. This improves the local
return geometry; it does not by itself prove less noise or lower total
switching-loop inductance. TI's
[TPA3251 layout guidance](https://www.ti.com/lit/ds/symlink/tpa3251.pdf)
calls for contiguous local GND under the device, close PVDD ceramics and
short input routing with its source ground.

The swap also moves the 36 V plane one internal layer farther from the
Bottom U3 pins. Using the [previous via-barrel estimate](POWER_AMPLIFIER.md#112-via-barrel-resistance-estimate-17-october-2026),
one Bottom-to-Inner 1 transition is about 2.01 mΩ rather than 0.36 mΩ for
Bottom-to-Inner 2. If all 5.56 A passed evenly through the 19 local 36 V vias,
their ideal parallel barrel resistance would be approximately 0.106 mΩ
instead of 0.019 mΩ, a change of only about 2.7 mW of barrel loss. Real
current shares with other paths, and plane spreading and via inductance are
outside that simple DC calculation. More importantly, C21/C22/C24/C25 still
connect to the U3 PVDD and GND pins through short Bottom-side copper, so the
closest commutation loops do not make the full plane round trip.

On the front, the raw `R_IN`/`L_IN` routes beside J4 still have adjacent
Inner 1 GND. Farther in, a large Inner 1 `15VA` field now underlies parts of
the Top buffered/filter and `VMID` routes around x = 60–72 mm, y = 69–92 mm.
Their continuous GND reference is on Inner 2, approximately 1.275 mm below
Top instead of 0.2104 mm. This is the counterpart of the U3 improvement,
but these low-frequency, low-current traces do not justify reversing the
whole layer allocation. Check the route and assembled noise before pursuing
a local Inner 1 GND corridor.

The U3-side bulk supply and speaker-output copper, local ceramic paths, and
large 36 V/GND fields are present. The additional Bottom GND does not visibly
remove the small Bottom `AMP_OUT_A`–`AMP_OUT_D` fields. At y = 33.7 mm the
stored Inner 1 36 V fill spans x = 20.0–41.2 mm beside the U3 via field,
while Inner 2 GND extends across U3's input side. This is a useful geometric
improvement in the local return, though the wider distant fields mainly
reduce DC spreading resistance. For scale, a hypothetical 40 × 20 mm,
15.2 µm inner-copper strip has about `1.13 mΩ/square × 2 squares = 2.3 mΩ`;
at 5.56 A it drops about 13 mV and dissipates about 70 mW. This is not an
extracted resistance of the non-uniform pour. Current is shared with the
bulk capacitors and other copper, and actual necks and contact resistance
matter more than the largest visible area. The 34.8/15.2 µm stack remains a
reasonable initial 1 oz outer / 0.5 oz inner construction; a final filled
neck and thermal check can decide whether heavier copper has a real benefit.

The PBTL loudspeaker current flows from one output bank through the speaker
to the other output bank, rather than returning as a 6 A audio current through
the analogue plane. The relevant GND disturbances are the local PVDD
capacitor and output-filter return currents. Their components and broad
left-side copper sit near U3 and the output connector; the raw input traces
lie to the right above local Inner 1 GND, while the later analogue stages
mostly reference Inner 2 GND. This is a favourable route ordering, but a
shared plane can still develop a voltage gradient. Keep the
output-filter returns local and the isolated RCA returns on the input side;
check hum/noise on the built board before introducing another plane split.

For U9, local stored fill within a 20 × 20 mm square around its tab is about
232, 393, 382, and 389 mm² on Top, Inner 1, Inner 2, and Bottom respectively.
These overlapping layers conduct into one another and are not four independent
free-air radiators. The extra Inner 1 copper helps spread heat but is unlikely
to replace the tab-to-board/via path as the main constraint. For U3, the
package-to-TIM-to-aluminium-plate path remains the designed heat exit; extra
GND copper can help heat escape through the pins but does not replace that
interface. The previously estimated U9 0.75 W at a provisional 120 mA
load is useful for scale, but actual continuous current and enclosure air
temperature control the required heat path. The relevant calculation and
uncertainties remain in
[power and grounding](POWER_AND_GROUNDING.md#12-12-v-and-15-v-linear-regulator-branches-reviewed-2026-10-13).

**27 October inductor-plane review.** The selected L5 is Bourns's
semi-shielded `SRN8040-470M`; L1–L4 use Vishay's shielded
`IHLP5050FDER100M5A`. At L5's roughly 8 × 8 mm body, the stored Inner 1,
Inner 2 and Bottom pour outlines are GND throughout a sampled grid. There is
no separately routed trace under that body on any layer. At y = 90.9 mm the
Inner 1 `15VA` outline begins around x = 39.5 mm, while L5 is centred at
x = 14.5 mm. Around L1–L4, Inner 1 is predominantly 36 V and Inner 2 GND;
the saved Bottom `AMP_nRESET` trace clips L1's body edge with Inner 2 GND
between trace and inductor. Copper-pour outlines and trace geometry establish
placement, not the amplitude of coupled noise or exact post-fill current flow.

For L5's nominal 36 V input, 17.36 V output, 47 µH and 674 kHz switching,
`D ≈ 17.36/36 = 0.482`, `T_ON ≈ D/674 kHz = 0.715 µs`, and
`di/dt ≈ (36 − 17.36)/47 µH = 0.397 A/µs`. The ideal continuous-mode rise
is therefore about 0.284 A per on-time, a current ramp rather than a sharp
current spike. At light load the MP4541 can pulse-skip, so this nominal
continuous-mode calculation does not predict the idle spectrum. The
switch-side winding still sees fast voltage edges, and the semi-shielded
part has some leakage field. A close continuous plane
can intercept capacitive coupling and carry local eddy currents, while a
cutout may weaken shielding and force return-current detours. The current
geometry and the selected inductor do not justify a pre-fabrication cutout.
The more consequential paths to the 15 V analogue rail are conducted `17V3`
ripple and any common impedance between buck switching returns and the quiet
LDO/analogue return. The local input/output capacitors and their complete
return loops, rather than the presence of GND under L5 alone, set those paths.
This is a risk judgement pending prototype measurements, not an EMI result.
[ADI inductor-plane guidance](https://www.analog.com/en/resources/analog-dialogue/raqs/raq-issue-164.html),
[MPS MP4541 layout guidance](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP4541GN/document_id/9688/),
[Bourns SRN8040](https://www.bourns.com/docs/product-datasheets/srn8040.pdf),
[Vishay IHLP5050FD-5A](https://www.vishay.com/docs/34337/ihlp5050fd-5a.pdf).

### 3.1 Earlier test-access proposal, 25 October 2026

At the time of this proposal the PCB had one dedicated test pad, TP1 on
`GND`. The following were candidates; the current board implements the
priority rails, status signals and local grounds as described in §1. Put any
future accepted
pads on the accessible Top side, with a short connection to the named net and
room for the intended probe after assembly; avoid the plate-facing Bottom
side, supply/output necks, and the amplifier's close capacitor loops. For
handheld probing, about 1.5–2 mm exposed pad diameter with several millimetres
of clear approach is a practical starting point, subject to actual probe tips
and local clearance; use a larger target only where access needs it. Pair a
rail-ripple pad with a nearby GND pad so the probe loop does not dominate the
observed waveform.

| Priority | Net and suggested neighbourhood | Bring-up question |
| --- | --- | --- |
| High | `17V3` near U9 input/C36; `12VAMP` near U9 output/C37 or the amplifier-side C8 | Is the buck healthy, and does the 12 V regulator maintain headroom through start-up and loaded troughs? Two observations distinguish buck sag from LDO/distribution sag. |
| High | `AMP_nRESET` near its Top-side transition towards U3; `AMP_nFAULT` and `AMP_nCLIP_OTW` near their Top-side U4/U10 inputs | Did RESET release and assert at the intended time, and did either active-low status line pulse? The LEDs alone cannot establish pulse duration or FAULT during RESET. |
| High | A local `GND` pad beside the 17V3/12VAMP rail pads | Provides a defined short measurement return for rail ripple and timing; existing TP1 is near the status circuitry instead. |
| Useful if space permits | `15VA` near the analogue load/C55; `VMID` near a quiet analogue decoupler | Separates analogue-rail faults from mid-rail/reference faults and supports analogue-noise checks. Existing C48/C55 and J2 pin 3 provide less convenient access. |
| Conditional | `AMP_DVDD` near the already routed Top-side U4/U10 source branch | Checks the internal reference under the deliberately accepted indicator load. Use only a high-impedance probe; do not provide an external load or a long stub. |

J6 already carries 36 V and GND, J5 the post-filter differential speaker
outputs, and J2/J3 several analogue and drive signals. Check whether their
fitted connectors or neighbouring large capacitor pads permit safe probing
before duplicating any of these nets. Do not create routine probe pads on
`REG17V3_SW`, its FB node,
U3's raw switching outputs or bootstrap nodes; probe the existing local pads
with a suitable short-ground/differential method only if a specific waveform
question requires it. Measure the post-filter `SPK+` to `SPK-` voltage
differentially; neither speaker conductor is a scope ground.

## 4 Minimum remaining release checks

1. Preserve the resolved PR-002/PR-004/PR-005/PR-006 copper connections. Document
   the actual J6 and PSU terminations as three physically paired feed/return
   paths; verify no unintended return through the plate or RCA. Inspect the
   PR-007 analogue-side reference geometry only if refining the layout or
   investigating measured noise.
2. Retain the user-reported zero-error ERC, DRC and net-connectivity result
   after the current refill (PR-009). Rerun affected checks after any electrical,
   layout or rule change.
   The replacement Gerber/drill/mask/outline data and U9 land apertures have
   been checked. Inspect JLCPCB's upload preview, relevant excluded rule
   classes and the selected order stack against this saved design (PR-010).
3. Preserve the confirmed 5 mm maximum fastener diameter and 6 mm keep-out
   diameter that close PR-003; revisit their fit if either changes.
4. On the prototype, check U9 temperature at its real continuous load and the
   U3/plate thermal interface. Check input noise with the assembled amplifier
   at a representative loaded operating point before altering the GND plane.

This is a review of the stated board snapshot, not fabrication approval or
assembled electrical/thermal qualification.

## 5 Current release disposition, 27 October 2026

The `rev0` fabrication package is ready for JLCPCB upload, with no
remaining bare-board data defect found. Before payment, confirm the rendered
four-layer/NPTH preview and standard four-layer, 1.6 mm order options (PR-010).
PR-003 remains
closed on the user's selected-fastener dimensions. PR-009 is closed on the
user's fresh zero-error ERC, DRC and connectivity reports after repour. The
first Gerber ZIP's mixed-drill defect is superseded by the replacement export.
U9's larger `M` land geometry is confirmed, with assembly and thermal checks
remaining for the built prototype (PR-012). Test-pad paste needs attention
only if a stencil is ordered (PR-013).
The JLCPCB standard four-layer, 1.6 mm construction is selected. SR-001 is
closed by the saved N-channel green ACTIVE circuit, subject to physical
polarity and visibility checks. The [power authority](POWER_AND_GROUNDING.md)
now locks the auxiliary supply selection for the first prototype. The selected
board footprint and copper choices are accepted for one bare-board prototype;
the remaining component-fit, harness, rear-plate, U9 temperature, U3 heat
transfer and assembled-noise questions are deferred to assembly and prototype
validation. They are not pre-fabrication pass claims. The JLCPCB upload preview
and order-option comparison remain a purchase gate, not a reason to withhold
the versioned design files.
