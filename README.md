# ntp-clock-drift-checker

Check clock drift against NTP per host: the input CSV lists host, offset_ms (signed offset from the NTP server in milliseconds — negative means the clock is behind) and stratum — IN SYNC at or under --warn-ms (default 100), DRIFTING over --warn-ms up to and including --critical-ms (default 500), OUT OF SYNC over --critical-ms — largest absolute offset first, with the worst drift named in the summary.

Sample input is included (sample.csv with five hosts).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
ws-03: OUT OF SYNC - offset -812 ms (stratum 4)
ws-02: DRIFTING - offset 342 ms (stratum 3)
ws-01: IN SYNC - offset 87 ms (stratum 3)
srv-db01: IN SYNC - offset 45 ms (stratum 2)
ntp-01: IN SYNC - offset 12 ms (stratum 2)
1 out of sync, 1 drifting, 3 in sync out of 5 host(s). Worst drift: ws-03 (-812 ms).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
