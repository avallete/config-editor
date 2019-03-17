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


if __name__ == '__main__':
    unittest.main()
