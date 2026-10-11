# Power and grounding

> **State:** Current authority for mains entry, protective earth, DC
> distribution, and grounding. The RSP-200-36, inlet, fuse, M4 protective-earth
> topology, and unfiltered-inlet decision remain locked. The auxiliary supply
> is under redesign: the canonical partial schematic now includes an MP4541GN
> candidate 36 V-to-approximately-17.36 V buck feeding a 15 V analogue LDO and
> an NCP1117 12 V amplifier LDO. The NCP1117 pin and tab mapping is now
> correct. Its output-capacitor stability, thermal design, and physical return
> paths need resolution as described in Section 1. The proposed schematic
> direction is one GND net with locally controlled analogue, buck, and
> amplifier return copper; the canonical schematic still shows three nets.
> The power tree is not approved for PCB implementation. The selected two-
> supervisor RESET topology senses 36 V and `17V3` with a selected dedicated
> divider; its headroom claim depends on the loaded buck trough and 12 V LDO
> input in [Power amplifier](POWER_AMPLIFIER.md).
> Earlier STH0548S15/LM2937 selections and their calculations below are
> superseded context, not current implementation instructions. Last reviewed:
> 2026-10-11.

## 1 Power architecture

```text
230 V AC
  |
36 V SMPS
  |
  +--> TPA3251 PVDD
  |
  +--> MP4541GN ~17.36 V buck (candidate partial schematic)
         |
         +--> NCP1117ST12T3G 12 V LDO (drawn, not approved)
         |      |
         |      +--> TPA3251 VDD/GVDD (drawn; loaded rail unverified)
         |
         +--> XC6701DF02FR-G 15 V analogue LDO (partial schematic)
                |
                +--> analogue front end
                |
                +--> buffered VMID ≈ 7.5 V
```

Requirements:

- keep the amplifier and analogue supply domains separate
- deliberate grounding/star connection
- resolve the MP4541GN implementation issues below and the 12 V
  amplifier supply faults in Section 1.2, then recalculate noise, load, heat,
  grounding, and RESET sequencing; confirm the lowest loaded `17V3` trough
  against the selected buck supervisor's release threshold

### 1.1 MP4541GN candidate schematic review (2026-10-06)

The canonical partial schematic uses `R6 = 180 kΩ` and `R10 = 11 kΩ` at FB,
giving a nominal `1 V × (1 + 180/11) ≈ 17.36 V` output. `R5 = 47 kΩ` sets
approximately 674 kHz in the manufacturer's nominal frequency equation.
With 36 V input and `L1 = 47 µH`, ideal nominal inductor ripple is about
0.28 A peak-to-peak. The Bourns `SRN8040-470M` has 1.4 A rated RMS current,
1.5 A saturation current, and 0.19 Ω maximum DCR; the current rating is
plausible for the auxiliary load, subject to its completed load budget.

The revised canonical XML shows a nine-pad SOIC-8EP pattern for `U2` and
1210 patterns for `C7`–`C9`. U2 has symbol pad 9 assigned to `PGND`.
Verify the actual land dimensions against the chosen parts and the resulting
PCB netlist before layout.

The current XML assigns `C5`–`C7` (36 V input capacitors), `C9`–`C11`
(buck output capacitors), `C14` (U2 VCC decoupling), `R8` (FREQ), `R4/R9` (EN
divider), `R6/R10` (FB divider), and U2 GND pin 7 and exposed pad 9 to `PGND`.
The 15 V LDO U3 and its local bypass capacitors remain on `AGND`.
Connect R10 to a quiet PGND sense point near the output-capacitor return, not
through the high-current switching return. Keep the VIN/input-capacitor and
SW/inductor/output-capacitor current loops compact; a new net name alone does
not control their physical paths. Lay out the buck-to-analogue return region so
the buck's pulsed current does not flow through quiet analogue copper.
The TPA3251's PVDD and 12 V VDD/GVDD returns use one local amplifier ground.
The 12 V branch takes its input from the buck's `17V3` net and returns it on
`GNDAMP`. The current schematic joins `PGND` to `GNDAMP` through R1 (0 Ω)
and `AGND` to `GNDAMP` through R2 (0 Ω). These parts will not be populated, so
the proposed schematic revision merges the three nets into `GND` and removes
R1/R2. Keep the amplifier return out of quiet analogue copper. Final 12 V
supply placement and return routing remain open.

The three output capacitors total 30 µF by nameplate value; their effective
capacitance at approximately 17.36 V bias is unverified. The output net remains
named `17V3`. The 12 V LDO is sourced from this rail; at the previous
120 mA amplifier-rail allocation its pass loss is approximately
`(17.36 V - 12 V) × 0.12 A ≈ 0.64 W`, before ground-current loss. The MP4541
may enter pulse-skip operation at light load, so assess rail ripple and
analogue noise at the actual idle and operating loads. These are design
checks, not claims of measured faults.

