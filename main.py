"""Check clock drift against NTP per host.

Usage: python3 main.py clocks.csv [--warn-ms 100] [--critical-ms 500]
CSV columns: host,offset_ms,stratum. offset_ms is the signed
offset from the NTP server in milliseconds (negative means the
clock is behind). Verdicts, on the absolute offset:
- IN SYNC: at or under --warn-ms (default 100).
- DRIFTING: over --warn-ms up to and including --critical-ms
  (default 500).
- OUT OF SYNC: over --critical-ms.
Largest absolute offset first.
"""
import argparse, csv, sys

def check(rows, warn_ms=100, critical_ms=500):
    out = []
    for row in rows:
        host = row["host"].strip()
        offset = int(row["offset_ms"])
        stratum = int(row["stratum"])
        magnitude = abs(offset)
        if magnitude > critical_ms:
            verdict = "OUT OF SYNC"
        elif magnitude > warn_ms:
            verdict = "DRIFTING"
        else:
            verdict = "IN SYNC"
        out.append((host, offset, stratum, verdict))
    return sorted(out, key=lambda r: (-abs(r[1]), r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--warn-ms", type=int, default=100)
    parser.add_argument("--critical-ms", type=int, default=500)
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = check(list(csv.DictReader(f)), args.warn_ms, args.critical_ms)
    for host, offset, stratum, verdict in results:
        print(f"{host}: {verdict} - offset {offset} ms (stratum {stratum})")
    counts = {v: sum(1 for *_, verdict in results if verdict == v)
              for v in ("OUT OF SYNC", "DRIFTING", "IN SYNC")}
    if results:
        worst = results[0]
        print(f"{counts['OUT OF SYNC']} out of sync, {counts['DRIFTING']} drifting, "
              f"{counts['IN SYNC']} in sync out of {len(results)} host(s). "
              f"Worst drift: {worst[0]} ({worst[1]} ms).")
    else:
        print("No hosts found.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
