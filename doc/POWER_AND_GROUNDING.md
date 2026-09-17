# Power and grounding

## 1 Power architecture

```text
230 V AC
  |
36 V SMPS
  |
  +--> TPA3251 PVDD
  |
  +--> ~15 V buck
         |
         +--> 12 V AMP LDO
         |      |
         |      +--> TPA3251 VDD/GVDD
         |
         +--> low-noise 12 V ANA LDO
                |
                +--> analogue front end
                |
                +--> buffered VMID ≈ 6 V
```

Requirements:

- `12V_AMP` and `12V_ANA` are separate nets
- deliberate grounding/star connection
- analogue rail should use high-PSRR low-noise post-regulation
- LT3045-class device acceptable for `12V_ANA`
- conventional low-noise LDO acceptable for `12V_AMP`

---

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
  +--> dedicated short PE conductor --> aluminium rear plate
  |
  +--> Mean Well FG/chassis terminal
```

Requirements:

- PE bond to rear plate must be mechanically independent of PCB mounting.
- Use dedicated chassis stud/bolt.
- Use ring terminal.
- Remove paint/coating at PE contact point.
- Use serrated/star washer or equivalent to bite into bare aluminium.
- Use locking hardware.
- Use appropriately sized green/yellow PE conductor.
- Do not rely on heatsink contact, PCB screws, RCA connectors, or PSU mounting screws as the sole protective-earth path.

---

## 4 36 V distribution

The Mean Well PSU output is the primary DC branching point.

```text
Mean Well +V
  |
  +--> dedicated heavy feed --> TPA3251 amplifier PCB
  |
  +--> separate feed --> 36 V -> 15 V buck converter

Mean Well -V
  |
  +--> dedicated heavy return --> TPA3251 power-ground plane
  |
  +--> separate return --> buck-converter input return
```

Requirements:

- Amplifier and buck currents must not share significant wiring impedance.
- Branches should meet only at, or immediately adjacent to, the Mean Well output terminals.
- Use suitably heavy conductors for the amplifier branch.
- TPA3251 PCB must use a compact, low-impedance ground plane rather than star traces.

---

## 5 Auxiliary-rail grounding

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
- Their intentional common point is the buck-output/reference region.
- Each PCB/domain uses a solid local ground plane.
- Do not route TPA3251 gate-drive or switching-current returns through analogue-ground wiring.

---

## 6 Amplifier ground and rear plate

The aluminium rear plate acts as:

- exposed conductive chassis
- TPA3251 heatsink
- protective-earth bonded metalwork

The TPA3251 heatsink/PowerPAD arrangement requires the amplifier ground to be intentionally referenced to the rear plate.

```text
TPA3251 AMP_GND
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
- Avoid additional unintended low-impedance AMP_GND-to-chassis connections elsewhere.
- Treat the Mean Well `-V` rail as earth-referenced once the completed amplifier/chassis bonding is installed.

---

## 7 Analogue ground

The analogue PCB uses a dedicated quiet ground plane:

```text
12V_ANA_GND
  |
analogue PCB ground plane
  |
input buffers / summer / LPF / level / differential driver
```

Requirements:

- Keep analogue ground currents local to the analogue board.
- Do not intentionally route Class-D or PSU switching currents through this plane.
- Connection to the wider DC return system occurs through the defined auxiliary-supply return path.
- Any future analogue-ground-to-chassis network must be deliberate and added only if prototype EMC/hum testing justifies it.

---

## 8 RCA inputs

Use chassis-isolated RCA connectors.

Requirements:

- RCA shells must not make direct electrical contact with the aluminium rear plate.
- Use insulated RCA sockets/bushes.
- Signal ground returns to the analogue PCB only.
- Do not use the RCA mounting hardware as a chassis-ground connection.

Reason:

- Prevent a second signal-ground-to-PE connection through the rear panel.
- Avoid forming a loop between RCA shell/chassis and amplifier-ground/chassis bonds.

---

## 9 Grounding topology summary

```text
                         PROTECTIVE EARTH
                               |
                    dedicated chassis stud
                               |
                    aluminium rear plate
                               |
                   controlled AMP_GND bond
                               |
                         Mean Well -V
                        /             \
                       /               \
              AMP power return      buck return
                    |                    |
              TPA3251 ground            |
                                         |
                                  15 V buck output
                                   /             \
                                  /               \
                         12V_AMP_GND          12V_ANA_GND
                              |                    |
                        TPA housekeeping      analogue ground
                                                   |
                                            insulated RCAs
```

---

## 10 PCB grounding rules

### 10.1 TPA3251 amplifier PCB

- Use a solid, low-impedance ground plane.
- Keep PVDD decoupling loops extremely short.
- Keep bootstrap and switching-current loops compact.
- Minimise switching-node copper area.
- Keep output-filter current returns local.
- Do not use long star traces for high-frequency returns.
- Follow TI reference-layout guidance closely.

### 10.2 Analogue PCB

- Use a continuous analogue-ground plane.
- Keep VMID distribution distinct from ground.
- Keep high-impedance nodes away from Class-D switching nodes and PSU magnetics.
- Connect to `12V_ANA_GND` at the intended supply-entry point.

---

## 11 Locked grounding decisions

Treat the following as fixed unless prototype evidence requires revision:

- Rear aluminium plate is permanently protective-earthed.
- Mean Well FG/chassis is connected to PE.
- Amplifier and buck receive separate 36 V feed/return branches from the Mean Well PSU.
- `12V_AMP` and `12V_ANA` have separate return branches meeting at the buck-output/reference region.
- TPA3251 uses a solid local power-ground plane.
- Analogue circuitry uses a separate quiet ground plane.
- TPA3251 amplifier ground is intentionally bonded to the aluminium rear plate at one controlled point.
- RCA sockets are electrically isolated from the aluminium panel.
- No additional chassis/signal-ground bonds are permitted unless explicitly added after prototype testing.
- Protective-earth continuity must not depend on PCB mounting or signal connectors.
