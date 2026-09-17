# Open questions

Pending decisions. Resolved items move to [`decisions.md`](decisions.md) as a DEC.
Format: `OQ-nn — question (date raised)`.

- **OQ-01 — Aerial robot: how the fleet mission planner reaches it, and what that
  means for firmware** (2026-09-11). **Resolved 2026-09-11 by
  [DEC-06](decisions.md): iNav first, ArduPilot as a later evolution.** The
  analysis is kept below for when that step is taken.

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
  fleet taking the off-board intent topology. When DEC-06's ArduPilot step is taken, Mission Planner and the
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
  aircraft flying when that tier is unreachable. Nothing to buy until DEC-06's step
  is due. Sources: <https://www.expresslrs.org/software/mavlink/>.
