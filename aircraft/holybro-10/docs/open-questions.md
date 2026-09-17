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

- **OQ-04 — Build state and the remaining parts** (2026-09-17). Whether the frame is
  assembled, and the receiver, video system and battery, are unrecorded
  ([`bom.md`](bom.md), [F-OQ-01](../../../fleet/open-questions.md)).
