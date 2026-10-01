# Ground station (ArduPilot)

The PC tool for configuring an ArduPilot flight controller is a ground control station
(GCS). It is the counterpart of the Betaflight and iNav Configurators: setup,
calibration, firmware flashing, the full parameter list and live readings (MAVLink
Inspector). Used on the bench only; aircraft fly on radio and goggles alone (Bee35
[`setup-ardupilot.md`](../aircraft/bee35/docs/setup-ardupilot.md)).

- **QGroundControl** — Linux, Windows, macOS, mobile. The fleet's Linux GCS.
- **Mission Planner** — ArduPilot's own, the most complete; Windows only.

## QGroundControl on Ubuntu 24.04

Done on the owner's Linux desktop 2026-09-22 with QGroundControl v5.1.4 (latest release,
2026-08-30). Installed, and working the same day: it connected to the Bee35's FC on
`/dev/ttyACM0` and flashed ArduCopter 4.7.1 to it. In v5.1 the setup pages (Firmware,
Frame, Parameters, Motors) are under Q menu → **Configure**; the Fly view stays locked
until required setup is complete, so live attitude is read in Analyze → MAVLink Inspector.

1. `sudo usermod -aG dialout $USER`, then log out and in. Without it the FC's
   `/dev/ttyACM0` (root:dialout, 0660) cannot be opened.
2. `sudo apt remove modemmanager` — it probes new serial devices and interferes with
   the FC link. Removing it took no other package.
3. `sudo apt install libfuse2t64 gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl` —
   `libfuse2t64` runs the AppImage (24.04's name for `libfuse2`); gstreamer serves video.
4. `QGroundControl-x86_64.AppImage` from
   [GitHub releases](https://github.com/mavlink/qgroundcontrol/releases) into
   `~/Applications/`, `chmod +x`, run. Until the re-login in step 1, run it as
   `sg dialout -c ~/Applications/QGroundControl-x86_64.AppImage` for the group access.
   Logging out may not be enough: if a tmux server or other process keeps the systemd
   user manager alive, the new desktop session (and anything launched from it, Files
   included) inherits the old groups. Seen 2026-09-22; a reboot clears it.
   Check a running process with `grep Groups /proc/<pid>/status` (dialout is GID 20
   on Ubuntu).

**USB check:** the MicoAir743 V2 enumerates as `1209:5741 Generic MicoAir743v2` and
appears as `/dev/ttyACM0` (seen 2026-09-22). If `lsusb` does not show it, suspect a
charge-only cable.

## From the terminal, without a GCS

[`tools/ap-params.py`](tools/ap-params.py) reads, sets, dumps and watches an ArduPilot
aircraft over USB with pymavlink (`uv run --with pymavlink python fleet/tools/ap-params.py
--help`). It writes `config/dump/` files in QGroundControl's layout, with the firmware
version and git hash in the header, and refuses to keep a dump that is not every
parameter. The GCS must be disconnected first; the two cannot share the port. First used
2026-10-01 on the Bee35 (its `config/diff/2026-10-01-flow-position.txt`).

## Phones and the MicoAir743 V2's Bluetooth

Checked 2026-10-01, when the owner asked for an iPhone app:

- **MicoAir publishes no phone app.** Its documented wireless path is **QGroundControl on
  Android** over the board's own Bluetooth (internally UART8, 115200; it broadcasts as
  `MicoAir743v2-xxxxx`, no pairing code; the board's Bluetooth LED goes solid when
  connected). Source: [MicoAir743v2 page](https://micoair.com/flightcontroller_micoair743v2/)
  and the [H743 V2 manual](https://docs.robofusion.net/flight-controllers/h743-v2-user-manual).
  MicoAssistant, for the MTF-01P, is a Windows program.
- **An iPhone cannot use that Bluetooth.** QGroundControl's Bluetooth link needs the Serial
  Port Profile, which iOS does not offer, and QGC has no BLE link; QGC on iOS connects over
  Wi-Fi (TCP/UDP) only — ArduPilot forum threads
  [74792](https://discuss.ardupilot.org/t/no-bluetooth-support-on-ios-version-of-qgroundcontrol/74792)
  and [41737](https://discuss.ardupilot.org/t/some-advice-for-qgc-ios-version/41737). So an
  iPhone needs a Wi-Fi MAVLink bridge on a spare UART, or the ELRS MAVLink route the Bee35's
  OQ-02 holds open; neither is set up or decided.
- The owner has no Android phone on record; whether one is owned is not known here.
