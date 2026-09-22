# Open questions

Pending decisions. Resolved items move to [`decisions.md`](decisions.md) as a DEC.
Format: `OQ-nn — question (date raised)`.

- **OQ-01 — Aerial robot: how the fleet mission planner reaches it, and what that
  means for firmware** (2026-09-11). **Resolved 2026-09-11 by
  [DEC-06](decisions.md): iNav first, ArduPilot as a later evolution.** DEC-06's firmware
  half is superseded by [DEC-08](decisions.md) (2026-09-19): ArduPilot from the start. The
  analysis is kept below for the fleet-node step.

  Original question: The aircraft is to be treated as an aerial robot
  in the wk-robotics family, reachable from the mission planner. In that family
  "Mission Planning" is the aspirational off-robot third tier above reflex and intent
  (wk-robotics `docs/common.md`, `docs/ideas.md`), speaking ROS 2 over the
  [topic contract](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#the-topic-contract).
  It may also mean ArduPilot's Mission Planner ground station. Either reading
  favours ArduPilot and conflicts with DEC-01:
  - **ArduPilot** has a native ROS 2 interface (AP_DDS, micro-ROS XRCE-DDS over
    serial or UDP, ArduPilot 4.5+) and full two-way MAVLink, so Mission Planner and
    a ROS 2 mission tier can both command it. The MicoAir743 V2 ships with it.
  - **iNav** has no ROS 2 interface. Its MAVLink support is telemetry out plus, from
    iNav 8, RC in over MAVLink (ELRS MAVLink mode). A ground station can display
    telemetry but cannot upload missions or change parameters. Unverified whether any
    other MAVLink commands are accepted.
  - A third path, iNav now and ArduPilot when the fleet role is real, keeps DEC-01's
    commonality with the 5" quad for the maiden and tune. (That commonality proved
    false on 2026-09-15: the 5" runs Betaflight. See the DEC-01 correction.)

  Unlike every other robot in the family, the flight controller is reflex and
  intent tier in one MCU; there is no on-board Pi. How it joins the topic contract
  is part of this question.

- **OQ-02 — Radio link for the mission-planning step: ELRS MAVLink mode or a third
  radio** (2026-09-11). Dormant since [DEC-07](decisions.md): the fleet-node step is not
  planned for this airframe. Kept because the analysis applies to any aircraft in the
  fleet taking the off-board intent topology. If the fleet-node step is taken, Mission Planner and the
  ground-side ROS 2 bridge need a two-way MAVLink link. The aircraft carries two
  radios already: ELRS 2.4 GHz for RC and Walksnail Avatar for video. Walksnail is
  video only as far as known; not verified. Options:
  1. **ELRS MAVLink mode, no extra radio.** Working assumption. ExpressLRS 3.5+
     (TX backpack 1.5+, ESP-based hardware only) carries RC embedded in MAVLink over
     the existing link, with telemetry back. Ground station connects to the TX
     backpack over WiFi, UDP port 14550. The RP3 V2 and RadioMaster internal module
     qualify. Supported by ArduPilot, PX4, iNav 8+ and Betaflight. Constraints:
     forced Hybrid/16ch-2switch mode and a fixed 1:2 telemetry ratio; 2.4 GHz
     throughput per the ELRS docs is ~2375 B/s down / ~1190 B/s up at F1000,
     ~1470 / ~735 at 333 Hz Full, ~110 / ~60 at 50 Hz. Enough for telemetry,
     parameters and mission upload; slow on a first full parameter fetch.
  2. **SiK telemetry radio (868 MHz in the UK), 57600 baud.** The traditional
     Mission Planner link and faster, at the cost of a UART, another antenna and
     ~20–30 g on a frame at its weight budget. Fallback if ELRS throughput proves
     inadequate.
  3. A companion computer with WiFi or 4G is a stated non-goal.

  In every option the hive-mind tier reaches the aircraft through the ground host
  (MAVLink to a ROS 2 bridge there), not over an air link of its own, which keeps the
  aircraft flying when that tier is unreachable. Nothing to buy until that step
  is due. Sources: <https://www.expresslrs.org/software/mavlink/>.

- **OQ-03 — Wiring strained by closing the frame: securing it before the maiden**
  (2026-09-22). The plug-to-plug harness between the stack boards worked loose twice on
  the first bench day: motors 3 and 4 did not respond until it was pressed home, and
  later, after the frame was screwed down, battery power stopped reaching the FC
  (`voltage_battery` 0) until it was reseated (owner). The frame is very tight
  internally when closed, and the squeeze on the stack is the suspected cause. Loose in
  flight, it drops FC power or motor signals. The same day the **MX-12 USB extension
  lead** stopped carrying data after the frame was closed: FC powered over it but did
  not enumerate on the PC, and did enumerate with the same cable plugged straight into
  the FC's USB-C (owner). Cause found on strip-down: a yellow wire in the extension
  harness pinched and broken when the frame was closed after reseating the harness;
  repaired, extension working again (owner, 2026-09-22). The owner counts the frame's tight interior against it.
  Options, none chosen: a retaining dab of hot glue or silicone over both plugs;
  re-routing with slack so closing the frame cannot pull on it; both. For the USB
  extension: repair or remake it with slack, or do without it and plug into the FC
  directly with the frame open.
  **Blocks the maiden.** Details: [`wiring.md`](wiring.md) solder notes.

- **OQ-04 — Camera mount part mislaid** (2026-09-22, owner). Part of the frame's camera
  mount is missing, so the Walksnail Nano Camera V3 cannot be mounted and the OSD step
  (checklist step 9) waits. Which part is missing: TBC. Options: find it; or print it —
  SpeedyBee publishes `19mmCamera-mount-bracket.stl` ([`../print/sources.md`](../print/sources.md)),
  but whether that is the missing part is unchecked, and the Nano V3 is 14 mm, so a
  14→19 mm adapter is needed either way ([`bom.md`](bom.md) camera row). **Blocks the
  OSD step and the maiden.**

- **OQ-05 — Flow sensor mount** (2026-09-22, owner). The MTF-01P is wired and working on
  UART4 but not mounted: the frame's underside has no obvious flat surface for it. It
  must face straight down with a clear view, and its mounting is 24.3 × 12 mm, Ø2.5 mm
  holes (MicoAir; official case STL, [`../print/sources.md`](../print/sources.md)).
  Likely a designed-and-printed bracket, parametric like the Holybro deck
  ([`../../holybro-10/print/src/h743-deck.py`](../../holybro-10/print/src/h743-deck.py)).
  Needed first: where on the underside it goes and the frame geometry there. The
  mounting fixes `FLOW_ORIENT_YAW`, `FLOW_POS_*` and `RNGFND1_GNDCLR`, so the direction
  check and calibration wait for it. **Blocks flow use; not the maiden in GPS modes.**
