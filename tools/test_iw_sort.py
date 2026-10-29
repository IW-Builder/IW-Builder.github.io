"""Tests for iw_sort.py. Run: python -m unittest test_iw_sort.py"""

import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest import mock

import iw_sort


def make_world():
    return {
        "title": "Test",
        "possibleCharacters": [{"name": "Ann", "characterId": "a"}, {"name": "Bo", "characterId": "b"}],
        "NPCs": [{"id": "n1", "name": "Cy", "positionInList": 0},
                 {"id": "n2", "name": "Dee", "positionInList": 1},
                 {"id": "n3", "name": "", "positionInList": 2}],
        "triggerEvents": [{"id": "t1", "name": "Dup"}, {"id": "t2", "name": "Other"},
                          {"id": "t3", "name": "Dup"}],
        "trackedItems": [{"id": "k1", "name": "X", "positionInList": 0},
                         {"id": "k2", "name": "Y", "positionInList": 1}],
        "other": {"untouched": [3, 2, 1]},
    }


class SortTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.world_path = self.path("w.json")
        with open(self.world_path, "w", encoding="utf-8") as f:
            json.dump(make_world(), f, indent=2)

    def tearDown(self):
        self.dir.cleanup()

    def path(self, name):
        return os.path.join(self.dir.name, name)

    def run_main(self, *args):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            iw_sort.main(list(args))
        return err.getvalue()

    def apply_text(self, text):
        order = self.path("o.txt")
        with open(order, "w", encoding="utf-8") as f:
            f.write(text)
        out = self.path("out.json")
        if os.path.exists(out):
            os.remove(out)
        warnings = self.run_main("apply", self.world_path, order, "-o", out)
        with open(out, encoding="utf-8") as f:
            return json.load(f), warnings

    def test_round_trip_is_identical(self):
        self.run_main("export", self.world_path)
        order = self.path("w.order.txt")
        self.run_main("apply", self.world_path, order)
        with open(self.world_path) as a, open(self.path("w.sorted.json")) as b:
            self.assertEqual(a.read(), b.read())

    def test_reorder_and_positions(self):
        world, _ = self.apply_text("[Other Characters]\n<unnamed>\nDee\nCy\n[Trackers]\nY\nX\n")
        self.assertEqual([n["id"] for n in world["NPCs"]], ["n3", "n2", "n1"])
        self.assertEqual([n["positionInList"] for n in world["NPCs"]], [0, 1, 2])
        self.assertEqual([t["id"] for t in world["trackedItems"]], ["k2", "k1"])
        self.assertEqual([t["positionInList"] for t in world["trackedItems"]], [0, 1])
        # Sections not in the file are left alone.
        self.assertEqual(world["possibleCharacters"], make_world()["possibleCharacters"])
        self.assertEqual(world["other"], make_world()["other"])

    def test_duplicates_keep_relative_order(self):
        world, _ = self.apply_text("[Triggers]\nDup\nOther\nDup\n")
        self.assertEqual([t["id"] for t in world["triggerEvents"]], ["t1", "t2", "t3"])
        world, _ = self.apply_text("[Triggers]\nOther\nDup\nDup\n")
        self.assertEqual([t["id"] for t in world["triggerEvents"]], ["t2", "t1", "t3"])

    def test_missing_unknown_and_extra_lines_never_drop_data(self):
        world, warnings = self.apply_text(
            "# comment\r\n[triggers]\r\nOther\r\nNope\r\nOther\r\n[Bogus]\r\nZ\r\n")
        self.assertEqual([t["id"] for t in world["triggerEvents"]], ["t2", "t1", "t3"])
        self.assertIn("'Nope' is not in the world", warnings)
        self.assertIn("listed more times than it exists", warnings)
        self.assertIn("missing from the text file", warnings)
        self.assertIn("unknown section [Bogus]", warnings)

    def test_refuses_to_overwrite(self):
        self.run_main("export", self.world_path)
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            iw_sort.main(["export", self.world_path])
        with self.assertRaises(SystemExit):
            iw_sort.main(["apply", self.world_path, self.path("w.order.txt"), "-o", self.world_path])


class AutoTest(unittest.TestCase):
    """Running with no arguments picks the mode from the files in the folder."""

    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.dir.name)

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.dir.cleanup()

    def write_world(self, name):
        with open(name, "w", encoding="utf-8") as f:
            json.dump(make_world(), f, indent=2)

    def run_auto(self, answers=()):
        answers = iter(answers)
        with mock.patch("builtins.input", lambda prompt="": next(answers, "")), \
                contextlib.redirect_stdout(io.StringIO()) as out, \
                contextlib.redirect_stderr(io.StringIO()) as err, \
                self.assertRaises(SystemExit) as exit_:
            iw_sort.main([])
        return exit_.exception.code, out.getvalue() + err.getvalue()

    def test_one_world_exports_then_sorts(self):
        self.write_world("w.json")
        code, _ = self.run_auto()
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists("w.order.txt"))
        # The second run finds the text file and sorts; its own output is not a candidate.
        code, _ = self.run_auto()
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists("w.sorted.json"))
        code, out = self.run_auto(["n"])
        self.assertIn("nothing written", out)

    def test_world_with_text_file_wins_and_plain_txt_matches(self):
        self.write_world("a.json")
        self.write_world("b.json")
        with open("b.txt", "w", encoding="utf-8") as f:
            f.write("[Trackers]\nY\nX\n")
        self.run_auto()
        with open("b.sorted.json", encoding="utf-8") as f:
            self.assertEqual([t["id"] for t in json.load(f)["trackedItems"]], ["k2", "k1"])

    def test_several_worlds_ask(self):
        self.write_world("a.json")
        self.write_world("b.json")
        with open("notes.json", "w") as f:
            f.write("[1, 2]")
        code, out = self.run_auto(["2"])
        self.assertNotIn("notes.json", out)
        self.assertTrue(os.path.exists("b.order.txt"))
        self.assertFalse(os.path.exists("a.order.txt"))


if __name__ == "__main__":
    unittest.main()
