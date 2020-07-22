from unittest import TestCase
import mock
from io import BytesIO as StringIO

from core.site_map import SiteMap, SquareType
from core.simulator_exceptions import (
    FILENOTEXIST,
    UNACCEPTABLESQUARE,
    EMPTYFILE,
    NOTAGRID
)


class TestSiteMap(TestCase):

    def set_up(self):
        pass

    def tear_down(Self):
        pass

    def test_init_valid_file(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        TestCase.assertEqual(self, test_siteMap.rows, 5)
        TestCase.assertEqual(self, test_siteMap.columns, 10)
        TestCase.assertEqual(self, test_siteMap.siteMap[0][1], SquareType.PLAIN)
        TestCase.assertEqual(self, test_siteMap.siteMap[0][2], SquareType.REMOVABLE_TREE)
        TestCase.assertEqual(self, test_siteMap.siteMap[2][7], SquareType.NONREMOVABLE_TREE)
        TestCase.assertEqual(self, test_siteMap.siteMap[4][0], SquareType.ROCK)

    def test_init_file_does_not_exist(self):
        with TestCase.assertRaises(self, Exception) as e:
            SiteMap("fake_path")
        TestCase.assertEqual(
            self,
            FILENOTEXIST.format("fake_path"),
            e.exception.message
        )

    def test_init_file_invalid(self):
        with TestCase.assertRaises(self, Exception) as e:
            SiteMap("./test/fixtures/invalid_sample1.txt")
        TestCase.assertEqual(
            self,
            UNACCEPTABLESQUARE.format('M'),
            e.exception.message
        )
        with TestCase.assertRaises(self, Exception) as e:
            SiteMap("./test/fixtures/invalid_sample2.txt")
        TestCase.assertEqual(
            self,
            NOTAGRID,
            e.exception.message
        )
        with TestCase.assertRaises(self, Exception) as e:
            SiteMap("./test/fixtures/invalid_sample3.txt")
        TestCase.assertEqual(
            self,
            EMPTYFILE,
            e.exception.message
        )

    def test_show_site_map(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        expectedPrintOut = ["  -----------------------------------------------------------------  ",
                            "o\to\tt\to\to\to\to\to\to\to",
                            "o\to\to\to\to\to\to\tT\to\to",
                            "r\tr\tr\to\to\to\to\tT\to\to",
                            "r\tr\tr\tr\to\to\to\to\to\to",
                            "r\tr\tr\tr\tr\tt\to\to\to\to",
                            "",
                            "  -----------------------------------------------------------------  "]
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            test_siteMap.show()
            printedLines = fake_out.getvalue().splitlines()
            for i in range(len(expectedPrintOut)):
                TestCase.assertEqual(self, printedLines[i], expectedPrintOut[i])

    def test_get_square_type(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        TestCase.assertEqual(self, test_siteMap.getSquareType('o'), SquareType.PLAIN)
        TestCase.assertEqual(self, test_siteMap.getSquareType('r'), SquareType.ROCK)
        TestCase.assertEqual(self, test_siteMap.getSquareType('t'), SquareType.REMOVABLE_TREE)
        TestCase.assertEqual(self, test_siteMap.getSquareType('T'), SquareType.NONREMOVABLE_TREE)
        TestCase.assertEqual(self, test_siteMap.getSquareType('*'), SquareType.CLEAR)
        with TestCase.assertRaises(self, Exception) as e:
            test_siteMap.getSquareType('e')
        TestCase.assertEqual(
            self,
            UNACCEPTABLESQUARE.format('e'),
            e.exception.message
        )

    def test_get_clearable_squares(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        TestCase.assertEqual(self, test_siteMap.getClearableSquares(), 48)

    def test_is_valid(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        TestCase.assertEqual(self, test_siteMap.isValid(0, 0), True)
        TestCase.assertEqual(self, test_siteMap.isValid(0, 9), True)
        TestCase.assertEqual(self, test_siteMap.isValid(4, 0), True)
        TestCase.assertEqual(self, test_siteMap.isValid(4, 9), True)
        TestCase.assertEqual(self, test_siteMap.isValid(-1, 1), False)
        TestCase.assertEqual(self, test_siteMap.isValid(2, 11), False)
