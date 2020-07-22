from enum import Enum

from core.site_map import SquareType


class CostItem(Enum):
    """
    Enum class representing different types of costs
    """
    COMMUNICATION = 0
    FUEL = 1
    UNCLEARD_SQUARE = 2
    PROTECTED_TREE_DESTRUCTION = 3
    PAINT_DAMAGE = 4


# dictionary mapping the square clock types to the amount of fuel consumed by them
fuelConsumption = {
    SquareType.CLEAR: 1,
    SquareType.PLAIN: 1,
    SquareType.ROCK: 2,
    SquareType.REMOVABLE_TREE: 2,
    SquareType.NONREMOVABLE_TREE: 0,
}

# dictionary mapping the cost incurred for each item
costPerQuantity = {
    CostItem.COMMUNICATION: 1,
    CostItem.FUEL: 1,
    CostItem.UNCLEARD_SQUARE: 3,
    CostItem.PROTECTED_TREE_DESTRUCTION: 10,
    CostItem.PAINT_DAMAGE: 2
}


class Expense(object):
    """
    This class represents the cost of a single simulation and is used by Bulldozer object
    """

    def __init__(self, totalUncleared):
        """
        initializer function to set the quantity of each cost item
        :param totalUncleared(int): sets the initial number of clearable square blocks that are not cleared
        """
        self.costQuantity = {
            CostItem.COMMUNICATION: 0,
            CostItem.FUEL: 0,
            CostItem.UNCLEARD_SQUARE: totalUncleared,
            CostItem.PROTECTED_TREE_DESTRUCTION: 0,
            CostItem.PAINT_DAMAGE: 0
        }

    def generateCostReport(self):
        """
        Generates a cost report of the simulation and shows on the concole
        Includes the following items:
        communication overhead, fuel usage, uncleared squares, destruction of protected tree, and paint damage
        """
        totalCost = 0
        report = [["Item", "Quantity", "Cost"]]

        communicationCost = self.costQuantity[CostItem.COMMUNICATION] * costPerQuantity[CostItem.COMMUNICATION]
        report.append(["communication overhead",
                      self.costQuantity[CostItem.COMMUNICATION],
                      communicationCost])
        totalCost += communicationCost

        fuelCost = self.costQuantity[CostItem.FUEL]*costPerQuantity[CostItem.FUEL]
        report.append(["fuel usage",
                      self.costQuantity[CostItem.FUEL],
                      fuelCost])
        totalCost += fuelCost

        unclearedCost = self.costQuantity[CostItem.UNCLEARD_SQUARE] * costPerQuantity[CostItem.UNCLEARD_SQUARE]
        report.append(["uncleared squares",
                      self.costQuantity[CostItem.UNCLEARD_SQUARE],
                      unclearedCost])
        totalCost += unclearedCost

        protectedTreeCost = self.costQuantity[CostItem.PROTECTED_TREE_DESTRUCTION]*costPerQuantity[CostItem.PROTECTED_TREE_DESTRUCTION]
        report.append(["destruction of protected tree",
                      self.costQuantity[CostItem.PROTECTED_TREE_DESTRUCTION],
                      protectedTreeCost])
        totalCost += protectedTreeCost

        paintDamageCost = self.costQuantity[CostItem.PAINT_DAMAGE] * costPerQuantity[CostItem.PAINT_DAMAGE]
        report.append(["paint damage to bulldozer",
                      self.costQuantity[CostItem.PAINT_DAMAGE],
                      paintDamageCost])
        totalCost += paintDamageCost

        report.append(["-----------------------------", "", ""])
        report.append(["Total", "", totalCost])

        for args in (report):
            print('{0:<30} {1:>20} {2:>20}'.format(*args))

    def addCommunicationOverhead(self):
        """
        Adds an extra communication overhead cost
        """
        self.costQuantity[CostItem.COMMUNICATION] += 1

    def removeUnclearedSquare(self):
        """
        Reduces the number of uncleared square blocks by one
        """
        self.costQuantity[CostItem.UNCLEARD_SQUARE] -= 1

    def addProtectedTreeDestruction(self):
        """
        Adds one unit to the cost of protected trees
        """
        self.costQuantity[CostItem.PROTECTED_TREE_DESTRUCTION] += 1

    def updateFuelConsumption(self, squareType):
        """
        Updates the fuel consumption according to the type of the square block
        :param squareType(int): The type of the square block
        """
        self.costQuantity[CostItem.FUEL] += fuelConsumption[squareType]

    def addPaintDamage(self):
        """
        Adds a unit to the cost of paint damage
        """
        self.costQuantity[CostItem.PAINT_DAMAGE] += 1
