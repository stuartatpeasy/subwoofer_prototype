# Off-board electrical bill of materials

> **State — working procurement list, 16 November 2026.** Owns the counted
> electrical items outside the partial main-board schematic and the candidate
> purchasing references in this list. It does not replace the schematic's PCB
> BOM or the electrical, mechanical and wiring authorities. Read when planning
> the component order. Next: confirm lead lengths, connector and crimp fit,
> supplier terms, and the open items in §4. Quantities are for one subwoofer;
> a candidate or drawing is not evidence of a fitted or tested assembly.

## 1. Scope and source

The partial [main-board schematic](../diptrace/main_board.dchxml) includes
PCB headers J1–J6 but not their mating housings or external panel and power
wiring. Its XML root identifies DipTrace schematic version 5.3.5.1 and inch
units; inspected SHA-256:
`8D2DF8FC4B64DD681D15BC050AD40E1F75A72F9E70D3C4CA319837E9E8CDA36C`.
The [system specification](SPECIFICATION.md), [front end](FRONT_END.md),
[power amplifier](POWER_AMPLIFIER.md), and
[power and grounding](POWER_AND_GROUNDING.md) own the selections and circuit
connections. The [fastener BOM](FASTENER_BOM.md) covers PE and other mechanical
fasteners. This is an electrical parts list, not a consolidated build or PCB
BOM; quantities exclude spares unless stated. Recheck UK stock, price, MOQ,
manufacturer part and packaging before ordering; no live availability is
promised here.

## 2. Main components and panel controls

