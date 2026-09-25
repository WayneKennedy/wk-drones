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
  **No longer blocks the maiden** (owner, 2026-09-25): the wiring has been inspected and
  is sound, and **a visual check is part of every pre-flight on every aircraft**, which is
  where a disturbed plug gets caught. Still worth doing one of the options above, since the
  cause — a tight interior squeezing the stack — is unchanged. Details:
  [`wiring.md`](wiring.md) solder notes.

- **OQ-04 — Camera mount part mislaid** (2026-09-22, owner). Part of the frame's camera
  mount is missing, so the Walksnail Nano Camera V3 cannot be mounted and the OSD step
  (checklist step 9) waits. **Which part is missing: the aluminium standoff for the camera
  mount and the camera grommets** (owner, 2026-09-23). Both are frame hardware, not
  printable: sourcing or substituting them is the fix, alongside the mount itself.
  - **Both parts are named in SpeedyBee's
    [O4 Air Unit Pro aluminium head module tutorial](https://support.speedybee.cn/pdf?f=hg2h&l=en)**
    (dated 2025-08-06, read 2026-09-25): a **25.5 mm aluminium standoff** across the top of
    the two aluminium head side plates, held by **two M2.5 × 8 mm button-head socket
    screws**, and **four vibration damping balls** seated in the camera support mount.
    Rest of that head's schedule: camera to support mount 4 × M2 × 3; VTX to the CNC
    cooling bottom plate 4 × M2 × 6; ring to cooling plate 4 × M3 × 14; head module to ring
    and carbon plate 2 × M3 × 14 + 2 × M3 × 10; antenna mounts M2 × 8.
    **To confirm: that this aircraft has that same aluminium head module** — the tutorial
    is written for the O4 Air Unit Pro and this aircraft carries a Walksnail Nano V3. If it
    does, those are the parts to source.
  - **The camera itself is no longer a problem** (owner, 2026-09-25): the Nano V3 came with
    a TPU adapter that brings it to standard 19/20 mm camera width, and it is sitting in
    the head's side plates now. The 14 → 19 mm gap this entry used to carry is closed.
  - **Nothing off the shelf replaces the head.** Measured from the official STLs
    (bounding boxes, 2026-09-25): `19mmCamera-mount-bracket.stl` is **13.2 × 13.2 ×
    4.25 mm**, a retainer, not a head; SpeedyBee's O4P camera support print is **23.6 ×
    24.3 × 30.9 mm** and still needs the aluminium side plates. Community full-TPU mounts
    ([Printables 1242717](https://www.printables.com/model/1242717-speedybee-bee35-dji-04-air-unit-pro-camera-mount),
    [Cults3D](https://cults3d.com/en/3d-model/gadget/speedybee-bee35-dji-o4-pro-tpu-camera-mount))
    are modelled around the O4 Pro camera, not a 19 mm standard one.
  - **Owner's approach, 2026-09-25: a printed insert between the CNC side plates**,
    screwed through the holes the damping balls use, holding the camera. It replaces the
    balls and the standoff's spacing job while keeping the aluminium plates that are
    already on the aircraft. **No vendor CAD is needed for it** — the plates are the fixed
    boundary. Four measurements off the airframe define the part: the inner gap between the
    plates, the ball-hole pattern and diameter on the plate faces, the camera's width and
    side-screw spacing, and the fore-and-aft depth available.
  - **Two paths, not exclusive** (owner is weighing them, 2026-09-25):
    **(a)** source the 25.5 mm standoff and four damping balls and keep the fitted CNC
    head — cheap, unblocks the maiden;
    **(b)** design a **TPU head** replacing both side plates and the standoff, taking the
    Nano at its adapted width — crash-friendlier and needs no vendor hardware, but it is a
    design job on the critical path. **Blocks the
  OSD step and the maiden** — with [OQ-05](#), one of the two remaining blockers (owner,
  2026-09-25).

- **OQ-05 — Flow sensor mount** (2026-09-22, owner). The MTF-01P is wired and working on
  UART4 but not mounted. Its mounting is 24.3 × 12 mm, Ø2.5 mm holes (MicoAir; official
  case STL, [`../print/sources.md`](../print/sources.md)).
  - **Location, second decision (owner, 2026-09-25, evening): up front, under the nose,
    on a three-point fastening** — two of the camera bracket's screws plus the heatsink's
    **forward** M2. Supersedes the same day's first choice, the heatsink itself (4 × M2 on a
    20 × 20 square sitting as a diamond to the airframe): a bracket for it was modelled
    ([`../print/sources.md`](../print/sources.md), commit `f4b3763`) and dropped because
    **it put the sensor too low** — with no landing gear the sink is the belly, and the
    sensor would have hung 21 mm below it. Up front it sits higher; `FLOW_POS_X` is then
    non-zero and must be measured and set.
  - **Heat, judged a non-issue by the owner (2026-09-25):** prop wash cools the underside
    in flight. Noted against it: the uncooled case is ground time with the VTX up, where
    TPU under constant load creeps rather than breaks, which would show as the sensor
    slowly drifting off vertical. **Four M2 standoffs giving an air gap** remove the
    concern at no cost and keep the fins in the airflow; not yet decided.
  - **There is no landing gear** (owner, 2026-09-25): the heatsink is the belly. Whatever
    hangs lowest is what the aircraft lands on, so the bracket needs feet or the sensor
    needs to sit above the sink's face. The sink's holes are **tapped M2 with 2 mm free
    behind them** (owner).
  - **Geometry given (owner, 2026-09-25):** the two front holes are **M3 clearance, 24 mm
    apart**, and define the datum; the third is on the centreline, **41 mm from each**, so
    39.2 mm aft; all three taken coplanar for now. **First-pass bracket drawn**
    ([`../print/sources.md`](../print/sources.md) `flow-mount`, not printed): 38 × 48 × 3
    plate, sensor long-axis across behind the front holes, face 20.8 mm off the mounting
    surface. **Then rejected by the owner the same evening, on seeing the drawing: at the
    nose the sensor hangs in the front ducts' downwash** — not by much, but the owner will
    not put the ducted airflow at risk, and a 17 mm bluff body at a duct exit is a
    vibration source. **Constraint from here: nothing in the ducts' outflow.** The
    airframe also has a moulded foot just aft of the front hole line, centred, which any
    nose plate would have to window round. Location is open again; three positions have
    now been tried on paper, and the choice is between the centre (clear of the ducts,
    but 17 mm + plate below the belly) and somewhere the sensor can recess up into the
    frame with its face flush.
  - The mount fixes `FLOW_ORIENT_YAW`, `FLOW_POS_*` and `RNGFND1_GNDCLR`, so the direction
    check and calibration wait for it.

  **Blocks the maiden** (owner, 2026-09-25) — with
  [OQ-04](#) it is one of the two things now standing between this aircraft and its first
  flight.
