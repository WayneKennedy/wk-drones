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

- **OQ-07 — How the flight controller is isolated from vibration** (2026-09-17, owner).
  The owner expects a 10" airframe to be a high-vibration one and is minded to change the
  deck ([DEC-02](decisions.md)) in two ways: **brass hex M3 standoffs pressed into the
  deck** so it sits snug on the plate, and **TPU** for the deck itself so it isolates the
  board. Neither is decided. What is established:
  - **Big props make the harder case, not just a louder one.** Vibration sits at motor
    rotation frequency. A 5" quad turns roughly 15,000–20,000 rpm, i.e. 250–330 Hz. These
    2216 KV880 motors on 4S with 1045 props will hover somewhere near 4,000–6,000 rpm,
    i.e. **roughly 70–100 Hz — an estimate, to be replaced by an FFT of a hover log**.
    Lower frequency is harder to filter and closer to the flight-control band, and a
    heavier prop carries more imbalance energy.
  - **An isolator only attenuates above √2 × its own natural frequency**, and must stay
    above the attitude-control band (~10–20 Hz). So the useful window for a soft mount
    here is a natural frequency of roughly **25–40 Hz**, which is a design target, not a
    material choice — durometer, beam section and isolated mass all set it.
  - **Brass standoffs answer the objection to a TPU deck.** Bolt preload through TPU
    relaxes (compression set) and the joints go loose; a brass standoff carries the
    preload in metal and leaves the TPU to flex, which is the standard way to bolt a soft
    part. The two proposed changes therefore belong together.
  - **Open:** whether to isolate the whole deck or only the board on four pads; the target
    natural frequency and how it is verified; standoff length, across-flats and thread;
    TPU durometer; and whether isolated mass should be added deliberately to lower the
    frequency.
  - **Filtering cannot be assumed to cover it.** The ARF kit's BLHeli_S 20 A ESCs
    ([`bom.md`](bom.md)) carry no telemetry line, so an RPM-referenced harmonic notch fed
    from the ESCs is not available; it would have to be throttle-referenced or driven by
    in-flight FFT. Not assessed against ArduPilot's current options.

