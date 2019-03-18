import unittest
import tempfile
from ..config_editor import *


class TestParser(unittest.TestCase):

    def setUp(self):
        self.parser = parser_creator()
        self.file = tempfile.NamedTemporaryFile()
        self.config = tempfile.NamedTemporaryFile()
        self.output = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.file.close()
        self.config.close()
        self.output.close()

    def test_with_invalid_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args([__name__, '-k'])
        self.assertEqual(cm.exception.code, 2)

    def test_with_no_config_file(self):
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args([__name__, '-f'])
        self.assertEqual(cm.exception.code, 2)

    def test_with_no_changes_file(self):
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args([__name__, '-c'])
        self.assertEqual(cm.exception.code, 2)

    def test_with_invalid_config_file(self):
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args([__name__, '-f', './doesnotexitfile.json', '-c', './tests.py'])
        self.assertEqual(cm.exception.code, 2)

    def test_with_invalid_changes_file(self):
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args([__name__, '-f', './test.py', '-c', './doesnotexistfile.txt'])
        self.assertEqual(cm.exception.code, 2)

    def test_with_valid_arguments(self):
        args = self.parser.parse_args(["-f%s" % self.file.name, "-c%s" % self.config.name])
        self.assertEqual(args.file.name, self.file.name)
        self.assertEqual(args.changes.name, self.config.name)
        self.assertEqual(args.output, sys.stdout)
        self.assertEqual(args.force_create, False)

    def test_with_valid_output(self):
        args = self.parser.parse_args(["-f%s" % self.file.name, "-c%s" % self.config.name, "-o%s" % self.output.name])
        self.assertEqual(args.file.name, self.file.name)
        self.assertEqual(args.changes.name, self.config.name)
        self.assertEqual(args.output.name, self.output.name)
        self.assertEqual(args.force_create, False)

    def test_with_path_create(self):
        args = self.parser.parse_args(["-f%s" % self.file.name, "-c%s" % self.config.name, "-p"])
        self.assertEqual(args.file.name, self.file.name)
        self.assertEqual(args.changes.name, self.config.name)
        self.assertEqual(args.force_create, True)


class TestLoadJsonConfig(unittest.TestCase):

    def setUp(self):
        self.file = tempfile.NamedTemporaryFile()
        self.file.file.write(b"""{}""")
        self.file.file.seek(0)
        self.config = tempfile.NamedTemporaryFile()
        self.config.file.write(b"""
        line1: some:test
        line2: some:test
        """)

    def tearDown(self):
        self.file.close()
        self.config.close()

    def test_load_invalid_json(self):
        self.config.file.seek(0)
        with self.assertRaises(json.decoder.JSONDecodeError) as cm:
            value = load_json_config(self.config.file)

    def test_load_valid_json(self):
        self.file.file.seek(0)
        value = load_json_config(self.file.file)
        self.assertDictEqual(value, {})


class TestReadLineByLine(unittest.TestCase):
    def setUp(self):
        self.testfile = tempfile.NamedTemporaryFile()
        self.testfile.file.write(b"""line1: some:test\nline2: some:test""")
        self.testfile.file.seek(0)

    def tearDown(self):
        self.testfile.close()

    def test_iterate_on_each_line(self):
        it = read_line_by_line(self.testfile.file)
        line1 = it.__next__()
        self.assertEqual(line1, b"line1: some:test\n")
        line1 = it.__next__()
        self.assertEqual(line1, b"line2: some:test")
        with self.assertRaises(StopIteration) as e:
            it.__next__()


class TestGetUpdateOrCreateValue(unittest.TestCase):

    def test_update_value(self):
        obj = {'a': {'deep': {'path': 42}}}
        path = 'a.deep.path'
        value = 44
        get_update_or_create_value(obj, path, value)
        self.assertEqual(obj['a']['deep']['path'], 44)

    def test_fail_update_invalid_path_subelement(self):
        obj = {'a': {'deep': {'path': 42}}}
        path = 'a.deep2.path'
        value = 44
        with self.assertRaises(KeyError):
            get_update_or_create_value(obj, path, value, force_create=False)

    def test_success_update_invalid_path_subelement(self):
        obj = {'a': {'deep': {'path': 42}}}
        path = 'a.deep2.path'
        value = 44
        get_update_or_create_value(obj, path, value, force_create=True)
        self.assertEqual(obj['a']['deep2']['path'], 44)
        self.assertEqual(obj['a']['deep']['path'], 42)


if __name__ == '__main__':
    unittest.main()
