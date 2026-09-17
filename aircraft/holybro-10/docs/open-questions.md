# Open questions

Pending decisions for the Holybro 10". Decisions, once taken, go in
[`decisions.md`](decisions.md). Format: `OQ-nn — question (date raised)`.

- **OQ-01 — A GPS each for the reflex and intent tiers?** (2026-09-17, owner). The
  owner's recollection, stated as "I think", of why two Matek M10Q-5883 GPS/compass
  units were bought: one for the flight controller and one for the companion computer,
  so both tiers have first-class access to position. The owner also believes the two
  Matek CAN Node L431 boards were bought for GPS and compass. Matek's
  [CAN node page](https://www.mateksys.com/?portfolio=can-l431) confirms that use: it
  bridges a GPS (UART) and a compass (I²C, QMC5883L by default) onto DroneCAN. Open:
  - whether the plan stands;
  - how the companion's GPS connects. A CAN node puts a GPS on the flight controller's
    DroneCAN bus; a Pi or Jetson would more simply read a GPS over its own UART or USB.
    Two nodes for one flight-controller GPS is unexplained;
  - the alternative of both units on the flight controller as ArduPilot dual GPS, with
    the companion reading position over MAVLink. Not assessed.

- **OQ-02 — Companion link wiring** (2026-09-17). The owner recalled planning MAVLink
  over wired I²C. MAVLink does not run over I²C: ArduPilot's wired companion link is a
  UART (TX, RX, ground) or USB, which is what the family's onboard topology already
  specifies. Pi and Jetson Orin Nano header UARTs are 3.3 V logic. Open: which H743
  serial port, baud rate, and UART or USB.

- **OQ-03 — Raspberry Pi or Jetson Orin Nano?** (2026-09-17, owner). **Leaning Jetson,
  not decided:** the owner thinks this airframe is "probably the highest value use" of the
  Jetson Orin Nano Super Developer Kit ordered 2026-09-17 (wk-robotics
  [`docs/status.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/status.md#ai-compute-purchase--ai-hat-2-jetson-or-dgx-spark)).
  Payload, power and mounting budgets for either are not done; Holybro quotes a 1500 g
  maximum payload excluding battery.

- **OQ-05 — A separate control pack for the companion computer** (2026-09-17, owner).
  Proposed: power the Jetson from its own 21700 pack, completely separate from the flight
  controller and ESC supply, as the hexapod does (its LOAD and CTRL rails,
  [wk-hexapod `docs/hardware.md`](https://github.com/WayneKennedy/wk-hexapod/blob/main/docs/hardware.md)).
  It matches the family power rule — isolate the logic rail
  ([wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#power-integrity)).
  Constraints found 2026-09-17, none tested here:
  - **2S is below the kit's input range.** The Orin Nano developer kit takes **9–20 V** on
    its 5.5 × 2.5 mm jack (NVIDIA staff,
    [forum](https://forums.developer.nvidia.com/t/jetson-orin-nano-input-voltage/298625);
    carrier spec SP-11324-001). A 2S1P Li-ion pack is 6.0–8.4 V, so it needs a boost
    converter. A **3S1P** (9.0–12.6 V) feeds it directly but sits on the floor of the range
    at cut-off; a **4S1P** (12.0–16.8 V) sits comfortably inside it.
  - **Energy is not the constraint.** At the Super profile's 25 W ceiling, a 4S1P P45B pack
    (~65 Wh) outlasts any flight; pack choice is about mass and simplicity.
  - **Separate does not mean floating.** The Jetson-to-flight-controller UART needs a common
    ground reference (OQ-02), so the two packs share a ground at that link, or the link is
    isolated.
  - **Still to decide:** cell count and where the pack mounts; low-voltage cut-off and a
    clean Jetson shutdown before it; fusing; how each pack's voltage is monitored (the
    flight controller's second battery input, or an I²C monitor on the Jetson); and whether
    the fleet's charger handles Li-ion.
  - **Stock, so nothing need be bought yet:** the fleet's **4S 1300 mAh LiPo packs** are in
    range at 14.8–16.8 V and are the lightest option in hand — the owner reports several,
    stored at storage voltage about a year ago and not puffy (2026-09-17), untested since.
    Two GNB 1300 mAh 4S 120C were bought 2024-05-17 and three GNB 1300 mAh 4S 120C **LiHV**
    2025-08-07 ([fleet](../../../fleet/README.md)); the 5" flies packs of this size, so they
    are shared. A LiPo has no protection circuit, so the cut-off above is the builder's job.
    No spare 21700 cells are recorded, and the three 4S1P P45B packs are flight packs, so a
    purpose-built control pack would mean buying cells.

- **OQ-04 — Build state and the remaining parts** (2026-09-17). Whether the frame is
  assembled, and the receiver, video system and battery, are unrecorded
  ([`bom.md`](bom.md), [F-OQ-01](../../../fleet/open-questions.md)).