Manufacturer sources: [MP4541GN data sheet](https://www.monolithicpower.com/en/documentview/productdocument/index/version/2/document_type/Datasheet/lang/en/sku/MP4541GN/document_id/9688/),
[MPS exposed-pad guidance](https://forum.monolithicpower.com/t/mp4541-exposed-pad-connection/2823/3),
[SRN8040 data sheet](https://www.bourns.com/docs/product-datasheets/srn8040.pdf),
and [Samsung capacitor identity](https://product.samsungsem.com/mlcc/CL32A106KBJNNN.do).

### 1.2 NCP1117 12 V branch review (2026-10-06)

The placed `U1 = NCP1117ST12T3G` maps VIN/pin 3 to `17V3`, VSS/pin 1 to
`GNDAMP`, and VOUT/pin 2 and tab pad 4 to `12VAMP`. This matches onsemi's
pinout, including its tab-to-output connection. Verify all four pads in the
PCB netlist before layout; this closes the earlier schematic tab-net error.

The NCP1117 input maximum is 20 V. For assumed 1% R6/R10 resistors and
MPS's 0.985–1.015 V feedback-reference limits, the 17.36 V target spans about
16.78–17.96 V in steady-state tolerance. That leaves about 2.04 V to the
NCP1117 input limit at the high end; resistor tolerance is not specified in
the schematic, and startup/load transients still need to remain within 20 V.

The `XC6701DF02FR-G` 15 V output may be as high as 15.30 V. Torex's
25 °C voltage chart specifies maximum dropout of 0.17 V at 20 mA and
0.85 V at 100 mA for this output version. At the illustrative 16.78 V
minimum buck level, remaining margin is about 1.31 V at 20 mA or
0.63 V at 100 mA, before rail ripple and return-path drops. Establish the
actual analogue load and use its loaded headroom and thermal conditions;
the 20 mA case is promising, while 100 mA leaves little room.
Torex defines the published dropout point at a 2% output fall, so these
25 °C figures do not establish the onset of loss of regulation. The selected
buck supervisor threshold in [Power amplifier](POWER_AMPLIFIER.md) permits
analogue-rail droop during a buck fault; it does not guarantee RESET before
this 15 V LDO leaves regulation.

`C4` is a nominal 10 µF ceramic at the NCP1117 output, now paralleled with
`C19 = 470 µF` electrolytic and `C20 = 100 nF`. Onsemi requires at
least 4.7 µF *effective* output capacitance and a specified ESR stability
range (typically 33 mΩ to 2.2 Ω); the bank's effective capacitance under 12 V
bias and ESR have not been verified to satisfy those limits. Its input capacitor
`C3` is also nominally 10 µF. At 120 mA, the 0.64 W pass loss implies about
103 °C junction rise using the data sheet's 160 °C/W SOT-223 minimum-pad
reference, before ground-current loss. This is not the actual board's thermal
resistance, but demands a deliberate copper/thermal design or a lower-loss
regulator. The TPA3251 12 V VDD/GVDD feeds and local bypasses are now drawn;
their actual load and U1 stability/thermal behaviour remain unverified.

Manufacturer sources: [onsemi NCP1117 data sheet](https://www.onsemi.com/download/data-sheet/pdf/ncp1117-d.pdf)
and [Torex XC6701 data sheet](https://product.torexsemi.com/system/files/series/xc6701.pdf).

### 1.3 Locked 36 V supply: Mean Well RSP-200-36

Use the Mean Well `RSP-200-36`. Manufacturer data current at the review date:

| Characteristic | RSP-200-36 value | Design consequence |
| --- | ---: | --- |
| rated output | 36 V, 5.56 A, 200.16 W | continuous system input-power ceiling |
| output adjustment | 32.4–39.6 V | set to 36 V; adjustment is not design margin |
| voltage tolerance | ±1.0% | includes setup, line, and load regulation |
| line / load regulation | ±0.2% / ±0.5% | verify the as-built 36 V rail under load |
| ripple and noise | 220 mV peak-to-peak maximum | manufacturer method uses 20 MHz bandwidth, 300 mm twisted pair, and 0.1 µF + 47 µF termination |
| input | 88–264 V AC, 47–63 Hz | universal input; no voltage selector |
| AC current | 1.3 A typical at 230 V AC | basis for the 2 A time-lag appliance fuse |
| inrush | 40 A typical at 230 V AC | requires a time-lag fuse and cold-start testing |
| power factor | greater than 0.95 typical at 230 V AC/full load | active PFC is internal |
| efficiency | 90% typical | about 22 W supply loss at 200 W output |
| leakage current | less than 1 mA at 240 V AC | component value; final equipment still requires verification |
| setup / rise time | 1500 ms / 50 ms at 230 V AC/full load | amplifier mute/enable design must tolerate this |
| hold-up time | 8 ms typical at full load | do not assume ride-through beyond this |

The 200.16 W rating is adequate for the 140–150 W amplifier target. As a
conservative illustration, 150 W audio output at 90% amplifier efficiency
requires

```text
150 W / 0.90 = 167 W DC
```

before auxiliary loads, leaving approximately 33 W within the PSU's continuous
rating. This is a sizing check, not a measured amplifier-efficiency result.

Protection behaviour:

- overload at 105–135% of rated output power: hiccup mode, automatic recovery
  after the fault is removed;
- overvoltage at 41.4–48.6 V: output shutdown, requiring input power cycling to
  recover; and
- overtemperature: output shutdown with automatic recovery after cooling.

Do not treat the overload range as a guaranteed peak-power rating.

Cooling and environment:

- fanless free-air convection;
- specified working range: -30 to +70 °C, subject to the manufacturer's
  derating curve;
- full rated load is available to 45 °C in the documented horizontal
  orientation, followed by linear derating to approximately 50% at 70 °C;
- do not obstruct the perforations; the final enclosed installation must prove
  its own internal ambient and PSU temperature; and
- above 2000 m altitude, reduce maximum ambient by 3.5 °C per 1000 m.

Mechanical and terminal data:

- 215 × 115 × 30 mm, manufacturer tolerance ±1 mm, mass 0.72 kg;
- four M4 bottom mounting holes, maximum screw penetration 3 mm;
- four M4 side mounting holes, maximum screw penetration 5 mm;
- terminal assignment: 1 `AC/L`, 2 `AC/N`, 3 `FG`, 4–6 `-V`, 7–9 `+V`;
- M3.5 terminal screws, tightened to the Mean Well installation-manual value
  of 8–10 kgf·cm (approximately 0.78–0.98 N·m); and
- exact placement and convection clearance remain part of the mechanical
  layout, using the manufacturer's drawing rather than re-created dimensions.

Published approvals and EMC claims:

- UL 62368-1 and TÜV BS EN/EN 62368-1;
- DEKRA EN 61558-1 and EN/IEC 61558-2-16 for the 36 V model;
- EAC TP TC 004, CCC GB 4943.1, BSMI CNS 15598-1, AS/NZS 60950.1, and the
  applicable BIS approval listed by Mean Well;
- emissions to BS EN/EN 55032 Class B and BS EN/EN 61000-3-2/-3; and
- immunity to BS EN/EN 61000-4-2, -3, -4, -5, -6, -8, and -11 and EN 55035
  light-industrial level.

These are component approvals/claims, not certification of the completed
subwoofer. Mean Well's EMC result used a particular metal test plate and the
manufacturer explicitly requires the final equipment to be re-confirmed.

Primary sources:

- [Mean Well RSP-200 series specification](https://www.meanwell.com/Upload/PDF/RSP-200/RSP-200-spec.pdf)
- [Mean Well enclosed-supply installation manual](https://www.meanwell.com/Upload/PDF/Enclosed_Type_EN.pdf)
- [Mean Well RSP-200 approvals and declarations](https://www.meanwell.com/webaPP/Product/search.aspx?pdf=UlNQLTIwMCwzMjAtVUstZGVjLnBkZg%3D%3D&prod=RSP-200)

### 1.4 Mains inlet, switching, and appliance fuse

Locked inlet assembly:

- Schurter `DD11.0111.1111`, Mouser `693-DD11.0111.1111`;
- IEC C14 Class-I inlet, 10 A at 250 V AC;
- front screw mounting, suitable for panels up to 8 mm thick and therefore for
  the 6 mm aluminium plate;
- non-illuminated two-pole line switch;
- one-pole 5 × 20 mm fuseholder in line only;
- 4.8 × 0.8 mm quick-connect terminals;
- V-Lock provision and rear insulation cover; and
- use the supplier drawing/CAD as the cut-out authority. The present drawing
  gives a 47.1 × 28.1 mm nominal opening, 56 mm mounting-hole centres, and
  3.4 mm mounting holes.

Required separate fuse drawer:

- Schurter `4301.1407`, Mouser `693-4301.1407`;
- extra-safe, one-pole drawer for a 5 × 20 mm fuse.

Initial locked appliance fuse:

- Schurter SPT `0001.2507`;
- `T2AH250V`: 2 A, 250 V AC, time-lag, ceramic, 5 × 20 mm;
- 1.5 kA AC breaking capacity and typical melting I²t of 9.2 A²s; and
- verify repeated cold starts at the highest expected internal ambient. If it
  nuisance-opens, do not increase the rating until the measured startup event,
  fuse time-current curve, and wiring protection have been reviewed.

Mean Well includes an internal line fuse, but it is a component-protection
device. The accessible inlet fuse is retained to protect the appliance mains
wiring and to provide serviceable, installation-specific coordination.

Wire the inlet as follows:

```text
C14 L --> T2A fuse --> switch pole 1 --> RSP terminal 1 AC/L
C14 N -------------> switch pole 2 --> RSP terminal 2 AC/N
C14 PE --> short PE lead --> dedicated M4 plate stud
                                  |
                                  +--> aluminium plate
                                  |
                                  +--> separate PE lead --> RSP terminal 3 FG
```

The switch must open line and neutral. Protective earth is never switched or
fused.

No additional mains-input filter is fitted for Rev A. The RSP-200 already has
an internal EMI filter and PFC and carries a component-level Class-B emissions
claim. A second filter would add size, cost and earth-leakage capacitance
without guaranteeing system compliance. Reopen this decision only if final
equipment conducted/radiated-emissions or audible-noise testing shows a need.

Primary component sources:

- [Schurter DD11 data](https://www.schurter.com/en/datasheet/typ_dd11.pdf)
- [Mouser DD11.0111.1111 listing](https://www.mouser.co.uk/en/ProductDetail/Schurter/DD11.0111.1111)
- [Schurter fuse-drawer data](https://www.schurter.com/en/datasheet/typ_fusedrawer_2.pdf)
- [Schurter SPT fuse data](https://www.schurter.com/en/datasheet/typ_spt_5x20.pdf)

### 1.5 Internal mains wiring and access assumptions

- Use harmonised stranded copper appliance wire, 0.75 mm² minimum, rated
  300/500 V or better and for the expected internal temperature: brown line,
  blue neutral, green/yellow protective earth.
- Use correctly tooled, fully insulated 4.8 × 0.8 mm receptacles at the inlet.
  One conductor per receptacle; do not stack receptacles or improvise a
  two-wire crimp on the PE blade.
- Use crimped ferrules or terminals compatible with the RSP terminal block.
  No loose strands may enter a screw terminal.
- Keep the mains loom short, supported near each termination, protected from
  sharp plate edges, and physically segregated from DC, loudspeaker, and
  signal wiring. Cross other wiring only where unavoidable.
- Fit the inlet's rear cover and a Mean Well `TBC-09` cover to the RSP-200
  terminal strip. These guards must prevent finger, tool, loose-wire, and
  displaced-component contact with mains terminals.
- Removing the rear plate is a service operation: disconnect the IEC lead
  first. No mains terminals are user-accessible in normal use.
- Provide enough PE slack that protective earth is the last conductor stressed
  if the rear assembly is displaced.

## 2 Grounding and earthing

### 2.1 Objectives

- Maintain Class-I protective earthing.
- Keep Class-D switching currents out of analogue return paths.
- Avoid unintended chassis/signal-ground loops.
- Use deliberate branch returns rather than arbitrary shared wiring.
- Use solid local ground planes on each PCB; do not implement literal long-wire star grounding at high frequencies.

---

## 3 Protective earth and chassis

The exposed aluminium rear panel is protective-earthed.

```text
IEC PE
  |
short dedicated PE conductor
  |
M4 protective-earth stud --> aluminium rear plate
  |
separate dedicated PE conductor
  |
Mean Well terminal 3 FG / chassis
```

Requirements:

- Use a dedicated M4 machine screw through the 6 mm plate, with its threaded
  end inboard. M3 is electrically adequate but is not the selected mechanical
  baseline.
- The stud must be mechanically independent of PCB, PSU, and plate mounting.
- On the bare inner plate face use a serrated/internal-tooth washer and first
  nut to clamp the stud permanently. Fit the two PE ring terminals above that
  fixed joint, followed by a flat washer and an all-metal prevailing-torque
  locknut. Servicing a conductor must not loosen the stud-to-plate bond.
- Remove paint/coating at PE contact point.
- Clean/abrade the contact area immediately before assembly; after tightening,
  protect around but never between the conductive interfaces against
  corrosion.
- Use M4 ring terminals crimped with their specified tooling to 0.75 mm²
  green/yellow conductors.
- Mark the stud with the protective-earth symbol.
- Do not rely on heatsink contact, PCB screws, RCA connectors, or PSU mounting screws as the sole protective-earth path.

---

## 4 36 V distribution

The Mean Well PSU output is the primary DC branching point.

```text
Mean Well +V (three common terminals)
  |-- two proposed conductors --> TPA3251 amplifier-domain power entry
  +-- one proposed conductor  --> 36 V -> 17V3 buck converter

Mean Well -V (three common terminals)
  |-- two proposed conductors --> TPA3251 power-ground region
  +-- one proposed conductor  --> buck-converter input return
```

Requirements:

- Amplifier and buck currents must not share significant wiring impedance.
- The buck-fed 12 V amplifier rail also connects the PCB return regions;
  do not assume the PSU terminals are their only connection. Keep each
  outgoing feed close to its corresponding return and review the resulting
  parallel paths.
- Use suitably heavy conductors for the amplifier branch.
- TPA3251 PCB must use a compact, low-impedance ground plane rather than star traces.

Earlier candidate amplifier-branch connector (2026-10-06): Molex Micro-Fit+
`218216-0400` four-contact right-angle SMT header with mating
`226263-1043` 300 mm, 16 AWG, factory-terminated female-to-free-end cable.
That candidate assigned two contacts to +36 V and two to return; these are two electrical nets,
regardless of the RSP-200's three parallel screw terminals per net. At the
36 V/5.56 A PSU limit, each connector contact is individually rated above the
whole branch current, so safe operation does not rely on equal current sharing.
This is a procurement candidate, not an approved PCB footprint or harness:
confirm pin numbering, pad/anchor geometry, cable reach, wire-end termination,
strain support, and polarity marking during layout. This four-contact candidate
does not implement the newly proposed six-conductor arrangement; select a
suitable connector or connector set before layout. Keep the buck's separate
feed and return as shown above. Mouser UK listed both parts as in stock,
normally stocked, active, and MOQ 1 at the review date; recheck before order.

---

## 5 Superseded auxiliary-rail design and grounding

Sections 5.1 and 5.2 retain the earlier 15 V converter and two 12 V
post-regulator analysis for provenance. They do not define the current power
tree or its bill of materials. The separate-domain principle remains current;
the exact new branching and return junction await the complete schematic.

The 15 V buck output is the branching/reference point for the two 12 V rails.

```text
15 V buck
  |
  +--> 12V_AMP LDO
  |      |
  |      +--> TPA3251 VDD/GVDD
  |
  +--> 12V_ANA LDO
         |
         +--> analogue front end
```

Returns:

```text
buck output return
  |
  +--> 12V_AMP_GND
  |
  +--> 12V_ANA_GND
```

Requirements:

- `12V_AMP_GND` and `12V_ANA_GND` are separate nets/branches.
- Their intentional common point is the STH0548S15 output-return/reference
  region.
- Each electrical domain uses a solid local ground plane, whether the domains
  are implemented on separate PCBs or on one partitioned PCB.
- Do not route TPA3251 gate-drive or switching-current returns through analogue-ground wiring.

### 5.1 Previous 15 V converter: XP Power STH0548S15

Use the XP Power `STH0548S15` non-isolated switching-regulator module:

- nominal system input: 36 V from its separate RSP-200-36 branch;
- module input range: use the manufacturer's conservative published
  `21–72 V DC` range for this design;
- regulated output: 15 V;
- component rating: 400 mA and 6 W;
- project maximum total 15 V rail load: 250 mA and 3.75 W;
- SMD-10 package, approximately `19.5 × 11.8 × 5.0 mm`;
- no galvanic isolation; and
- remote on/off left open for normal enabled operation unless the final
  schematic identifies a specific need to control it.

The 250 mA project limit preserves current and thermal margin for component
tolerance and the TPA3251's typical-only VDD/GVDD current figures. It is the
combined input-current budget for the `12V_AMP` LDO, `12V_ANA` LDO, RESET
supervisor, VMID, and every other auxiliary load derived from 15 V. Do not use
the module's unused 150 mA component capability to add functions without
reopening this budget.

Implementation requirements from the
[STH05 data sheet](https://www.xppower.com/portals/0/pdfs/SF_STH05.pdf):

- fit a performance-critical generic 22 µF, 63 V minimum, ±20%, 105 °C SMD
  aluminium-electrolytic input capacitor at the converter pins; its 17.6 µF
  tolerance minimum exceeds the manufacturer's 10 µF requirement; 63 V is the
  preferred rating, while a 100 V substitute is acceptable if it meets the
  same footprint, ripple, lifetime, and damping requirements;
- measure a sample's ESR near the filter's 10–20 kHz resonance region and at
  100 kHz, then use those values in the final damping assessment; this is not
  the LM2937 output-capacitor stability test and no pass/fail ESR range is yet
  asserted;
- parallel it with the exact KEMET `C1206C104K1RAC7867` 100 nF, 100 V,
  ±10%, X7R, 1206 ceramic capacitor;
- keep total effective output capacitance within the specified 100 µF maximum;
- populate the manufacturer's external C-L-C EMI-filter arrangement in Rev A
  rather than treating the module-level Class-B claim as a completed-system
  result;
- use the exact Bourns `SRR7045-560M` 56 µH, ±20% shielded power inductor;
- keep the input filter, converter, and local capacitors close together with
  short current loops;
- do not route PCB tracks beneath the module; and
- place the module in the power region, away from the RCA inputs, VMID,
  crossover filter, and other high-impedance analogue nodes.

Use pin 9 as the 36 V branch input return and pin 7 as the output-side 15 V
reference/branching region. Because the converter is non-isolated, these are
electrically common inside the module; do not create an additional external
return path that bypasses the intended input/output current routing.

Implement the manufacturer's differential-mode input filter as two parallel
2.2 µF, 100 V, 1206 MLCCs from the incoming 36 V branch to its return, followed
by the series 56 µH inductor, followed by a second pair of parallel 2.2 µF,
100 V, 1206 MLCCs at the converter side. The two 4.4 µF banks are on opposite
sides of the inductor and therefore do not form one parallel 8.8 µF bank. With
an ideally stiff source, 56 µH and the converter-side 4.4 µF give a nominal
10.1 kHz pole; the inductor's ±20% tolerance moves that calculation to
approximately 9.26–11.3 kHz. The local 22 µF aluminium electrolytic materially
lowers the actual converter-side resonance, so final damping must be assessed
using the selected capacitors' effective capacitance and ESR, the inductor DCR,
and the source impedance.

The `SRR7045-560M` has 0.18 Ω maximum DCR, 1.30 A typical RMS-current rating,
0.80 A typical saturation current, and 9 MHz typical self-resonant frequency.
These provide ample margin over both the 250 mA project output-load limit and
the module's published 311 mA full-load input current at minimum input voltage.
Treat it as a specialised exact part.

Provisionally use four Würth Elektronik `885012208124` capacitors for the two
EMI-filter shunt banks. This is a performance-critical exact Rev-A selection:
2.2 µF, 100 V, ±10%, X7R, 1206. Würth's typical DC-bias curve indicates that
approximately 45% of nominal capacitance remains near 40 V, giving about
0.99 µF per capacitor and 1.98 µF per parallel pair. Using that estimate with
56 µH moves the stiff-source pole estimate from the nominal 10.1 kHz to about
15.1 kHz. This typical curve is a design estimate, not a guaranteed minimum.

The Samsung `CL31B225KCHSNNE` was considered as an alternative. Its modelling
tool indicates approximately 51.2% of nominal capacitance remains at 36.24 V,
or about 1.13 µF per capacitor. Even if that model-to-model difference is
real, it changes the calculated pole by only about 7% and ideal attenuation
well above resonance by about 1.1 dB. That is not material enough to justify
further catalogue optimisation before Rev-A measurement. Reopen the capacitor
choice only if the assembled filter shows unacceptable ripple or ringing.

Capacitor sources:

- [Würth Elektronik 885012208124 data sheet](https://www.we-online.com/components/products/datasheet/885012208124.pdf)
- [Samsung CL31B225KCHSNN component data](https://weblib.samsungsem.com/mlcc/mlcc-ec-data-sheet.do?partNumber=CL31B225KCHSNN)

The data sheet gives approximately 540 kHz switching at 20% load and about
50 kHz at 10% load. Check conducted ripple, magnetic/electric coupling, and
mixing with the TPA3251's then-assumed 450 kHz switching during prototype
validation. The current amplifier setting is nominal 600 kHz; this paragraph
records the superseded converter option. The
two 12 V post-regulators remain required; the converter does not directly feed
the analogue or amplifier housekeeping circuits.

### 5.2 Previous 12 V post-regulators and branch networks

Use one Texas Instruments `LM2937ESX-12/NOPB` on each branch. This is the
fixed-12 V, 500 mA DDPAK/TO-263 version; do not substitute the lower-current
SOT-223 `LM2937IMPX-12/NOPB`. The common part was selected because its typical
ripple-rejection plot remains useful through the STH0548S15's documented
50–540 kHz operating region, it has adequate voltage/current/thermal margin,
and it avoids a second regulator type. The graph is typical data measured on a
5 V version under different conditions, not a guaranteed 12 V minimum. The
12 V version's specified 10 Hz–100 kHz output noise is 360 µV RMS typical at a
5 mA load, so prototype rail and audio-output noise measurements remain the
acceptance evidence.

A mixed regulator scheme could reduce intrinsic `12V_ANA` noise, but it would
add another BOM line and layout pattern without solving a demonstrated problem.
The OPA167x stages have strong supply rejection, the analogue branch receives
additional RC attenuation, and the audio path is low-bandwidth. Rev A therefore
uses two LM2937s. Reopen the mixed-regulator option only if the assembled board
shows regulator-related noise or STH0548S15/TPA3251 mixing products that the
defined filtering and layout cannot reduce adequately.

Implement the 15 V output and two regulator inputs as follows:

```text
STH0548S15 pin 5
  |
  +-- 10 µF, 25 V SMD aluminium electrolytic
  |     || KEMET C1206C104K1RAC7867 100 nF to pin 7
  |
  +-- 0 Ω link (12V_AMP; reserve 3.3 Ω option)
  |     +-- KEMET EEV226M035S9DAA 22 µF aluminium electrolytic
  |           || KEMET C1206C104K1RAC7867 100 nF
  |     +-- LM2937ESX-12/NOPB
  |
  +-- 10 Ω, 1206, >=0.25 W (12V_ANA)
        +-- KEMET EEV226M035S9DAA 22 µF aluminium electrolytic
              || KEMET C1206C104K1RAC7867 100 nF
        +-- LM2937ESX-12/NOPB
```

Fit the amplifier link as 0 Ω for Rev A. A 3.3 Ω population option is retained
for measured-noise troubleshooting, but must not be fitted until RESET timing,
minimum 15 V rail voltage, and loaded LDO headroom have been rechecked. Fit the
10 Ω analogue resistor. With the nominal 22 µF downstream capacitance and
ignoring ESR initially, its one-pole corner is

```text
fc = 1 / (2 pi R C) = 1 / (2 pi x 10 ohm x 22 µF) = 723 Hz
```

The selected capacitor's listed 1 Ω impedance at 100 kHz and 20 °C limits the
high-frequency attenuation of the real 10 Ω RC network. Approximating that
impedance as ESR gives a pole near 658 Hz, a zero near 7.23 kHz, and a
high-frequency shelf of `1 / (10 + 1)`, or approximately -20.8 dB, before the
LDO's own rejection. This is still useful: applying the shelf conservatively
to the converter's specified 75 mV peak-to-peak ripple gives about 6.8 mV
peak-to-peak at the LDO input. These are model estimates because impedance
varies with frequency and temperature; assembled ripple measurement remains
the acceptance evidence.

At the 35 mA analogue branch budget the resistor drops 0.35 V and dissipates
12 mW. The nominal capacitance directly associated with the converter output
is 54.3 µF: 10 µF common, two 22 µF branch capacitors, and three 100 nF
capacitors. This remains below the module's 100 µF maximum; even the stated
positive component tolerances total only about 65.1 µF. Verify the final BOM
and every additional 15 V capacitor against that limit.

The power-tree capacitor selections use the project-wide generic/specialised
distinction:

| Function | Classification | Required selection |
| --- | --- | --- |
| STH0548S15 input bulk | performance-critical generic because its ESR contributes to filter damping | 22 µF, 63 V minimum and preferred, ±20%, 105 °C SMD aluminium electrolytic; 6.3 mm diameter × approximately 8 mm high can/land pattern; at least 100 mA ripple-current rating; measure ESR near 10–20 kHz and at 100 kHz and use it in the damping assessment; a 100 V substitute is acceptable if all requirements are met |
| STH0548S15 EMI-filter shunt banks | performance-critical; provisional exact Rev-A part | four Würth Elektronik `885012208124`, 2.2 µF, 100 V, ±10%, X7R, 1206 MLCCs, used as two parallel pairs; use approximately 0.99 µF each at 40 V for preliminary analysis and verify the assembled filter |
| 36 V-side high-frequency bypass | exact part for BOM consolidation | KEMET `C1206C104K1RAC7867`: 100 nF, 100 V, ±10%, X7R, 1206 |
| STH0548S15 output bulk | generic | 10 µF, 25 V minimum, ±20%, 105 °C SMD aluminium electrolytic; 5 mm diameter × approximately 5.8 mm high can/land pattern |
| STH0548S15 output and LM2937-input high-frequency bypasses | exact part for BOM consolidation | KEMET `C1206C104K1RAC7867`: 100 nF, 100 V, ±10%, X7R, 1206; one at the converter output and one directly at each LM2937 input |
| each LM2937 input reservoir | performance-critical exact part | KEMET `EEV226M035S9DAA`: 22 µF, 35 V, ±20%, 105 °C SMD aluminium electrolytic, 5 mm diameter × 5.65 mm maximum height, listed 1 Ω impedance at 100 kHz and 20 °C, 160 mA ripple-current rating at 100 kHz, and 2,000-hour life at 105 °C |
| each LM2937 output capacitor | performance-critical exact part | KEMET `EEV226M035S9DAA`; the same electrical and mechanical data apply; capacitance must remain at least 10 µF and measured ESR must remain between 0.01 Ω and 3 Ω over the project's operating-temperature range |
| 12 V load decoupling | generic | 100 nF, 50 V, ±10%, X7R, 0603 unless a load data sheet requires otherwise |

Use the same exact KEMET `EEV226M035S9DAA` at both LM2937 inputs and outputs.
Its listed 1 Ω impedance at 100 kHz and 20 °C is comfortably within the
LM2937's required 0.01–3 Ω output-capacitor ESR range; a lower ESR is not an
intrinsic improvement because the regulator also imposes a lower stability
limit. Before assembly approval, measure a representative sample's ESR at
100 kHz. Manufacturer data or further measurements must also establish that
capacitance remains at least 10 µF and ESR remains in range over the project's
actual operating-temperature range. Preserve capacitor polarity. Reopen the
selection only if those checks fail or Rev-A ripple/noise is unacceptable.

Use KEMET `C1206C104K1RAC7867` for all four 100 nF high-frequency bypass
positions in the auxiliary filter chain: the STH0548S15 input, its output, and
the two LM2937 inputs. Its 100 V rating and 1206 package are deliberately
overspecified on the 15 V nodes to consolidate the BOM. Yageo/KEMET's current
specification identifies `C1206C104K1RACTU`, with
`C1206C104K1RAC7800` as a packaging alias; treat those suffixes as the same
electrical component only after confirming the supplied termination and
packaging are compatible. This consolidation does not apply automatically to
distributed 12 V load decouplers, which remain generic 100 nF parts placed in
the package most appropriate to each load.

All generic capacitor substitutions are acceptable only when every property
in the table is met. Do not substitute the four exact KEMET capacitors without
repeating their capacitance, ESR, temperature, ripple, lifetime, mechanical,
and regulator-stability review. Confirm regulator stability on the assembled
PCB because distributed ceramic load bypasses appear in parallel with the
stability capacitor at high frequency.

The current allocation is:

| 15 V-derived load | Design allocation | Basis |
| --- | ---: | --- |
| TPA3251 VDD plus two PBTL gate-supply bridges | 120 mA | 90 mA published typical operating current plus 30 mA engineering allowance; TI gives no maximum |
| eight OPA167x channels, including VMID allowance and signal current | 35 mA | 22.4 mA maximum quiescent current plus 12.6 mA allowance |
| two LM2937 ground currents | 40 mA | 20 mA data-sheet maximum per regulator, conservatively applied outside its stated 500 mA test condition |
| TPS3842 and divider/pull-up overhead | <1 mA | supervisor itself is microampere-scale; allowance covers the passive network |
| **allocated total** | **196 mA maximum** | **54 mA remains inside the 250 mA project limit** |

The TPA3251 figures are typical-only, so 120 mA is a controlled design
allocation, not a guaranteed device maximum. Measure both branch currents on
the first assembled board and reopen the budget if either allocation is
exceeded.

The LM2937 data sheet guarantees dropout only at 50 mA and 500 mA, not around
the expected amplifier-branch current. Characterise one `LM2937ESX-12/NOPB`
sample at 25 °C and 50, 75, 100, 125, 150, 175, and 200 mA. At each current,
establish the regulated output at 15.0 V input, reduce input voltage slowly,
and record `VIN - VOUT` when `VOUT` has fallen 100 mV from that regulated
baseline. Treat this as sample characterisation rather than a guaranteed
production limit, and use the result when finalising the TPS3842 threshold.

For a deliberately pessimistic thermal check at 15.6 V, 40 °C ambient, full
allocated load, and the LM2937's 20 mA maximum ground current, the amplifier
regulator dissipates approximately

```text
PD = (15.6 V - 12 V) x 0.120 A + 15.6 V x 0.020 A = 0.744 W
```

Using TI's 41.8 °C/W JEDEC junction-to-ambient figure gives about 31 °C rise,
or 71 °C junction. The analogue regulator, after the 10 Ω drop, dissipates
approximately 0.42 W and reaches about 58 °C by the same deliberately
pessimistic method. Both are comfortably below the 125 °C operating limit,
but each DDPAK tab still needs a generous local copper heat-spreader; final PCB
thermal verification supersedes the JEDEC estimate.

Primary source:

- [Texas Instruments LM2937 data sheet](https://www.ti.com/lit/ds/symlink/lm2937.pdf)
- [KEMET EEV226M035S9DAA specification](https://search.kemet.com/download/specsheet/EEV226M035S9DAA)
- [KEMET C1206C104K1RACTU specification](https://search.kemet.com/component-documentation/download/specsheet/C1206C104K1RACTU)

---

## 6 Amplifier ground and rear plate

The aluminium rear plate acts as:

- exposed conductive chassis
- TPA3251 heatsink
- protective-earth bonded metalwork

The TPA3251 heatsink/PowerPAD arrangement requires the amplifier ground to be intentionally referenced to the rear plate.

```text
TPA3251 GNDAMP
  |
controlled low-impedance bond
  |
aluminium rear plate
  |
PE
```

Requirements:

- Use one intentional amplifier-ground-to-chassis bond.
- Locate this bond close to the TPA3251/heatsink region.
- Avoid additional unintended low-impedance GNDAMP-to-chassis connections elsewhere.
- Treat the Mean Well `-V` rail as earth-referenced once the completed amplifier/chassis bonding is installed.

---

## 7 Analogue ground

The analogue domain uses a dedicated quiet ground plane:

```text
AGND
  |
analogue-domain ground plane
  |
input buffers / summer / LPF / level / differential driver
```

Requirements:

- Keep analogue ground currents local to the analogue domain.
- Do not intentionally route Class-D or PSU switching currents through this plane.
- Connection to the wider DC return system occurs through the defined auxiliary-supply return path.
- Any future analogue-ground-to-chassis network must be deliberate and added only if prototype EMC/hum testing justifies it.

---

## 8 RCA inputs

Use chassis-isolated RCA connectors.

Requirements:

- RCA shells must not make direct electrical contact with the aluminium rear plate.
- Use insulated RCA sockets/bushes.
- Signal ground returns to the analogue domain only.
- Do not use the RCA mounting hardware as a chassis-ground connection.

Reason:

- Prevent a second signal-ground-to-PE connection through the rear panel.
- Avoid forming a loop between RCA shell/chassis and amplifier-ground/chassis bonds.

---

## 9 Grounding topology summary

The current partial schematic uses `GNDAMP`, `PGND`, and `AGND`, joined through
R1/R2 0 Ω links that are not intended to be populated. These links do not
represent a completed-board connection. The proposed revision uses one
electrical `GND` net and controls analogue, buck, and amplifier return paths by
placement and copper geometry. The six Mean Well output terminals are three
connections to each of its common +V and -V rails, not isolated outputs.
Separate amplifier and buck 36 V wire branches remain intended; their return
paths also connect on the PCB through the buck-fed 12 V amplifier rail and its
local decoupling. Do not claim a single physical ground junction or use the
TPA3251's internal ground connections as a PCB return conductor. Keep the
12 V amplifier return out of quiet analogue copper. The exact board-current
paths and connector assignment remain to be settled in layout.

---

## 10 PCB grounding rules

### 10.1 TPA3251 amplifier domain

- Use a solid, low-impedance ground plane.
- Keep PVDD decoupling loops extremely short.
- Keep bootstrap and switching-current loops compact.
- Minimise switching-node copper area.
- Keep output-filter current returns local.
- Do not use long star traces for high-frequency returns.
- Follow TI reference-layout guidance closely.

### 10.2 Analogue domain

- Use a continuous analogue-ground plane.
- Keep VMID distribution distinct from ground.
- Keep high-impedance nodes away from Class-D switching nodes and PSU magnetics.
- Connect the quiet analogue return region to the wider board return outside
  the buck's pulsed current paths.

### 10.3 Combined-PCB partition under grounding review

Rev A uses one four-layer PCB with physically partitioned analogue and
Class-D domains. A common schematic `GND` net is proposed; it does not require
uniform ground copper across the entire board.

Partition rules:

- Keep broad, low-impedance local return copper for the amplifier and a quiet
  analogue return region. Contain the buck's pulsed input and output loops near
  its capacitors and switch. Define any inter-region ground connections from
  complete supply-and-return loops, not from a literal single-point rule.
- Keep a placement and routing corridor between the analogue circuitry and
  switching nodes. Route the balanced audio pair together across it. Determine
  other crossings from the finished placement and supply/return loops; do not
  leave a signal or power trace crossing a reference-plane gap.
- Bring amplifier and buck 36 V feeds and returns from separate Mean Well
  terminal pairs. The PSU terminals share common rails, and the buck-fed 12 V
  amplifier branch also connects the returns on the PCB. Review parallel
  return paths rather than assuming the PSU is their sole meeting point.
- Put the TPA3251 input side at the corridor edge. Put its switching nodes,
  PVDD commutation loops, output inductors, and speaker connection on the far
  side, away from the analogue domain.
- Route the two audio conductors together, symmetrically, and without stubs.
  Terminate them into the TPA3251-side input network immediately after the
  crossing.
- AC-couple both conductors symmetrically at the TPA3251 side so the amplifier
  establishes its own input bias/common-mode voltage. Confirm the final input
  network when the differential-driver values are selected.
- Populate the symmetric 100 Ω/100 pF input networks specified in
  [Front end](FRONT_END.md). Reserve matched optional footprints for any
  additional RF/common-mode mitigation justified by prototype measurements;
  leave those additional positions unpopulated by default.
- Keep mounting hardware in the analogue domain electrically isolated from the
  protective-earthed aluminium plate. The single intended amplifier-ground to
  chassis bond remains near the TPA3251/heatsink region.

The corridor is a placement and field-control tool, not galvanic isolation.
Good Class-D loop layout and a continuous return reference beneath any
crossing are more important than a nominal corridor width.

### 10.4 Layer-count decision

Two layers are technically feasible: TI's TPA3251 evaluation module implements
the amplifier and local differential-input op amps on a 2-layer, 2-oz-copper
PCB. It would require disciplined use of broad copper pours, an unbroken local
amplifier-ground plane, and close adherence to the TI reference placement.
This feasibility basis is the official
[TPA3251EVM product page](https://www.ti.com/tool/TPA3251EVM),
[EVM user guide](https://www.ti.com/lit/pdf/SLAU751), and the
[TPA3251 layout guidance](https://www.ti.com/lit/ds/symlink/tpa3251.pdf).
This is supporting precedent only; a two-layer board is not a project fallback.

Four layers are locked for this project's combined Rev-A board because they
provide materially better implementation margin:

- a substantially less interrupted local ground plane for each domain;
- easier, lower-inductance access from decoupling and signal returns to their
  local planes;
- less competition between high-current routing and return continuity;
- better containment of fields and more routing freedom at the boundary; and
- a less fragile route to a quiet analogue section on the same substrate.

This choice reduces EMC, noise, and layout-rework risk. It does not imply that
a competent 2-layer implementation would necessarily sound worse or measure
worse in-band.

Provisional layer intent, subject to the exact fabricator and thermal stack:

- front outer layer: analogue components and amplifier parts best placed away
  from the plate, with broad high-current copper where appropriate;
- rear outer layer: the TPA3251, selected close decoupling/bootstrap and other
  support parts that fit the machined reliefs, with direct short pin connections;
- inner layers: keep a solid `GND` reference adjacent to the rear-mounted
  TPA3251 and a quiet `GND` region for front-side analogue circuitry; reserve
  the remaining area for supply distribution without severing critical
  return paths; and
- begin with approximately 35 µm (1 oz) copper on all four layers. Upgrade
  selected outer layers to approximately 70 µm (2 oz) only if actual route
  width, length, RMS current, voltage drop, heating, or fabrication constraints
  justify the extra cost. Confirm the fabricator's finished stack-up before
  routing.

The former requirement that every TPA3251 support part crosses the PCB is
superseded. Put the high-frequency local decoupling on the IC side where the
pin geometry and milled clearance permit. Where a loop must cross layers,
keep its outward and return transitions adjacent and use appropriate local
via groups. Apply the return-path and placement rules on both populated sides.

---

## 11 Locked grounding decisions

Treat the following as fixed unless prototype evidence requires revision:

- Rear aluminium plate is permanently protective-earthed.
- Mean Well FG/chassis is connected to PE.
- IEC inlet PE connects by one short conductor to the dedicated M4 plate stud;
  a separate conductor runs from that stud to RSP terminal 3 `FG`.
- Amplifier and buck receive separate 36 V feed/return branches from the Mean Well PSU.
- TPA3251 uses a solid local power-ground plane.
- Analogue circuitry uses a separate quiet ground plane.
- TPA3251 amplifier ground is intentionally bonded to the aluminium rear plate at one controlled point.
- RCA sockets are electrically isolated from the aluminium panel.
- No additional chassis/signal-ground bonds are permitted unless explicitly added after prototype testing.
- Protective-earth continuity must not depend on PCB mounting or signal connectors.
- Rev A uses one four-layer PCB with electrically partitioned analogue and
  amplifier domains. There is no two-layer fallback; four layers are a project
  robustness requirement, not a TPA3251 functional requirement.
