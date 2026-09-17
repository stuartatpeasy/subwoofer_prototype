# Analogue front end

## 1 Overview

Use OPA167x family.

Preferred parts:

- `OPA1678` dual
- `OPA1679` quad

### 1.1 Signal chain

```text
RCA L/R
  |
RF protection + DC blocking
  |
L/R unity buffers
  |
active L+R averaging summer
  |
variable 2nd-order Butterworth LPF
  |
level control
  |
0° / 180° polarity selection
  |
single-ended to differential driver
  |
TPA3251
```

## 2 Inputs

Per channel:

- RCA input
- target input impedance: nominal 47 kΩ
- nominal source level: approximately 2 V RMS
- clean handling target: approximately 3 V RMS

Initial network:

```text
RCA
 |
1 kΩ series
 |
330–470 pF RF shunt
 |
2.2 µF film coupling capacitor
 |
47 kΩ to VMID
 |
OPA167x unity buffer
```

Requirements:

- source must see a benign, well-defined load
- no dependence on source-specific output impedance
- input protection should not add significant capacitance/distortion

## 3 Stereo-to-mono summer

Topology:

- active inverting averaging summer
- non-inverting input referenced to VMID

Initial values:

- `R_L = 22 kΩ`
- `R_R = 22 kΩ`
- `R_F = 11 kΩ`

Transfer:

```text
Vmono = -0.5 × (VL + VR)
```

Use 0.1% resistors if practical.

## 4 Variable low-pass filter

Locked topology:

- 2nd-order Sallen-Key
- Butterworth
- `Q ≈ 0.707`
- 12 dB/octave
- continuously variable
- dual-gang linear pot
- target range approximately 40–100 Hz
- unity-gain filter stage

Initial values:

- `C2 = 82 nF`
- `C1 = 164 nF` using `2 × 82 nF` in parallel
- each R arm = `13.7 kΩ + one 20 kΩ pot gang`

Expected range:

- minimum R: approximately 100 Hz
- maximum R: approximately 41 Hz

TODO:

- verify exact transfer function/Q/frequency range in simulation
- choose exact pot series/tolerance

## 5 Level control

- mono
- post-LPF
- initial value: 10 kΩ logarithmic pot
- connected between LPF output and VMID
- wiper feeds differential-driver stage

## 6 Polarity control

Provide user-selectable:

- 0°
- 180°

Preferred implementation:

- differential driver generates `+V` and `−V`
- DPDT switch swaps differential lines
- no unnecessary dedicated inverter stage

## 7 Differential driver

Requirements:

- drive TPA3251 differentially
- target total differential voltage gain approximately 1.2
- approximate per-leg gain: ±0.6
- allow approximately 2 V RMS source to drive amplifier close to full power with level control at maximum

TODO:

- confirm TPA3251 exact input sensitivity/gain configuration
- choose final resistor values
- confirm headroom on 12 V analogue rail
