import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check

def row(host, offset, stratum):
    return {"host": host, "offset_ms": str(offset), "stratum": str(stratum)}

class TestClockDrift(unittest.TestCase):
    def test_in_sync(self):
        r = check([row("h", 12, 2)])
        self.assertEqual(r[0][3], "IN SYNC")

    def test_exactly_warn_is_in_sync(self):
        r = check([row("h", 100, 2)])
        self.assertEqual(r[0][3], "IN SYNC")

    def test_just_over_warn_is_drifting(self):
        r = check([row("h", 101, 2)])
        self.assertEqual(r[0][3], "DRIFTING")

    def test_exactly_critical_is_drifting(self):
        r = check([row("h", 500, 2)])
        self.assertEqual(r[0][3], "DRIFTING")

    def test_over_critical_is_out_of_sync(self):
        r = check([row("h", 501, 2)])
        self.assertEqual(r[0][3], "OUT OF SYNC")

    def test_negative_offset_uses_absolute_value(self):
        r = check([row("h", -812, 4)])
        self.assertEqual(r[0][3], "OUT OF SYNC")

    def test_largest_offset_first(self):
        r = check([row("a", 45, 2), row("b", -812, 4), row("c", 342, 3)])
        self.assertEqual([x[0] for x in r], ["b", "c", "a"])

    def test_empty_input(self):
        self.assertEqual(check([]), [])
