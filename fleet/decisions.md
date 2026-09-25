# Fleet decisions

Decisions true of more than one aircraft. Per-aircraft decisions live in each aircraft's
`docs/decisions.md`. Format: `F-DEC-nn — decision (date)`.

- **F-DEC-01 — Which aircraft are wk-robotics robots** (2026-09-13, owner). The
  criterion is wk-robotics's, defined once in its
  [`docs/common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md#aircraft-and-the-tiers):
  an aircraft is a family robot when an intent tier commands its flight controller,
  wherever that tier runs. Applied to the fleet:
  - **Holybro 10" — yes.** Bought specifically to carry a Raspberry Pi or Jetson
    hard-wired to the flight controller: the onboard-intent topology. The fleet's only
    candidate, and the only aircraft the wk-robotics index lists as a project.
  - **Bee35 — no.** An FPV aircraft; no room for a computer and no plan for one
    ([DEC-07](../aircraft/bee35/docs/decisions.md)).
  - **5" freestyle — no.** A human on the sticks. A small Pi on it has been floated by
    the owner and is not a decision; it is recorded on the aircraft's page as an idea.

  A human pilot is neither topology. Any of the three could cross the line later under the
  off-board topology (a ground machine commanding the flight controller over radio); that
  would be a new decision here, not an edit to this one.

- **F-DEC-08 — No DJI: the fleet stays on open/hobbyist video** (2026-09-25, owner).
  "O4 is DJI, and I have zero DJI kit in my ecosystem, I prefer to stay hobbyist not
  corporate." Video stays **Walksnail Avatar HD**, which every aircraft's goggles already
  are (Fat Shark Dominator Avatar HD). Same reasoning as
  [F-DEC-02](#f-dec-02)'s rejection of closed radio ecosystems.
  - **Nothing DJI has ever been bought** (invoice ledgers and mailbox searched
    2026-09-25): the only DJI-named lines are a goggle power adapter and an antenna pack
    that lists DJI among several compatibilities.
  - **The Bee35's aluminium head module is not a DJI purchase.** The frame variant bought
    was "Bee35 Pro (with CNC VTX heatsink)" (Unmanned Tech #18595), whose head is the
    O4-Pro-style aluminium assembly; SpeedyBee's O4 tutorial therefore documents that
    hardware. The aircraft flies a Walksnail Nano V3 in it
    ([OQ-04](../aircraft/bee35/docs/open-questions.md)).

- **F-DEC-07 — Every multirotor carries a downward MicoAir MTF-01P** (2026-09-25, owner).
  Optical flow plus ToF range, facing down, for position hold and height near the ground.
  Multirotors only: the planes hover nothing and gain nothing.
  - **State:** Bee35 fitted and working on UART4 ([its `wiring.md`](../aircraft/bee35/docs/wiring.md));
    the 5" and the Holybro 10" have none. **Two ordered 2026-09-25** — Unmanned Tech
    #19494, £45.98 the pair, £49.57 with shipping and tax, due 2026-09-28. Nothing else in
    stock serves: the one other flow
    sensor owned, a Matek 3901-L0X, was rejected on 2026-09-25 — 2 m range and a VL53L0X
    that sunlight swamps (wk-inventory `docs/stock.md`).
  - **The Holybro carries both it and the TFmini Plus**, whose ToF it duplicates. The
    TFmini stays: 12 m, IP65, bought for accurate height on landing. Which one ArduPilot
    reads as `RNGFND1` there is unsettled.
  - **The 5" needs [F-DEC-06](#f-dec-06) done first** — flow is no use to it on Betaflight.
  - Mounting is per aircraft and unsolved on both: Bee35 [OQ-05](../aircraft/bee35/docs/open-questions.md).

- **F-DEC-06 — ArduPilot or iNav on every aircraft; no Betaflight** (2026-09-25, owner).
  Anything new, and anything reflashed, runs ArduPilot or iNav. Betaflight is not used:
  the fleet is built around position hold, autonomy and flow or GPS aiding, which is what
  those two firmwares are for.
  - **The 5" is the only aircraft affected**, and it converts — its
    [OQ-01](../aircraft/fpv-5/docs/open-questions.md) is now *when* and *to which*, not
    *whether*. It is flight ready today, so converting means reflashing, retuning and
    re-testing a working aircraft; save its Betaflight `diff all` and `dump all` to
    `aircraft/fpv-5/config/` first.
  - Current state: Bee35 ArduPilot ([DEC-08](../aircraft/bee35/docs/decisions.md)),
    Holybro none flashed with ArduPilot implied ([DEC-01](../aircraft/holybro-10/docs/decisions.md)),
    5" Betaflight.
  - **Amended 2026-09-25, owner — one reference aircraft per firmware:**
    - **5" — the fleet's reference iNav.** Settles *which* in its
      [OQ-01](../aircraft/fpv-5/docs/open-questions.md); only *when* is left. Its
      SpeedyBee F405 V3 makes the choice for it: ArduPilot's `speedybeef4v3` build
      compiles optical flow out, so the MTF-01P of
      [F-DEC-07](#f-dec-07) would be dead on it.
    - **Bee35 — the fleet's reference ArduPilot**, already flying it
      ([DEC-08](../aircraft/bee35/docs/decisions.md)).
    - **Holybro 10" follows the Bee35 onto ArduPilot**, making DEC-01's implication
      explicit. Its H743 carries the full build, so nothing the Bee35 proves is out of
      reach there.
    - What a reference aircraft is for: settings, wiring conventions and procedures are
      worked out once on it and carried across, rather than re-derived per airframe.

- **F-DEC-05 — Pre-flight, every switch is back** (2026-09-22, owner). On every model,
  all switches pushed away from the pilot is the safe starting state: disarmed, no
  failsafe or special function active, and the most manual flight mode (Stabilize on
  ArduPilot multirotors). Each model's switch functions are mapped to fit, so a single
  glance checks the radio. EdgeTX's switch warnings on the TX16S already expect every
  switch "up" (back). Layout: [`radio.md`](radio.md).
- **F-DEC-04 — The fleet is all-electric** (2026-09-17, owner). No internal-combustion
  aircraft. The Seagull 40 was glow-powered and was the owner's "last gasp" before
  converting to all-electric; it is written off (wk-inventory stock), and the fuelproofer
  and fuel tubing bought from Wheelspin in 2023 were for it. Every aircraft since is
  electric.

- **F-DEC-03 — Consolidate battery types; share packs across aircraft** (2026-09-17,
  owner). Packs are costly and inconvenient to store and charge, so the fleet keeps as few
  variants as it can and flies them across several aircraft rather than buying a format per
  airframe. A new aircraft that needs a new pack format is a cost to weigh, not a given.
  **Today that means two standards:** 4S for the quads and the Holybro, 6S for the large
  planes. The Twin Otter specified 6S, which surprised the owner at purchase precisely
  because the rest of the fleet is 4S. Pack holdings and which aircraft fly them are in
  [`README.md`](README.md).

- **F-DEC-02 — Every plane and drone is "SMART": ELRS plus a flight controller**
  (2026-09-17, owner). Going forward, each aircraft in the fleet flies an ExpressLRS
  receiver into a programmable flight controller, never a proprietary radio or
  stabilisation ecosystem. Reason, the owner's: to avoid lock-in to closed ecosystems such
  as Spektrum's. The owner's word "SMART" is not otherwise defined; GPS, telemetry or a
  firmware choice are not implied by this decision. Already so by their BOMs: Bee35 and 5".
  Holybro 10": flight controller chosen, receiver TBC. To commission to it: the Swordfish
  and the Phoenix. The Twin Otter flies a receiver with no flight controller; bringing it to this standard is a rebuild, low priority (owner, 2026-09-17). The Avanti S, also built without a flight controller, is crashed and in storage; its repair is the moment to fit one (owner, 2026-09-17).
