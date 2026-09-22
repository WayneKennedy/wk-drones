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
