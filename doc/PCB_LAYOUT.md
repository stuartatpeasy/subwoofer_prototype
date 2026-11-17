# PCB layout review

> **Lifecycle:** rev0 PCB design complete; prototype board in fabrication, as reported 17 November 2026.
>
> **Owns:** Board release identity, design observations and remaining prototype checks.
>
> **Does not own:** Circuit selection, plate design, assembled performance or prior review chronology.
>
> **Read when:** Assessing the fabricated board, bringing it up or considering a future layout change.
>
> **Current conclusion:** The rev0 board has been sent to fabrication. The user reports adequate clearance for prototyping; physical fit and performance remain to be verified on received hardware.
>
> **Next gate:** Inspect the received board and component/plate assembly, then perform the applicable checks in [prototype validation](VALIDATION.md). Rerun affected design checks if the design changes.
>
> **Limitations:** Fabrication does not establish assembly fit, electrical operation or thermal performance; ERC, DRC and connectivity results were user-reported rather than independently inspected.
>
> **Last reviewed:** 2026-11-17

## 1 Reviewed design state and scope

The released `diptrace/main_board.dchxml` schematic has SHA-256 `8D2DF8FC4B64DD681D15BC050AD40E1F75A72F9E70D3C4CA319837E9E8CDA36C`; `diptrace/main_board.dipxml` has SHA-256 `3744A7833C0E57E4FE62DCA9915B242764058CE7C559B1F7AC672308E9A5288A`; and `diptrace/main_board_gerber.zip` has SHA-256 `7F4FC58342F29ACC4264627F15A6F0F761676DC9A96459C25625F79BC9E8082E`. The saved 90 × 100 mm four-layer board has four Ø3.40 mm corner NPTH and two Ø2.90 mm IC-adjacent NPTH. The export passed ZIP CRC and layer-function checks; its six non-plated hits match the saved PCB. The reported fabrication order supersedes the earlier proposed upload-preview gate; the preview outcome itself was not independently observed here.

The user reports passing ERC, DRC and connectivity checks after the final refill. These were not independently inspected. Repeat affected checks after any design, routing, copper or rule change. The [dated review archive](history/PCB_LAYOUT_HISTORY.md) retains the earlier file identities, release evidence and detailed findings.

## 2 Findings

| ID | Current consequence |
| --- | --- |
| PR-001, PR-012 | Inspect the U9 DPAK solder joints and measure its temperature under actual sustained load. Its 6.04 × 5.63 mm tab land is smaller than ST's recommended 6.70 × 6.70 mm land; this is an accepted prototype choice. |
| PR-002, PR-004–PR-006 | Preserve the resolved U3 local GND connection, supply/return routing and plane arrangement if the board is revised. |
| PR-003 | The selected maximum 5 mm fastener lies within the 6 mm keep-out; verify the actual fit during assembly. |
| PR-007, PR-014 | The analogue reference and copper beneath L5 are accepted for the prototype. Assess assembled ripple and noise before changing them. |
| PR-008, PR-011 | Check probe access with the plate and components installed. Use a short local ground return for ripple measurements. |
| PR-009 | ERC, DRC and connectivity were reported passing; rerun the affected checks if the design changes. |
| PR-010 | The prototype board is in fabrication. The prior export inspection and its limits are retained in the [history](history/PCB_LAYOUT_HISTORY.md). |
| PR-013 | If a stencil is ordered, suppress paste on test pads TP1–TP11. |

## 3 Engineering interpretation

J6 joins its three positive pins to the common 36 V field and its three return pins to GND. The three paired feed/return cables are parallel paths and need not share current equally. Check the actual terminations, cable support and return paths against [power and grounding](POWER_AND_GROUNDING.md#4-36-v-distribution).

Inner 2 provides the local GND reference beside U3 and Inner 1 carries the broad 36 V field. Portions of the analogue routing instead reference the more distant Inner 2 GND. The saved geometry does not establish assembled noise: measure it before revising the plane arrangement. Local supply and output-filter returns should remain short and the RCA returns isolated as described in the grounding authority.

## 4 Prototype checks

Inspect received board and component clearances, the selected fastener/keep-out and probe access during assembly. Verify the U3-to-plate contact stack without forcing or bowing the board, and measure U9 and amplifier thermal behaviour at representative load. The [mechanical authority](MECHANICAL.md) owns the plate and fit details; [prototype validation](VALIDATION.md) owns the electrical and thermal checks. Retain the independent protective-earth and mains-construction checks before first mains energisation.

## 5 Current release disposition, 12 November 2026

The 12 November package is the rev0 fabrication release; the user reported on 17 November that the board is in fabrication and its clearance is adequate for prototyping. The precise factory preview and manufacturing results have not been independently verified here. Physical fit, thermal and electrical checks remain for the built prototype. Earlier order-preparation gates and superseded checkpoints are retained as dated evidence in the [review archive](history/PCB_LAYOUT_HISTORY.md).
