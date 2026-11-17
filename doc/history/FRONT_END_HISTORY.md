# Front-end design history

> **HISTORY — superseded alternatives and calculations.** The [current front-end authority](../FRONT_END.md) owns the selected circuit and prototype actions. The text below records historical proposals, not current instructions.

**2026-10-11 film reassessment (historical; substitution made 2026-10-13).** The
schematic labels the RCA coupling capacitors C1/C6 and the amplifier-input
coupling capacitors C11/C15; earlier references C25/C42 and C64/C65 in this
discussion predate the schematic renumbering (reference check 2026-10-12).
These were the four X7R
capacitors carrying bass-band signal. At nominal
2.2 µF, the magnitude of their reactance at 20 Hz is 3.62 kΩ. With a
low-impedance 3 V RMS RCA source, approximately 0.23 V RMS appears across
each RCA coupling capacitor (47 kΩ return plus 1 kΩ input series resistor).
For a 1.8 V RMS driver leg, approximately 0.27 V RMS appears across each
amplifier-input capacitor (nominal 24 kΩ input). These are illustrative
worst-clean-level calculations, not measured distortion; the actual voltage
increases if DC bias reduces the effective X7R capacitance. Film removes this
voltage-dependent-capacitance uncertainty, but no audible or measured
improvement has been established in this circuit. A 2.2 µF film part is a
reasonable pre-layout substitution if its footprint and rear-plate clearance
are acceptable. Polypropylene is not required solely for low distortion:
TI's AC-coupling comparison found no significant performance difference among
the film dielectrics it tested. Keep both amplifier-input legs the same value
and type, and verify the chosen part's voltage rating at the actual DC bias.
[TI capacitor distortion study](https://www.ti.com/lit/an/slyt796a/slyt796a.pdf).

**2026-10-11 input-value check (historical alternatives; C1/C6 remain 2.2 µF).**
Using the 47 kΩ bias resistor alone, 1.0 µF gives a 3.39 Hz pole and
0.123 dB capacitor-related loss at 20 Hz relative to the input's midband
gain; with a −10% film capacitor and −1% bias resistor, that loss is
0.154 dB. The separate 1 kΩ/47 kΩ midband divider loses about 0.18 dB
irrespective of capacitance. This is small, but a corner below 20 Hz does not
mean zero loss at 20 Hz. Defining a strict input-stage budget of 0.10 dB
at 20 Hz gives a maximum pole of 3.05 Hz. With the same tolerances, the
nominal capacitance must be at least 1.25 µF; 1.5 µF ±10% film gives
0.069 dB worst-case loss. At a looser 0.20 dB input-stage budget, 1.0 µF
±10% is sufficient. The existing 2.2 µF amplifier-input coupling adds
approximately 0.10 dB nominally at 20 Hz on each signal path, independent
of this choice. Do not count both RCA coupling capacitors as cascaded poles:
each source traverses only its own input capacitor before summing. The
1 kΩ RCA series resistor slightly lowers the input pole; the calculations
above omit it conservatively. The 2026-10-13 film selection retains 2.2 µF.

A Nichicon UWP 2.2 µF bipolar aluminium electrolytic remains an unselected
alternative. Of its two relevant ratings, prefer the
`UWP1V2R2MCL1GB` 35 V, 4 mm-diameter part over the
`UWP1H2R2MCL1GB` 50 V, 5 mm-diameter part: both are ±20%, 5.4 mm high,
rated for 1,000 hours at 85 °C, and have the same maximum 0.15 dissipation
factor and 10 µA leakage specification, so the larger voltage rating provides
no useful circuit benefit. Bipolar construction removes the start-up polarity
constraint of an ordinary polarised electrolytic, and 2.2 µF preserves the
nominal frequency response and settling times already calculated. Before
approval, compare 20–100 Hz distortion with a film reference and measure
leakage-induced DC shifts at both the 47 kΩ input nodes and the two nominal
24 kΩ TPA3251 inputs. Pair the two amplifier-input parts by measured
capacitance and leakage.

Panasonic `EEE-1VA2R2NR` is a technically lower-leakage bipolar SMD
alternative: its maximum leakage is 6 µA rather than 10 µA, although its
maximum dissipation factor is higher at 0.24. A 2026-09-23 Mouser UK check
with `In Stock`, `Normally Stocked`, and `Active` all selected retained the
part and showed 20,607 in stock, a minimum order of one, and a one-off price
of £0.353. Do not select it as the new-design default, however: Panasonic's
own current product page marks it `NRFND`. Treat it only as a stocked
contingency unless Panasonic restores a new-design lifecycle status or an
active successor with the same electrical advantage becomes available.

Assess the assembled low-frequency response as part of normal prototype
validation. The selected Panasonic film part has a distinct through-hole
pattern; verify its 7.5 mm pitch and physical clearance on the PCB.



### 4.1 Solder-lug alternatives and resistance scaling, 31 October 2026

The user accepted the present 20 kΩ `PDB182-K420K-203B` PC-pin terminals
on 31 October 2026. The following comparison records why changing resistance
would also affect the filter; a resistance change is possible **only with two gangs that vary
together approximately linearly**. The current `rev0` schematic, PCB and
fabrication archive retain 13.7 kΩ arms and three 82 nF capacitors; the
alternatives below are not a selected circuit revision.

For matched gangs, write each arm as `R = R_FIXED + R_POT`. With
`C_FEEDBACK = 2 C_SHUNT`, the unity-gain Sallen-Key equations above reduce to
`f0 = 1/(2π R sqrt(C_FEEDBACK C_SHUNT))` and `Q = 0.707`.
Increasing either arm resistance lowers the frequency. Changing the pot
resistance alone therefore changes the *low* endpoint while the high endpoint
stays set by `R_FIXED`. To retain a 100:40 = 2.5:1 span,
`(R_FIXED + R_POT_MAX)/R_FIXED ≈ 2.5`, so
`R_FIXED ≈ R_POT_MAX/1.5`. Keeping the high endpoint near 100 Hz then requires
capacitors to scale inversely with that fixed resistance, while preserving
their 2:1 ratio to retain Butterworth Q.

| Hypothetical matched linear dual pot | Current 13.7 kΩ / 82 nF / 164 nF gives | Approximate retune for 40–100 Hz | Retuned nominal endpoints |
| --- | --- | --- | --- |
| 10 kΩ | 57.9–100.2 Hz | 6.8 kΩ in each fixed arm; 164 nF shunt, 328 nF feedback | 40.8–100.9 Hz |
| 20 kΩ current | 40.7–100.2 Hz | 13.7 kΩ; 82 nF shunt, 164 nF feedback | unchanged |
| 50 kΩ | 21.5–100.2 Hz | 34.0 kΩ in each fixed arm; 33 nF shunt, 66 nF feedback | 40.6–100.3 Hz |

The 10 kΩ retune could use `2 × 82 nF` in the shunt and `4 × 82 nF` in
feedback, versus the present three footprints total. The 50 kΩ retune needs
smaller capacitors; Panasonic lists 33 nF 50 V PPS in a different package from
the placed 82 nF part. Neither retune is a drop-in component swap on the
released board. Matching the gangs remains important: the general equation
above shows that unequal arms reduce Q below 0.707 as well as moving f0.
[Panasonic ECHU(X) catalogue](https://industrial.panasonic.com/cdbs/www-data/pdf/RDI0000/ABD0000C173.pdf).

A genuine matched-linear 50 kΩ pot could instead be shunted across each
variable gang with about 33.3 kΩ: `50 kΩ || 33.3 kΩ ≈ 20 kΩ` at its maximum.
This nominally preserves the present endpoints and capacitors, but compresses
the frequency scale: halfway through rotation the filter would be about 49 Hz,
versus about 58 Hz for the current 20 kΩ linear control. It needs two matched
external resistors and still requires gang and wiring checks. This is an
exploratory harness option, not a replacement decision.

The two Mouser numbers raised by the user,
[10 kΩ `652-PDB182-GTRB2-103`](https://www.mouser.co.uk/en/ProductDetail/Bourns/PDB182-GTRB2-103MN)
and [50 kΩ `652-PDB182-GTRB2-503`](https://www.mouser.jp/en/ProductDetail/Bourns/PDB182-GTRB2-503MN),
resolve to manufacturer variants ending **`MN`**. Bourns calls the GTRB2 a
blend/balance guitar control with a centre detent: its M gang changes over the
first half of rotation and then stays constant, while its N gang stays constant
over the first half and changes over the second. They are **not matched linear
dual gangs**, despite the catalogue's generic `Linear` attribute. In the
present wiper-to-end rheostat wiring, one filter arm moves in each half-turn;
the response would rise towards the centre and fall again, with Q varying.
For illustration with unchanged 13.7 kΩ/82 nF/164 nF parts, the 50 kΩ MN
option gives approximately `f0 = 46.5 Hz, Q = 0.54` at either end and
`f0 = 100.2 Hz, Q = 0.707` at centre. Do not substitute either GTRB2 part for
the current control. [Bourns GTRB datasheet](https://www.bourns.com/docs/product-datasheets/pdb182-gtrb.pdf),
[Bourns blend/balance application note](https://www.bourns.com/docs/technical-documents/technical-library/sensors-controls/application-notes/Bourns_PDB182_Blend-Balance_Guitar_Pots_AppNote.pdf).



### 6.1 Dailywell polarity-switch candidate, 31 October 2026

Mouser `118-1MD1T2B3M1QES` is Dailywell `1MD1T2B3M1QES`, a maintained
two-position DPDT panel toggle with six solder lugs. The manufacturer's 1M
series drawing identifies `1MD1` as ON–ON, `T2` as the short actuator, `B3`
as a 7.10 mm threaded 1/4-40 UNS bushing, `M1` as solder lugs and `Q` as
silver-plated contacts/terminals. The 1M series is rated −40 to +85 °C.
This was the first **functional candidate, not a selected switch**; the
gold-contact E-Switch in §6.2 has since been selected.
[Dailywell 1M series datasheet](https://datasheet.lcsc.com/lcsc/2304140030_Dailywell-1M31T1B1M1QES-5_C545198.pdf),
[Mouser listing](https://www.mouser.co.uk/ProductDetail/Dailywell/1MD1T2B3M1QES).

The published contact table gives common terminals 2 and 5. One position
closes 2–3 and 5–6; the other closes 2–1 and 5–4. A proposed four-wire
cross-over harness connects J3 pin 3 (`INPUT_A` return) to 2, pin 4
(`INPUT_B` return) to 5, J3 pin 1 (`VPLUS`) to both 3 and 4, and J3 pin 2
(`VMINUS`) to both 1 and 6. The first switch position then passes the legs
straight; the second swaps them. These are schematic terminal numbers, not
an established front-panel lever direction: check continuity and label the
actual part after mounting.

The switch is before the two 2.2 µF input coupling capacitors, so its contacts
sit at approximately 7.5 V common-mode potential but carry essentially no
steady DC current.
At a representative 1.2 V RMS signal per leg and nominal 24 kΩ amplifier
input, the audio current is only about `1.2/24000 ≈ 50 µA RMS`. The specified
initial 10 mΩ contact resistance would have negligible signal loss; the
question is whether silver contacts remain consistently conductive at such
low current after storage and use. Dailywell specifies `Q` for power contacts
and recommends gold for precision, low-level circuits because it resists
oxidation. No minimum reliable load or low-current contact-life guarantee was
found for this silver variant. A gold-contact ON–ON DPDT with solder lugs is
preferable for a repeatable build; this candidate could be tried in a
prototype if the contact behaviour is checked in the assembled signal path.
[Dailywell contact-material guidance](https://www.dailywell.com.tw/en/faq/Dailywell-FAQ-02.html).

The 7.10 mm bushing cannot clamp the full 12 mm rear plywood. A local recess
must leave enough exposed thread for the supplied nut and lockwasher, with
wood strength and rear lug/harness clearance checked before drilling. The
[mechanical authority](../MECHANICAL.md#3-rear-panel-structure) owns that fit.

