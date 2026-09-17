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
