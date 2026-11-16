# Active Subwoofer Project

The saved schematic, four-layer PCB and fabrication archive form the `rev0`
bare-board prototype release. The release identity and remaining order-preview
gate are in [PCB layout review](doc/PCB_LAYOUT.md). Enclosure, harness,
assembly and measured electrical/thermal performance remain prototype work.
The [13 November system order review](doc/REV0_ORDER_REVIEW.md) records the
PCB/P01-spreader fit evidence and separate pre-payment and dry-fit gates.
The 140–150 W clean subwoofer output target is bounded peak capability;
continuous output at that level is not required. The selected 200 W PSU retains
headroom for those peaks. [Thermal design](doc/THERMAL.md) owns the sustained
heat screen and the rear-spreader assessment.
The current enclosure DAE has the locked 300 × 470 × 320 mm structural
cabinet, a rear perimeter brace, vent and rear-panel fasteners, ash
corner legs and edge bumpers, eight M4 driver screws with threaded inserts,
and a separate insulating FR-4 control panel.
The extra 10 mm depth serves the electronics compartment; decorative ash lies
outside the bare structural envelope. The PCB/plate stack, protective-earth
hardware, mains guards and harness, assembled cooling and accessible
temperatures remain open.
[Mechanical design](doc/MECHANICAL.md) owns the fit and outlet.

## 1 Objective

Design and build a compact sealed active subwoofer for a 20–30 m³ room, intended to support sealed two-way mains below approximately 60 Hz.

Primary constraints:

- music-oriented rather than extreme home-cinema SPL
- compact cabinet
- 300 × 470 × 320 mm nominal bare-cabinet outer envelope, with a downward-
  firing driver, sloped acoustic partition, 20.0 L net sealed acoustic target,
  and separate naturally ventilated electronics chamber; decorative trim may
  extend beyond the bare envelope
- analogue signal path
- no microcontroller or firmware
- no forced-air cooling
- no custom mains PSU
- CNC-relieved rear plate allowing selected components and through-hole leads on
  the plate-facing side of the amplifier PCB
- the rear panel alone uses 12 mm plywood and carries all user controls and
  external connectors; other structural plywood thicknesses remain as specified
- the aluminium plate remains the amplifier heat spreader, PCB mount and
  protective-earth bond
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
| What electrical parts and harnesses are needed outside the PCB schematic? | [Off-board electrical BOM](doc/OFFBOARD_ELECTRICAL_BOM.md) | External parts, connector mates, wire and purchasing/fit gates |
| Which fasteners are modelled and which Boltworld SKUs need checking? | [Fastener BOM](doc/FASTENER_BOM.md) | Counted DAE instances, candidate SKUs and outstanding procurement checks |
| Where are the SketchUp-compatible component models? | [3D model catalogue](doc/3d_models/README.md) | Project selections and fit notes; reusable component models and generation records are in the Hub library |
| What heat load must passive cooling handle? | [Thermal design](doc/THERMAL.md) | Present thermal assumptions and cooling requirement |
| What must the prototype prove? | [Prototype validation](doc/VALIDATION.md) | Electrical, thermal, and acoustic measurements |
| How should DipTrace schematic and PCB data be exposed or inspected? | [DipTrace data and tooling](doc/DIPTRACE.md) | Canonical partial schematic XML, shared Hub SDK route, read-only inspection workflow, and future parser/plugin gates |
| What does the current routed PCB review find? | [PCB layout review](doc/PCB_LAYOUT.md) | Saved four-layer board correspondence, copper and return-path findings, and fabrication gates |
| What must be checked before the rev0 PCB, P01 plate, and wider parts orders? | [System order review](doc/REV0_ORDER_REVIEW.md) | Dated cross-system evidence, order disposition, and first dry-fit gates |
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
- **Driver placement in 3D:** [driver 3D model](doc/3d_models/README.md),
  then [mechanical design](doc/MECHANICAL.md) for the cabinet constraints.
- **PSU placement in 3D:** [RSP-200-36 model](doc/3d_models/RSP-200-36.md),
  then [mechanical design](doc/MECHANICAL.md) for enclosure and guard space.
- **Mains-inlet placement in 3D:** [DD11.0111.1111 model](doc/3d_models/DD11.0111.1111.md),
  then [mechanical design](doc/MECHANICAL.md) for the rear FR-4 panel mounting.
- **Control placement in 3D:** [PDB18 potentiometer models](doc/3d_models/PDB18-potentiometers.md),
  then [mechanical design](doc/MECHANICAL.md) for the rear FR-4 panel mounting.
- **Rear signal-part placement in 3D:** [RCA and polarity-switch models](doc/3d_models/Rear-signal-parts.md),
  then [mechanical design](doc/MECHANICAL.md) for the rear FR-4 panel mounting.
- **Provisional heatsink placement in 3D:** [557-140AB model](doc/3d_models/557-140AB.md),
  then [thermal design](doc/THERMAL.md#12-bolt-on-extrusion-shortlist-31-october-2026) for the cooling decision.
- **Fastener placement in 3D:** [fastener model routes](doc/3d_models/README.md#2-fastener-layout-references),
  then [mechanical design](doc/MECHANICAL.md) for the assembly and length decisions.
- **DipTrace schematic or PCB inspection:** [DipTrace data and
  tooling](doc/DIPTRACE.md), then the [current PCB layout review](doc/PCB_LAYOUT.md)
  for a routing or fabrication question and only the affected electrical,
  grounding, or mechanical authority. Load only the shared Hub SDK files
  selected by that route.
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
