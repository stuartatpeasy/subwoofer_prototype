# Active Subwoofer Project

## 1 Objective

Design and build a compact sealed active subwoofer for a 20–30 m³ room, intended to support sealed two-way mains below approximately 60 Hz.

Primary constraints:

- music-oriented rather than extreme home-cinema SPL
- compact cabinet
- 390 mm cubic external cabinet with a sealed 20.0 L front acoustic chamber and
  separate ventilated rear electronics chamber
- analogue signal path
- no microcontroller or firmware
- no forced-air cooling
- no custom mains PSU
- CNC-relieved rear plate allowing selected components and through-hole leads on
  the plate-facing side of the amplifier PCB
- one four-layer PCB with physically controlled analogue and power regions
- engineering-led, measurable design

## 2 Documentation index

Start with the smallest document that answers the question. Read the system
specification first only when a decision could affect more than one subsystem.

| Question | Document | Scope |
| --- | --- | --- |
| What is fixed, provisional, or still to be selected? | [System specification](doc/SPECIFICATION.md) | System requirements, locked decisions, driver, cabinet, amplifier, and selected PSU |
| How is the input signal conditioned and filtered? | [Analogue front end](doc/FRONT_END.md) | RCA inputs, mono summing, variable low-pass filter, level, polarity, and differential drive |
| How is the loudspeaker driven? | [Power amplifier](doc/POWER_AMPLIFIER.md) | TPA3251 PBTL stage, output filter, Zobel network, passives, and layout constraints |
| How are the rails, returns, chassis, and protective earth arranged? | [Power and grounding](doc/POWER_AND_GROUNDING.md) | Power tree, DC distribution, grounding domains, chassis bonding, RCA isolation, and PCB grounding |
| What constrains the cabinet, PCB, and rear plate? | [Mechanical design](doc/MECHANICAL.md) | PCB clearance, aluminium plate, thermal interface, and rear-panel structure |
| What heat load must passive cooling handle? | [Thermal design](doc/THERMAL.md) | Present thermal assumptions and cooling requirement |
| What must the prototype prove? | [Prototype validation](doc/VALIDATION.md) | Electrical, thermal, and acoustic measurements |
| How should DipTrace schematic and PCB data be exposed or inspected? | [DipTrace data and tooling](doc/DIPTRACE.md) | Canonical partial schematic XML, shared Hub SDK route, read-only inspection workflow, and future parser/plugin gates |
| Which shared resources, environment facts, or general procedures apply? | [Hub index](../Hub/README.md) | Open only the relevant Hub topic; retain this project's design and evidence here |
| How should a schematic review be run and reported? | [Shared Hub index](../Hub/README.md) | Open its schematic-review procedure; use this project's saved schematic and current design authorities as the review inputs |
| What work remains? | [Action list](doc/TODO.md) | Ordered design, construction, and validation tasks |
| How should the documentation itself be reviewed or consolidated? | [Documentation review procedure](doc/DOCUMENTATION_REVIEW.md) | Targeted and comprehensive review modes, preservation rules, validation, and Git gates |

## 3 Suggested reading routes

- **System-level decision:** this README, then the
  [system specification](doc/SPECIFICATION.md), followed by only the affected
  subsystem document.
- **Analogue or crossover question:** [analogue front end](doc/FRONT_END.md),
  then the electrical checks in [prototype validation](doc/VALIDATION.md).
- **Class-D or output-network question:**
  [power amplifier](doc/POWER_AMPLIFIER.md), with the relevant supply and
  return constraints in [power and grounding](doc/POWER_AND_GROUNDING.md).
- **Cabinet, rear-panel, or cooling question:**
  [mechanical design](doc/MECHANICAL.md),
  [thermal design](doc/THERMAL.md), then the thermal and acoustic checks in
  [prototype validation](doc/VALIDATION.md).
- **DipTrace schematic or PCB inspection:** [DipTrace data and
  tooling](doc/DIPTRACE.md), then only the affected electrical, grounding, or
  mechanical authority. Load only the shared Hub SDK files selected by that
  route.
- **Schematic review:** whenever asked to review this project's schematic,
  open the [shared Hub index](../Hub/README.md) and follow its schematic-review
  procedure. Then use the DipTrace inspection route above and the affected
  project authorities. Report numbered findings with severity and verification
  state.
- **Shared context:** for tools, suppliers, the listening room, or general
  procedures, open the [Hub index](../Hub/README.md), then only the topic needed
  alongside this project's affected authority. Record project-specific
  decisions and measurements here; update the Hub for reusable new facts.
- **Planning question:** [action list](doc/TODO.md), using the
  [system specification](doc/SPECIFICATION.md) to distinguish locked decisions
  from provisional selections.

## 4 Document status conventions

- **Locked** means do not revisit without measured or simulated evidence.
- **Initial**, **candidate**, **preferred**, **approximately**, and **expected**
  identify values or choices that still require confirmation.
- A design statement is not a validation result. Measured results should be
  added to [prototype validation](doc/VALIDATION.md) as they become available.
