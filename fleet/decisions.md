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

- **F-DEC-02 — Every plane and drone is "SMART": ELRS plus a flight controller**
  (2026-09-17, owner). Going forward, each aircraft in the fleet flies an ExpressLRS
  receiver into a programmable flight controller, never a proprietary radio or
  stabilisation ecosystem. Reason, the owner's: to avoid lock-in to closed ecosystems such
  as Spektrum's. The owner's word "SMART" is not otherwise defined; GPS, telemetry or a
  firmware choice are not implied by this decision. Already so by their BOMs: Bee35 and 5".
  Holybro 10": flight controller chosen, receiver TBC. To commission to it: the Swordfish
  and the Phoenix.
