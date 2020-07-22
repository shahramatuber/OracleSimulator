from unittest import TestCase
import mock
from io import BytesIO as StringIO

from core.expense import Expense, CostItem
from core.site_map import SquareType


class TestExpense(TestCase):
    def set_up(self):
        pass

    def tear_down(Self):
        pass

    def test_add_communication_overhead(self):
        fakeExpense = Expense(10)
        fakeExpense.addCommunicationOverhead()
        expectedCostQuantity = {
            CostItem.COMMUNICATION: 1,
            CostItem.FUEL: 0,
            CostItem.UNCLEARD_SQUARE: 10,
            CostItem.PROTECTED_TREE_DESTRUCTION: 0,
            CostItem.PAINT_DAMAGE: 0
        }
        TestCase.assertDictEqual(self, fakeExpense.costQuantity, expectedCostQuantity)

    def test_remove_uncleared_square(self):
        fakeExpense = Expense(10)
        fakeExpense.removeUnclearedSquare()
        expectedCostQuantity = {
            CostItem.COMMUNICATION: 0,
            CostItem.FUEL: 0,
            CostItem.UNCLEARD_SQUARE: 9,
            CostItem.PROTECTED_TREE_DESTRUCTION: 0,
            CostItem.PAINT_DAMAGE: 0
        }
        TestCase.assertDictEqual(self, fakeExpense.costQuantity, expectedCostQuantity)

    def test_add_protected_tree_destruction(self):
        fakeExpense = Expense(10)
        fakeExpense.addProtectedTreeDestruction()
        expectedCostQuantity = {
            CostItem.COMMUNICATION: 0,
            CostItem.FUEL: 0,
            CostItem.UNCLEARD_SQUARE: 10,
            CostItem.PROTECTED_TREE_DESTRUCTION: 1,
            CostItem.PAINT_DAMAGE: 0
        }
        TestCase.assertDictEqual(self, fakeExpense.costQuantity, expectedCostQuantity)

    def test_update_fuel_consumption(self):
        fakeExpense = Expense(10)
        squareType = SquareType.ROCK
        fakeExpense.updateFuelConsumption(squareType)
        expectedCostQuantity = {
            CostItem.COMMUNICATION: 0,
            CostItem.FUEL: 2,
            CostItem.UNCLEARD_SQUARE: 10,
            CostItem.PROTECTED_TREE_DESTRUCTION: 0,
            CostItem.PAINT_DAMAGE: 0
        }
        TestCase.assertDictEqual(self, fakeExpense.costQuantity, expectedCostQuantity)

    def test_add_paint_damage(self):
        fakeExpense = Expense(10)
        fakeExpense.addPaintDamage()
        expectedCostQuantity = {
            CostItem.COMMUNICATION: 0,
            CostItem.FUEL: 0,
            CostItem.UNCLEARD_SQUARE: 10,
            CostItem.PROTECTED_TREE_DESTRUCTION: 0,
            CostItem.PAINT_DAMAGE: 1
        }
        TestCase.assertDictEqual(self, fakeExpense.costQuantity, expectedCostQuantity)

    def test_generate_cost_report(self):
        fakeExpense = Expense(10)
        expectedReport = ["Item                                       Quantity                 Cost",
                          "communication overhead                            0                    0",
                          "fuel usage                                        0                    0",
                          "uncleared squares                                10                   30",
                          "destruction of protected tree                     0                    0",
                          "paint damage to bulldozer                         0                    0",
                          "-----------------------------                                           ",
                          "Total                                                                 30"]
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            fakeExpense.generateCostReport()
            printedLines = fake_out.getvalue().splitlines()
            for i in range(len(expectedReport)):
                TestCase.assertEqual(self, printedLines[i], expectedReport[i])