| Item | Qty | Identity / purchasing reference | Status and notes |
| --- | ---: | --- | --- |
| Loudspeaker driver | 1 | SB Acoustics `SB23MFCL45-4` | Selected; user has received a driver |
| 36 V supply | 1 | Mean Well `RSP-200-36` | Selected, 200 W class; [manufacturer](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf) |
| PSU terminal guard | 1 | Mean Well `TBC-09` | Selected; confirm it fits the supplied PSU and loom |
| Mains inlet, switch and holder | 1 | Schurter `DD11.0111.1111`, Mouser `693-DD11.0111.1111` | Selected C14, double-pole switch, one-pole fuse, rear cover. [DD11 data](https://www.schurter.com/en/datasheet/typ_dd11.pdf) |
| Fuse drawer | 1 | Schurter `4301.1407`, Mouser `693-4301.1407` | Separate from inlet |
| Appliance fuse | 1 fitted | Schurter `0001.2507`, T2AH250V, 5 × 20 mm, ceramic | Selected; optional spare |
| RCA left / right | 1 each | REAN `NYS367-9` white, Mouser `568-NYS367-9`; `NYS367-2` red, Mouser `568-NYS367-2` | Selected; panel isolation and fit checks remain |
| Level control | 1 | Bourns `PDB181-E420K-103A2`, Mouser `652-PDB181E420K103A2` | Selected, 10 kΩ single gang |
| Crossover control | 1 | Bourns `PDB182-K420K-203B`, Mouser `652-PDB182-K420K203B` | Selected, 20 kΩ dual gang; PC-pin wiring and mounting need a fit check |
| Polarity switch | 1 | E-Switch `100DP1T1B1M1REH`, Mouser `612-100-F1112` | Selected DPDT ON–ON; confirm lever mapping |
| Control knobs | 2 | For 6 mm, 18-tooth shafts | Selection and exposed shaft depth remain open; see [mechanical design](MECHANICAL.md) |

## 3. Harnesses and terminations

| Item | Qty | Identity / purchasing reference | Status and notes |
| --- | ---: | --- | --- |
| J1 and J2 JST PH receptacle housings | 2 | JST `PHR-3` | Three positions each; mates with schematic's `S3B-PH-SM4-TB`; [JST PH data](https://www.mouser.com/catalog/specsheets/JST_B2B_PH_SM4_TB_LF_SN_ePH.pdf) |
| J3 and J4 JST PH receptacle housings | 2 | JST `PHR-4` | Four positions each; mates with `S4B-PH-SM4-TB`; same manufacturer data |
| JST PH pre-crimped leads | 14 leads | JST `01SPHSPH-26L-300`, RS `820-1412`, [RS listing](https://uk.rs-online.com/web/c/cables-wires/wire-to-board-cables-ribbon-cable/?pn=6) | Candidate: 300 mm, 0.14 mm², PH contact at both ends. Use one complete lead per circuit, remove the unused end and insert the retained contact in its housing; gives nearly 300 mm before stripping. RS listed packs of 10 in its indexed page: 2 packs for 14 leads, recheck. Do not cut seven leads in half unless 150 mm is enough. Pin each housing from the circuit, not the lead colours; actual reach remains to be dry-fitted. |
| J5 speaker-output plug and pigtail | 1 | Molex `215326-1021`, 2-way, 150 mm, 16 AWG | Current selected assembly, housing and contacts included. For the requested longer option, `215326-1023`, Mouser `538-215326-1023`, is 600 mm and may be cut to the needed length before splicing. Its longer thin-wire section and service reach must be assessed; it is a candidate, not a second assembly. [Molex series](https://www.molex.com/en-us/products/series-chart/215326). |
| J6 36 V plug and pigtail | 1 | Molex `215326-1063`, Mouser `538-215326-1063` | Selected 6-way, 600 mm, 16 AWG, housing and contacts included. Three 36 V and three return leads; verify mapping, support and termination at PSU. |
| Driver cable | As required | Generic 2 × 2.5 mm² copper, red/black insulated conductors with overall outer jacket; **no SKU** | User-specified. Dry-fit with independent service slack at both ends before cutting; pass jacket through sealed, protected feed-through. |
| Driver female blade receptacle | 2 | TE `9-160313-2`, Mouser `571-9-160313-2` | Candidate for measured ~6.3 × 0.7–0.8 mm tabs; 1–2.5 mm² and 4.32 mm maximum insulation OD. **Not yet physically confirmed**: test fit and retention, conductor insulation diameter and correct crimp tool. [TE data](https://www.te.com/en/product-9-160313-2.html). |
| Speaker-cable to J5 pigtail splice | 2 | Insulated, mechanically supported splice suitable for 1.31 mm² to 2.5 mm² copper | Select a splice specifically rated for both sizes and the chosen crimp tool; no exact part selected. Never force 2.5 mm² into the Mini-Fit contact. |
| IEC inlet female blade receptacle | 3 | Z+F `V70FV007006`, fully insulated, 4.8 × 0.8 mm, 0.5–1.5 mm² | Candidate for line, neutral and PE, one wire each. [Manufacturer catalogue](https://zf-usa.com/wp-content/uploads/2025/06/2025-05-Z-F-Terminals-Catalog-MAY-30-V2-1.pdf) identifies the size and insulation; confirm voltage/temperature, wire insulation OD, crimp tool, tab fit and inlet rear-cover clearance before selection. A partially insulated barrel alone does not meet the fully insulated requirement. |
| PE stud ring terminals | 2 | Insulated M4 rings suitable for 0.75 mm² green/yellow wire | One each from inlet and PSU FG; choose compatible crimp/tool, flat contact faces and adequate insulation rating. |
| PSU mains and FG terminations | 3 | Insulated M3.5 ring terminals, or manufacturer-compatible ferrules | One each L, N and FG, for 0.75 mm². Determine final style against the PSU terminal-block drawing and cover; FG connects to the PE stud. Do not infer a bare-wire connection is acceptable. |
| PSU DC terminations | 6 | Insulated M3.5 ring terminals or manufacturer-compatible ferrules for 16 AWG (~1.31 mm²) | One per J6 pigtail conductor, one wire per PSU screw, three +V and three −V. Confirm screw/terminal fit and routing. |
| Control wiring and jumpers | As required | Insulated signal wire compatible with the 0.14 mm² JST leads and solder lugs / PC pins | Include J1 dual-gang straps, J3 cross-over jumpers, J4 RCA returns and appropriate insulation/strain support. Preserve wiring and pin maps in [front end](FRONT_END.md); final lengths remain open. |
| Tri-rated mains wire, brown | As required | 0.75 mm² stranded copper, brown, 300/500 V minimum, temperature suitable for enclosure | Inlet switched line to PSU L; cut after service-position trial. Example [CPC brown 100 m reel](https://cpc.farnell.com/pro-power/tr-0-75mm-brn/cable-tri-rated-0-75mm-brown-100m/dp/CB15113); large reel is an example, not an ordering recommendation. |
| Tri-rated mains wire, blue | As required | 0.75 mm² stranded copper, blue, 300/500 V minimum, temperature suitable for enclosure | Switched neutral to PSU N. |
| Tri-rated protective-earth wire, green/yellow | As required | 0.75 mm² stranded copper, green/yellow, 300/500 V minimum, temperature suitable for enclosure | Separate inlet-to-stud and stud-to-PSU FG conductors; leave service slack. |
| Bonding hardware and conductors for both sinks | 2 bonds | Bare-metal contacts and suitable bonding hardware/conductors | Required; detailed terminal style and lengths still open. Do not count as completed by the greased sink joints. |
| Insulating sleeving, heat-shrink, identification and cable support | As required | Sized and rated for the actual joints and location | Cover exposed contacts and splices, provide mechanical support and segregation. |

## 4. Completion and assembly checks

1. Confirm J1/J2/J3/J4 pin maps, labels, harness reach, terminal seating and
   physical routing; 14 leads account for every connector position. J1 has
   three board conductors even though the dual pot has six pins; its straps
   are separate local jumpers.
2. Verify mains terminal and inlet-cover fit with the actual 0.75 mm² wire and
   correct crimp tooling. The 4.8 mm family includes both 0.5 and 0.8 mm tab
   thicknesses. The supplier's minimum pack size and suitability for the actual
   installation remain open. Follow the earth stack and pre-energisation bond
   checks in [power and grounding](POWER_AND_GROUNDING.md) and
   [validation](VALIDATION.md).
3. The longer J5 pigtail is an option: preserve the 2.5 mm² jacketed run,
   place supported splices in the electronics chamber and confirm both service
   positions. The current 150 mm choice and its loss estimate remain in
   [power amplifier](POWER_AMPLIFIER.md#13-speaker-output-connection).
4. Check the driver terminals physically before ordering more than samples;
   the earlier TE `640909-2` and `640923-1` did not fit the received tabs.
5. Choose and count any further hardware revealed by the final assembly,
   including PSU wiring, sink bonds, guards, cable restraints, and signal-screen
   arrangements; do not assume the PCB or cabinet model captures these.

The project Mouser Search API client could not resolve its network connection
on 16 November. Product links and indexed supplier pages were used instead;
stock, UK ordering terms and all unverified alternatives require rechecking.
