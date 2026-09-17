# System specification

## 1 Locked decisions

Do not revisit without measured/simulation evidence:

- SB23MFCL45-4
- sealed enclosure
- 360 × 340 × 300 mm external cabinet
- approximately 20 L net
- 36 V main rail
- TPA3251 PBTL
- approximately 140–150 W
- 450 kHz switching frequency
- passive cooling
- OPA1678/OPA1679
- single 12 V analogue rail
- buffered 6 V VMID
- stereo RCA input
- approximately 47 kΩ input impedance
- active mono averaging
- 2nd-order Butterworth Sallen-Key LPF
- dual-gang linear crossover pot
- approximately 40–100 Hz range
- mono level control
- selectable 0°/180° polarity
- differential TPA3251 drive
- IHLP5050FDER100M5A inductors
- SMD-only amplifier board
- X7R MLCC output-filter capacitors
- 6 mm 1050A-H14 aluminium rear plate
- matt-black external plate finish
- no fan
- no MCU/firmware

## 2 Driver

- SB Acoustics `SB23MFCL45-4`
- 4 Ω
- `Fs ≈ 27 Hz`
- `Qts ≈ 0.34`
- `Vas ≈ 37 L`
- `Sd ≈ 210 cm²`
- `Xmax ≈ ±12 mm`
- rated power ≈ 150 W

## 3 Cabinet

- sealed
- external dimensions: `360 × 340 × 300 mm`
- material: 18 mm plywood
- target net acoustic volume: approximately 20 L
- target gross internal volume before displacement: approximately 24–25 L
- expected `Qtc ≈ 0.57`
- expected system resonance `Fc ≈ 46 Hz`
- suitable internal bracing required

## 4 Amplifier

- TI `TPA3251`
- mono PBTL
- 4 Ω load
- main rail: 36 V DC
- target clean output: approximately 140–150 W
- switching frequency: 450 kHz
- passive cooling only

## 5 Main PSU

- current candidate (not locked in yet): Mean Well RSP-200-36
- commodity enclosed mains SMPS, fanless
- 36 V, 200-250 W
- selected unit must come from a reputable manufacturer
