import unittest
from upackage.upackage import UPackage


class UPackageTestCase(unittest.TestCase):

    def test_get_path_no_extension_when_one_ext(self):
        path = "some/file/path/here.txt"
        path_no_ext = UPackage._get_file_path_no_extensions(path)

        assert path_no_ext == "some/file/path/here"

    def test_get_path_no_extension_when_two_ext(self):
        path = "some/file/path/here.thing.txt"
        path_no_ext = UPackage._get_file_path_no_extensions(path)

        assert path_no_ext == "some/file/path/here.thing"

    def test_get_path_no_extension_when_three_ext(self):
        path = "some/file/path/here.thing.txt.other"
        path_no_ext = UPackage._get_file_path_no_extensions(path)

        assert path_no_ext == "some/file/path/here.thing.txt"