- **OQ-08 — Which Walksnail kit, given both are fitted elsewhere?** (2026-09-17, owner).
  The owner intends to fit a **Walksnail Avatar HD Pro Micro Kit** to this aircraft for FPV
  and flight observation, alongside ArduPilot and the autonomy that is the point of the
  airframe. **Exactly two were ever bought** (2023-06-29 and 2023-08-16, £159.00 each,
  [fleet Walksnail kit](../../../fleet/README.md#walksnail-kit-bought)) and **both are
  fitted**: one on the [5"](../../fpv-5/docs/bom.md), which is flight ready, and one on the
  [Swordfish](../../swordfish/README.md) canopy, repaired but not commissioned and
  **unassessed after two crashes**. There is no spare. So this needs the owner to choose
  between moving the Swordfish's kit (that aircraft is not flying, but the kit's condition
  is unknown), moving the 5"'s (which grounds the acro aircraft's video), or buying a
  third. **Nothing is decided and nothing should be assumed bought.**
  - **What it means for the airframe, all to be confirmed against the kit in hand.**
    Retailer and review pages for the Pro kit give a VTX of **33.5 × 33.5 × 10.5 mm** with
    **25.5 × 25.5 mm through-holes** and 20 × 20 mm tapped into the heatsink
    ([Oscar Liang](https://oscarliang.com/walksnail-avatar-hd-pro-v2-kit/),
    [Caddx](https://www.caddxfpv.com/products/walksnail-avatar-hd-pro-kit), read
    2026-09-17); these are 2026 listings, not the 2023 kit, and the kit is on another
    aircraft where it can be measured.
  - **It will not live on the flight-controller deck.** The deck's central bay is 27 mm
    between ribs ([`../print/sources.md`](../print/sources.md)), narrower than the VTX, and
    the VTX runs hot and wants clean airflow away from the board. The upper plate has four
    unused Ø3.4 anchors per side at (±50, ±23) and (±50, ±37) that suit a separate bracket.
  - **The camera makes [OQ-06](#) blocking.** A nose camera cannot be positioned until
    which edge of the plate faces forward is settled.

- **OQ-09 — Which vision camera for the Jetson, and from where?** (2026-09-17, owner).
  The companion computer ([OQ-03](#)) needs a camera for AI vision, separate from the FPV
  camera ([OQ-08](#)). The owner asked whether to repurpose the hexapod's RealSense and
  whether a camera of that age earns its weight. Findings, 2026-09-17:
  - **The airframe was already planned for one.** A **Holybro Depth Camera Mount for Intel
    RealSense** was bought with the frame on 2025-07-24 ([`bom.md`](bom.md), £12.90). The
    intent predates this conversation.
  - **Not the hexapod's.** Its D435i is in service and is that robot's
    [DEC-02](https://github.com/WayneKennedy/wk-hexapod/blob/main/docs/decisions.md) —
    it replaced the Pi camera *and* the ultrasonic, and RTAB-Map runs on it directly.
    Taking it stops a working robot, against the owner's stated goal of more finished
    projects.
  - **There is only one D435i in the house, and it is the hexapod's** (owner, 2026-09-17).
    The two RealSense cameras `wk-devastator` records as the tank's are the same physical
    D435i, since moved to the hexapod, plus one other. That other is part **82637BRPLHV**,
    which retailer listings identify as an **Intel RealSense T265 tracking camera**
    ([B&H](https://www.bhphotovideo.com/c/product/1560728-REG/intel_82637brplhv_intelrealsense_tracking_camerat265.html),
    [CDW](https://m.cdw.com/product/intel-realsense-t265-usb-3.1-gen-1-micro-b-tracking-camera/5639627),
    read 2026-09-17) — identified from the part number, not from the hardware.
    **`wk-devastator`'s sourcing record still implies both cameras are on the tank and
    needs correcting there.**
  - **So no depth camera is free.** Fitting depth to this aircraft means buying one, or
    taking the hexapod's and stopping that robot.
  - **Age is not the objection.** The D435i is ~72–75 g against Holybro's 1500 g payload
    ceiling, and D4xx active stereo **works better in bright light, not worse** — sunlight
    adds the texture the stereo matcher needs, the projector simply stops contributing
    ([Intel tuning guide](https://dev.intelrealsense.com/docs/tuning-depth-cameras-for-best-performance)).
    Glare pointing at the sun is the real caution, and baffling is the answer.
  - **The T265 does not help here, whatever its support status.** It emits pose, not
    depth: it cannot see a wall or a tree, so it does nothing for the requirement that
    makes depth essential. Beyond that it is discontinued, and
    [wk-robotics `common.md`](https://github.com/WayneKennedy/wk-robotics/blob/main/docs/common.md)
    already records it as "the only member that ran visual-inertial SLAM on-device …
    Discontinued. No current RealSense does on-device SLAM."
  - **The driver situation is the hard reason, and it checks out** (verified 2026-09-17).
    The T265 is an EOL product: **librealsense removed its code at v2.54.1**, and the last
    validated release supporting it is **v2.50.0**
    ([release notes](https://github.com/IntelRealSense/librealsense/wiki/Release-Notes),
    [v2.54.1](https://github.com/IntelRealSense/librealsense/releases/tag/v2.54.1)).
    Current JetPack ships far newer, and the hexapod already runs 2.58.1, so using a T265
    means pinning a 2022-era librealsense. The owner's recollection that it is worth
    nothing in 2026 was correct; **the reason had never been written down** — the failure
    the placement rule exists to prevent. Its one trick, GPS-denied pose, is served on this
    aircraft by GPS anyway.
  - **Settled by the owner 2026-09-17: depth and obstacle avoidance are essential.** The
    aircraft is not to be flown fast and must see walls and trees before hitting them. So
    both a depth camera and a global-shutter camera are in scope, not one or the other.
  - **ArduPilot's documented avoidance path names the D435i specifically.** Its
    [RealSense depth camera page](https://ardupilot.org/copter/docs/common-realsense-depth-camera.html)
    (read 2026-09-17) supports the **D435 and D435i**, "other Intel depth cameras may also
    work". A companion runs
    [`d4xx_to_mavlink.py`](https://github.com/rishabsingh3003/Vision-Obstacle-Avoidance),
    converting depth to **`OBSTACLE_DISTANCE`** (up to 72 sectors) at **~15 Hz**. Flight
    controller side: `SERIAL2_PROTOCOL 2`, `SERIAL2_BAUD 921`, `PRX1_TYPE 2`,
    `AVOID_ENABLE 7`, `AVOID_MARGIN 1.5`, `AVOID_BEHAVE 1` (stop), `AVOID_DIST_MAX 1.5`,
    `AVOID_ANG_MAX 30`. **The camera must face forward — other orientations are not
    supported**, so this covers forward flight only, not sideways drift.
  - **Integration risk, unverified.** That wiki recommends Ubuntu 18.04 and Python 3.6+,
    and the script came out of a 2020 GSoC project. JetPack on an Orin Nano is Ubuntu
    22.04. Expect work; do not assume it runs as written.
  - **Where stereo actually fails is not where it is expected to.** Tree trunks and
    textured or brick walls carry the texture the matcher needs and are the easy case. The
    two real holes are **smooth featureless walls in bright sun** — no texture, and the IR
    projector is washed out — and **thin branches and twigs**, which fall below the depth
    resolution at range. Slow flight and a generous `AVOID_MARGIN` are the mitigation.
  - **Global-shutter camera, nothing suitable owned** (checked 2026-09-17: the only free
    camera anywhere is the T265; the D435i is the hexapod's and the InnoMaker UVC pair is
    the SO-ARM101's, rolling-shutter USB 2). The fitting product is the **Arducam 2.3 MP
    AR0234 colour global shutter camera for Jetson AGX Orin / Orin Nano / Orin NX**,
    1920 × 1200, onboard ISP, **pre-validated on Orin Nano against NVIDIA's V4L2 drivers**
    — which is the point, because driver support per JetPack version is the usual trap
    with Jetson CSI cameras. Cheaper mono alternative: Arducam **OV9281** 1 MP global
    shutter.
  - **$110 plus shipping, and no UK stockist** (owner, 2026-09-17; searching confirms it).
    Arducam's franchised EMEA distributor is **EBV**, a trade distributor, and retail goes
    through **UCTRONICS** from China; [RobotShop UK](https://robotshop.com/uk/arducam.html)
    and [Botland](https://botland.store) (Poland) carry some Arducam lines. So the real
    cost is the sticker plus shipping, plus 20% import VAT on goods *and* shipping, plus a
    courier handling fee — materially above $110, and days to weeks of lead time.
  - **SKU trap.** Arducam sells an AR0234 module **B0429** for "Jetson Nano/Xavier NX and
    Orin NX" *and* a separate one for "AGX Orin / Orin Nano / Orin NX". The drivers are
    compiled per kernel, so **the Orin-series SKU is the one that matters here**; a reseller
    listing B0429 is not necessarily it.
  - **The D4xx line is not discontinued; only the tracking line is.** Intel's wind-down
    took the T265 and the L515, and the stereo D400 line survived: the D435i is a current
    product sold by **RealSense, Inc. "under license from Intel Corporation"** — the
    business is now independent of Intel ([D435i product page](https://www.realsenseai.com/products/depth-camera-d435i/),
    read 2026-09-17), and RS Online UK stocks it. Buying one is not buying into a dead
    line; reusing the T265 is.
  - **Prices, RS Online UK, read 2026-09-17, ex VAT:** RealSense **D435i £434.00**,
    **D455 £543.30**. **The D455 will not fit the mount already owned** — the Holybro
    depth-camera mount in [`bom.md`](bom.md) is sized for the 90 × 25 × 25 mm D435 body and
    the D455 is 124 mm long. A printed mount would be needed.
  - **The value alternative is a Luxonis OAK-D S2**, $329 at
    [Luxonis](https://shop.luxonis.com/products/oak-d-s2), UK through Amazon and RoboSavvy
    — roughly half a D435i. Its stereo pair is global shutter and it runs neural inference
    on-device, so **one device could cover both the depth requirement and the
    global-shutter camera**, saving the Arducam purchase as well. The cost is leaving
    ArduPilot's maintained `d4xx_to_mavlink.py` behind and writing the `OBSTACLE_DISTANCE`
    bridge against DepthAI instead. Not assessed.
  - **Open:** which physical depth unit gets bought;
    whether forward-only avoidance is enough or a second proximity source is wanted; and
    the payload and power budgets, still not done ([OQ-03](#)).

- **OQ-06 — Which edge of the upper plate is forward?** (2026-09-17). Holybro's frame
  STEP file is symmetric about both plate axes and marks no nose, so the CAD cannot say
  it. It decides which way the H743 faces on its deck ([DEC-02](decisions.md)) — the deck
  itself does not care, its boss pattern is square — and it decides
  `AHRS_ORIENTATION`. Settle it against the assembled airframe, or against the battery
  mount and GPS mast positions.

- **OQ-04 — Build state and the remaining parts** (2026-09-17). Whether the frame is
  assembled, and the receiver, video system and battery, are unrecorded
  ([`bom.md`](bom.md), [F-OQ-01](../../../fleet/open-questions.md)).
