from unittest import TestCase
import mock
from io import BytesIO as StringIO

from core.site_map import SiteMap
from core.bulldozer import Bulldozer, CommandType, Location, Direction
from core.expense import CostItem


class TestSiteMap(TestCase):
    def set_up(self):
        pass

    def tear_down(Self):
        pass

    def test_get_command_type(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("left"), CommandType.TURN_LEFT)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("l"), CommandType.TURN_LEFT)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("right"), CommandType.TURN_RIGHT)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("r"), CommandType.TURN_RIGHT)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("advance 10"), CommandType.ADVANCE)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("a 10"), CommandType.ADVANCE)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("quit"), CommandType.QUIT)
        TestCase.assertEqual(self, test_bulldozer.getCommandType("q"), CommandType.QUIT)

    def test_advance_on_plain_land(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.location = Location(1, 2)
        test_bulldozer.direction = Direction.EAST
        test_bulldozer.advance(2)
        TestCase.assertEqual(self, test_bulldozer.location.row, 1)
        TestCase.assertEqual(self, test_bulldozer.location.column, 4)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 2)

    def test_advance_on_rocky_land(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.location = Location(4, 1)
        test_bulldozer.direction = Direction.EAST
        test_bulldozer.advance(2)
        TestCase.assertEqual(self, test_bulldozer.location.row, 4)
        TestCase.assertEqual(self, test_bulldozer.location.column, 3)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 4)

    def test_advance_on_removable_tree(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.location = Location(0, 1)
        test_bulldozer.direction = Direction.EAST
        # pass a tree and a plain land without stopping:
        test_bulldozer.advance(2)
        TestCase.assertEqual(self, test_bulldozer.location.row, 0)
        TestCase.assertEqual(self, test_bulldozer.location.column, 3)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 3)
        # should incur paint damage
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.PAINT_DAMAGE], 1)

        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.location = Location(0, 1)
        test_bulldozer.direction = Direction.EAST
        # Visit the tree, stop, and continue on a plain land:
        test_bulldozer.advance(1)
        test_bulldozer.advance(1)
        TestCase.assertEqual(self, test_bulldozer.location.row, 0)
        TestCase.assertEqual(self, test_bulldozer.location.column, 3)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 3)
        # Should not incur paint damage
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.PAINT_DAMAGE], 0)

    @mock.patch('core.bulldozer.Bulldozer.terminate')
    def test_advance_on_protected_tree(self, mock_terminate):
        mock_terminate.return_value = None
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.location = Location(2, 6)
        test_bulldozer.direction = Direction.EAST
        test_bulldozer.advance(1)
        # It should terminate at the next square, because the next square block is a protected tree
        TestCase.assertEqual(self, test_bulldozer.location.row, 2)
        TestCase.assertEqual(self, test_bulldozer.location.column, 7)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 0)

    def test_apply_command_advance(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.applyCommand('a 5')
        TestCase.assertEqual(self, test_bulldozer.location.row, 0)
        TestCase.assertEqual(self, test_bulldozer.location.column, 4)
        # One of the square blocks is a tree, the others are plain land
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 6)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.PAINT_DAMAGE], 1)
        TestCase.assertEqual(self, test_bulldozer.history[-1], "Advance 5")

    @mock.patch('core.bulldozer.Bulldozer.terminate')
    def test_apply_command_advance_out_of_site(self, mock_terminate):
        mock_terminate.return_value = None
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.applyCommand('a 20')
        TestCase.assertEqual(self, test_bulldozer.location.row, 0)
        TestCase.assertEqual(self, test_bulldozer.location.column, 9)
        # One of the square blocks is a tree, the others are plain land
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 11)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.PAINT_DAMAGE], 1)
        TestCase.assertEqual(self, test_bulldozer.history[-1], "Advance 20")

    def test_apply_command_turn_left(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.applyCommand('l')
        TestCase.assertEqual(self, test_bulldozer.location.row, 0)
        TestCase.assertEqual(self, test_bulldozer.location.column, -1)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 0)
        TestCase.assertEqual(self, test_bulldozer.history[-1], "Turn left")

    def test_apply_command_turn_right(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.applyCommand('r')
        TestCase.assertEqual(self, test_bulldozer.location.row, 0)
        TestCase.assertEqual(self, test_bulldozer.location.column, -1)
        TestCase.assertEqual(self, test_bulldozer.expense.costQuantity[CostItem.FUEL], 0)
        TestCase.assertEqual(self, test_bulldozer.history[-1], "Turn right")

    def test_generate_report(self):
        test_siteMap = SiteMap("./test/fixtures/sample1.txt")
        test_bulldozer = Bulldozer(test_siteMap)
        test_bulldozer.applyCommand('a 4')
        test_bulldozer.applyCommand('r')
        test_bulldozer.applyCommand('a 2')
        expectedReport = ["",
                          "These are the commands you issued:",
                          "",
                          "Advance 4, Turn right, Advance 2",
                          "",
                          "The costs for this land clearing operation were:",
                          "",
                          "Item                                       Quantity                 Cost",
                          "communication overhead                            3                    3",
                          "fuel usage                                        7                    7",
                          "uncleared squares                                42                  126",
                          "destruction of protected tree                     0                    0",
                          "paint damage to bulldozer                         1                    2",
                          "-----------------------------                                           ",
                          "Total                                                                138"]
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            test_bulldozer.generateReport()
            printedLines = fake_out.getvalue().splitlines()
            for i in range(len(expectedReport)):
                TestCase.assertEqual(self, printedLines[i], expectedReport[i])
