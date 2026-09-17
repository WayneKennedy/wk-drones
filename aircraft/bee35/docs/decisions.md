# Decisions

Architecture decision records. Unresolved items live in
[`open-questions.md`](open-questions.md). Each captures the decision, the alternatives and the
reasoning, not just the outcome. Format: `DEC-nn — decision (date)`.

- **DEC-01 — iNav over ArduPilot** (2026-09-11). ArduPilot's EKF3 Loiter is the
  stronger position hold and was the original plan. Chose iNav for firmware
  commonality with the existing 5" quad, a familiar configurator, and an easier
  tune. Hardware is identical either way, so ArduPilot remains a reflash away if
  iNav's hold disappoints. Confirmed by DEC-06.
  *Correction (2026-09-15):* the 5" runs Betaflight, not iNav (owner, checked on the
  aircraft in the SpeedyBee app). The commonality reason was false, and "familiar
  configurator" may have rested on the same belief. The easier tune, DEC-06's goal and
  the reflash path do not depend on it. The decision has not been revisited.

- **DEC-02 — Bee35 Pro over standard Bee35** (2026-09-11). Not a preference: the
  standard version was out of stock. Turned out favourable. The alloy heatsink has
  20×20 mounting holes and takes the Walksnail VTX, which runs hot in a ducted frame
  with poor airflow.

- **DEC-03 — 4S over 6S** (2026-09-11). Motors were mis-ordered as 1700KV (the 6S
  variant) and exchanged for 3000KV. Considered building 6S P45B packs instead:
  ~50% more energy for ~50% more pack mass nets only ~10% endurance gain, at ~£60
  and a second pack format. Fleet commonality on the existing 4S1P P45B packs won.
  *Note (2026-09-17, invoices):* not an exchange. The 3000KV set is a separate purchase
  from Drone Authority; no return of the 1700KV set to Unmanned Tech is in the mail
  ([`bom.md`](bom.md)). The decision is unaffected.

- **DEC-04 — MTF-01P over MTF-02P** (2026-09-11). The -02P was the original spec and
  has been out of stock for months. The -01P is the better sensor anyway: 12 m lidar
  vs 6 m, 100 Hz vs 50 Hz. Its only disadvantage is ~3 g, irrelevant at this AUW.

- **DEC-05 — Flywoo GM10 Mini over Matek M10Q-5883** (2026-09-11). Matek stock
  unavailable in the UK due to export restrictions. Same M10050 + QMC5883L silicon,
  smaller patch antenna.

- **DEC-06 — iNav first; ArduPilot and the mission-planning tier are a later
  evolution** (2026-09-11, owner). The project's initial goal is a DIY build that
  gets close to the DJI Neo experience: reliable hands-off loiter and docile flight.
  Build on iNav to reach that, keeping DEC-01's commonality with the 5" quad (a premise
  since found false; see the DEC-01 correction). Only
  once the basic goal is met and the flight envelope is predictable does the
  aircraft become a fleet node reachable from the wk-robotics mission-planning
  tier, which needs ArduPilot: a native ROS 2 interface (AP_DDS) and two-way
  MAVLink, neither of which iNav has (its MAVLink is telemetry out and RC in only). The hardware
  supports both; the reflash is the whole cost. Resolves OQ-01.

- **DEC-07 — An FPV aircraft, not a family robot** (2026-09-13, owner). The goal is a
  DIY Walksnail/ELRS aircraft with a DJI-like hands-off FPV experience, and it stops
  there. Two reasons: the 153 mm ducted frame has no room for an intent-tier computer,
  and the wk-robotics criterion for an aerial robot (`docs/common.md`, *Aircraft and the
  tiers*) is that an intent tier commands the flight controller, which nothing here does
  or will. The fleet's aerial-robot candidate is the Holybro 10" (`../../holybro-10/`),
  bought to carry a Pi or Jetson wired to its flight controller. DEC-06 stands as written:
  the ArduPilot reflash remains available, and the off-board intent topology in the same
  `common.md` section means this airframe could still become a fleet node without any
  onboard change. It is not planned. OQ-02 applies only if this is revisited.
