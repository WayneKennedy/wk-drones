#!/usr/bin/env python3
"""Read, set, dump and watch ArduPilot parameters over MAVLink, from the bench.

For any aircraft in the fleet on ArduPilot, over USB (or any pymavlink connection
string). The ground station must not hold the port at the same time. Nothing here arms,
reboots or writes anything but the parameters named on the command line.

    uv run --with pymavlink python fleet/tools/ap-params.py version
    uv run --with pymavlink python fleet/tools/ap-params.py get FLOW_POS_Z RNGFND1_GNDCLR
    uv run --with pymavlink python fleet/tools/ap-params.py set FLOW_POS_Z=0.04 RNGFND1_GNDCLR=0.05
    uv run --with pymavlink python fleet/tools/ap-params.py dump out.params "Board: ... note"
    uv run --with pymavlink python fleet/tools/ap-params.py watch DISTANCE_SENSOR OPTICAL_FLOW --seconds 5

`--port` defaults to /dev/ttyACM0 at 115200. `dump` writes QGroundControl's .params
layout (header, then "sysid compid NAME VALUE TYPE" per line), the same as the files in
aircraft/*/config/dump/, with ArduPilot's version and git hash in the header.
`set` writes each parameter, reads it back, and fails if the readback differs.
"""

import argparse
import sys
import time

from pymavlink import mavutil


def connect(port, baud):
    m = mavutil.mavlink_connection(port, baud=baud)
    m.wait_heartbeat(timeout=10)
    return m


def version(m):
    m.mav.command_long_send(m.target_system, m.target_component,
                            mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE, 0,
                            mavutil.mavlink.MAVLINK_MSG_ID_AUTOPILOT_VERSION, 0, 0, 0, 0, 0, 0)
    v = m.recv_match(type="AUTOPILOT_VERSION", blocking=True, timeout=5)
    if v is None:
        return "AUTOPILOT_VERSION: no reply"
    fw = v.flight_sw_version
    ver = f"{(fw >> 24) & 0xff}.{(fw >> 16) & 0xff}.{(fw >> 8) & 0xff}"
    git = bytes(v.flight_custom_version).decode(errors="ignore").strip("\x00")
    return ver, git


def get(m, names):
    out = {}
    for n in names:
        m.param_fetch_one(n)
        r = m.recv_match(type="PARAM_VALUE", blocking=True, timeout=5)
        while r is not None and r.param_id != n:
            r = m.recv_match(type="PARAM_VALUE", blocking=True, timeout=5)
        out[n] = None if r is None else (r.param_value, r.param_type)
    return out


def set_params(m, assignments):
    results = []
    for a in assignments:
        name, value = a.split("=", 1)
        before = get(m, [name])[name]
        if before is None:
            raise SystemExit(f"{name}: not on this vehicle")
        value = float(value)
        m.param_set_send(name, value, before[1])
        r = m.recv_match(type="PARAM_VALUE", blocking=True, timeout=5)
        while r is not None and r.param_id != name:
            r = m.recv_match(type="PARAM_VALUE", blocking=True, timeout=5)
        after = get(m, [name])[name]
        ok = after is not None and abs(after[0] - value) < 1e-6
        results.append((name, before[0], after[0] if after else None, ok))
        if not ok:
            raise SystemExit(f"{name}: wrote {value}, read back {after}")
    return results


def fetch_all(m):
    m.param_fetch_all()
    params, total, last = {}, None, time.time()
    while True:
        r = m.recv_match(type="PARAM_VALUE", blocking=True, timeout=3)
        if r is None:
            if time.time() - last > 3:
                break
            continue
        last = time.time()
        total = r.param_count
        params[r.param_id] = (r.param_value, r.param_type, r.param_index)
        if total and len(params) >= total:
            break
    if total and len(params) < total:
        # ask for the ones that were missed
        have = {v[2] for v in params.values()}
        for i in range(total):
            if i not in have:
                m.mav.param_request_read_send(m.target_system, m.target_component, b"", i)
                r = m.recv_match(type="PARAM_VALUE", blocking=True, timeout=3)
                if r is not None:
                    params[r.param_id] = (r.param_value, r.param_type, r.param_index)
    return params, total


def fmt(v, t):
    """Floats at 9 significant figures, as QGroundControl writes them, so dumps diff cleanly."""
    if t in (9, 10):
        return f"{float(v):.9g}"
    return str(int(round(v)))


def dump(m, path, note):
    ver, git = version(m)
    params, total = fetch_all(m)
    if total is None or len(params) != total:
        raise SystemExit(f"got {len(params)} of {total} parameters; not saving")
    with open(path, "w") as f:
        f.write("# Onboard parameters for Vehicle 1\n#\n# Stack: ArduPilot\n# Vehicle: Multi-Rotor\n"
                f"# Version: {ver} \n# Git Revision: {git}\n# {note}\n#\n"
                "# Vehicle-Id Component-Id Name Value Type\n")
        for name in sorted(params):
            v, t, _ = params[name]
            f.write(f"1\t1\t{name}\t{fmt(v, t)}\t{t}\n")
    return ver, git, len(params)


def watch(m, types, seconds):
    end = time.time() + seconds
    seen = {}
    while time.time() < end:
        r = m.recv_match(type=types, blocking=True, timeout=1)
        if r is not None:
            seen[r.get_type()] = r
    for t in types:
        print(t, "->", seen[t].to_dict() if t in seen else "nothing received")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", default="/dev/ttyACM0")
    p.add_argument("--baud", type=int, default=115200)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("version")
    sub.add_parser("get").add_argument("names", nargs="+")
    sub.add_parser("set").add_argument("assignments", nargs="+", metavar="NAME=VALUE")
    d = sub.add_parser("dump"); d.add_argument("path"); d.add_argument("note")
    w = sub.add_parser("watch"); w.add_argument("types", nargs="+"); w.add_argument("--seconds", type=float, default=5)
    a = p.parse_args()
    m = connect(a.port, a.baud)
    if a.cmd == "version":
        print(version(m))
    elif a.cmd == "get":
        for n, v in get(m, a.names).items():
            print(n, "=", "not on this vehicle" if v is None else fmt(*v))
    elif a.cmd == "set":
        for name, before, after, ok in set_params(m, a.assignments):
            print(f"{name}: {before} -> {after} {'ok' if ok else 'MISMATCH'}")
    elif a.cmd == "dump":
        ver, git, n = dump(m, a.path, a.note)
        print(f"saved {n} parameters from ArduPilot {ver} ({git}) to {a.path}")
    elif a.cmd == "watch":
        watch(m, a.types, a.seconds)
    m.close()


if __name__ == "__main__":
    main()
