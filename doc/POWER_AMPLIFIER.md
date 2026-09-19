# Power amplifier

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
- on the combined PCB, face the TPA3251 input pins toward the copper-free
  analogue/power corridor and keep switching nodes and output inductors on the
  opposite side
- use the four-layer partition and layer intent defined in
  [Power and grounding](POWER_AND_GROUNDING.md); TI's 2-layer EVM establishes
  device feasibility, but two layers are not a project fallback

### 1.1 Rear-mounted IC and front-side support components

The TPA3251 is the only rear-side component. All decoupling, bootstrap, input,
mode, protection, output-filter, and bulk components are on the front side.
Consequently, all electrical paths between the IC and those parts cross the PCB.

Layout requirements:

- mirror each critical front-side part or pin-group network as closely as
  practical over its corresponding rear-side IC pins;
- use a dedicated local via group at each PVDD/GND pin cluster rather than a
  shared remote via farm;
- use broad rear-side copper from the paralleled PVDD, ground, and output pins
  into their via groups, then broad front/inner-layer copper onward;
- keep each bootstrap capacitor's two via transitions adjacent and its complete
  BST-to-capacitor-to-OUT loop extremely small;
- keep AVDD, DVDD, GVDD, VBG, VDD, C_START, and other local bypass loops short,
  with their signal and return vias placed as a pair;
- preserve symmetry through the via transitions for the differential input;
  and
- determine via drill, finished plating, count, and pad geometry from both
  current capacity and high-frequency inductance. Do not size the arrays from
  DC ampacity alone.

This is a deliberate departure from TI's preferred same-side, direct PVDD
decoupling connection. Four layers, closely placed parallel vias, and direct
front-to-rear component mirroring are therefore part of the implementation,
not optional layout refinement. Via-in-pad or filled/capped vias may help at
the densest nodes, but are not assumed until the fabricator process is chosen.

### 1.2 Protection, fault response, and RESET control

Use the TPA3251's internal undervoltage, overcurrent, short-circuit, and thermal
protection. Supply undervoltage may recover automatically. A persistent
overload or overtemperature shutdown may remain latched until the user switches
the complete subwoofer off and on. Do not add an automatic fault-retry circuit.
The exact `OC_ADJ` resistor, CB3C threshold, and associated surrounding
passives remain to be selected with the final PBTL implementation.

No normally visible fault LED is required. Provide accessible SMD diagnostic
test points for `FAULT` and `CLIP_OTW`; these signals are for prototype and
service diagnosis rather than normal user indication.

Use the Texas Instruments `TPS3842A011DRLR` analogue undervoltage supervisor
to control `RESET` without firmware. This is the adjustable 0.7 V-threshold,
1%-hysteresis, active-low open-drain variant in the six-pin SOT-5X3 package.
Its exposed leads have 0.50 mm pitch, which is the project's accepted minimum
for hand assembly. The device is powered from and monitors the nominal 15 V
buck output:

- monitor the nominal 15 V buck output so decay can be detected while both
  regulated 12 V rails remain valid;
- hold `RESET` low for at least 400 ms after PVDD is applied, as recommended by
  TI;
- release `RESET` only after the amplifier and analogue supplies have settled;
- assert `RESET` promptly when the monitored rail decays, before the analogue
  front end or TPA3251 gate-drive supply leaves regulation; and
- verify the complete power-up and power-down sequence by measuring the
  loudspeaker-output transient, not merely the RESET waveform.

Implementation baseline:

- fit at least 0.1 µF directly between supervisor `VDD` and ground;
- use the external SENSE divider to set a provisional falling threshold near
  13.9 V; the exact resistors remain open until the planned LM2937 sample
  dropout characterisation and the first board establish the loaded `12V_AMP`
  dropout and minimum 15 V rail voltage;
- leave `CTS` open for the fastest undervoltage assertion, subject to final
  noise testing; an optional local SENSE capacitor may be used if required;
- use `CTR` to guarantee at least 400 ms reset-release delay at component and
  supervisor timing extremes; 270 nF ±10% is the current design seed, giving
  approximately 0.49–1.10 s from the data-sheet limits; and
- pull the open-drain RESET output to a TPA3251-safe logic voltage. Do not load
  the TPA3251 `DVDD` reference output to obtain that pull-up voltage.

The earlier 182 kΩ over 10.0 kΩ seed is rejected. Its nominal 13.44 V falling
threshold can leave only 0.84 V across a worst-high 12.6 V LM2937 output, even
before PCB distribution loss, while the regulator guarantees dropout only at
50 mA (250 mV maximum) and 500 mA (1 V maximum), not at the 120 mA project
allocation. A lower-resistance 47.0 kΩ over 2.49 kΩ, both 0.1%, is the current
calculation seed:

```text
0.700 V x (1 + 47.0 kΩ / 2.49 kΩ) = 13.91 V nominal
```

This is intentionally not yet a locked divider. Worst-case TPS3842 threshold,
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
- suitable for 450 kHz operation

Prototype validation required:

- idle temperature
- sustained-load temperature
- contribution to idle PVDD current

## 3 Output capacitors

Reference target:

- approximately 680 nF per filter position

Constraints:

- SMD only
- through-hole film prohibited
- 1.2 mm underside PCB-to-aluminium clearance

Preferred implementation:

- X7R MLCC
- 100 V
- larger package preferred
- parallel parts acceptable/preferred

Example:

```text
3 × 220 nF, 100 V, X7R
```

Nominal total:

```text
660 nF
```

Requirements:

- check manufacturer DC-bias curves
- avoid Y5V/Z5U
- ensure acceptable AC loss at PWM frequency

## 4 Zobel/output damping network

Reference resistor:

- 3.3 Ω

Requirements:

- non-inductive
- SMD
- approximately 1–2 W class
- 1206/2010/2512 depending selected series

Prototype validation:

- temperature at idle
- temperature under sustained high output

## 5 General amplifier-board passives

### 5.1 Resistors

Default:

- SMD only
- 1%
- 0805 preferred
- approximately 125 mW minimum

Exceptions:

- precision signal networks
- Zobel/power resistors

### 5.2 Ceramics

Use voltage rating appropriate to node.

Guideline:

- 12 V rails: 16–25 V X7R
- bootstrap: 50–100 V
- PVDD bypass: 50–63 V minimum
- output filter: approximately 100 V X7R
- use C0G/NP0 for small precision/HF values where appropriate

Do not blindly use 100 V parts everywhere.

### 5.3 Bulk electrolytics

- SMD aluminium electrolytic
- 63 V preferred for 36 V PVDD
- low ESR
- suitable ripple-current rating
- nominal 470 µF reference positions
