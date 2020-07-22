from enum import Enum

from core.site_map import SquareType
from core.expense import Expense
from core.simulator_exceptions import (
    QUITSIMULATION,
    OUTOFSITEMOVE,
    MOVEONPROTECTEDTREE
)


class Direction(Enum):
    """
    Enum class identifying the direction
    """
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3


class CommandType(Enum):
    """
    Enum class identifying the type of the command
    """
    ADVANCE = 0
    TURN_RIGHT = 1
    TURN_LEFT = 2
    QUIT = 3


class Location(object):
    """
    A utility class to represent a 2-D point as location
    """
    def __init__(self, row, column):
        self.row = row
        self.column = column


class Bulldozer(object):
    """
    This class represents a Bulldozer
    It has a sitemap and an expense object,
    and executes the commands given to it on the sitemap
    """

    def __init__(self, siteMap):
        """
        Initializes the sitemap,
        initial location is the top left corner
        initial direction is towards east
        the command history is empty in the beginning
        expenses only include the number of non-cleared square blocks
        :param siteMap(SiteMap): the site map on which the bulldozer will execute
        """
        self.siteMap = siteMap
        self.location = Location(0, -1)
        self.direction = Direction.EAST
        self.history = []
        self.expense = Expense(self.siteMap.getClearableSquares())

    def applyCommand(self, commandStr):
        """
        executes a command on the site map
        :param commandStr(str): the given command
        including advance, turn right, turn left, and quit
        """
        # First, log the command in the command histpry
        self.updateCommandHistory(commandStr)
        commandType = self.getCommandType(commandStr)

        # if this is a quit command, generate report and exit
        if commandType == commandType.QUIT:
            self.terminate(quit=True)
        else:
            # If it's not a quit command, add a communication overhead cost
            self.expense.addCommunicationOverhead()

            # For advance command, move location and
            # update sitemap according to the direction
            if commandType == CommandType.ADVANCE:
                squares = int(commandStr.split()[1])
                self.advance(squares)

            # For the otehr two commands, just change the direction
            elif commandType == CommandType.TURN_RIGHT:
                self.direction = Direction((self.direction.value + 1) % 4)
            elif commandType == CommandType.TURN_LEFT:
                self.direction = Direction((self.direction.value - 1) % 4)

    def getCommandType(self, commandStr):
        """
        Returns the type of the command
        :param commandStr(str): the input command string
        """
        if commandStr[0] == 'a':
            return CommandType.ADVANCE
        if commandStr == 'right' or commandStr == 'r':
            return CommandType.TURN_RIGHT
        if commandStr == 'left' or commandStr == 'l':
            return CommandType.TURN_LEFT
        if commandStr == 'quit' or commandStr == 'q':
            return CommandType.QUIT

    def advance(self, squares):
        """
        Moves the bulldozer squares numbers forward
        :param squares(int): the number of blocks to move forward
        """

        # For each direction, move block by block and
        # update the location of bulldozer
        # If moved out of the site map, terminate
        # If moved to a protected tree square, terminate
        # (This is done inside the visit function)
        # If passed through a removable tree, add paint damage cost,
        # but don't add the cost if stopped on it
        if self.direction == Direction.EAST:
            for i in range(1, squares + 1):
                if self.siteMap.isValid(self.location.row, self.location.column + 1):
                    self.location.column += 1
                    self.checkForPaintDamage(i, squares)
                    self.visit(self.location.row, self.location.column)
                else:
                    self.terminate(outOfSite=True)
        elif self.direction == Direction.WEST:
            for i in range(1, squares + 1):
                if self.siteMap.isValid(self.location.row, self.location.column - 1):
                    self.location.column -= 1
                    self.checkForPaintDamage(i, squares)
                    self.visit(self.location.row, self.location.column)
                else:
                    self.terminate(outOfSite=True)
        elif self.direction == Direction.SOUTH:
            for i in range(1, squares + 1):
                if self.siteMap.isValid(self.location.row + 1, self.location.column):
                    self.location.row += 1
                    self.checkForPaintDamage(i, squares)
                    self.visit(self.location.row, self.location.column)
                else:
                    self.terminate(outOfSite=True)
        elif self.direction == Direction.NORTH:
            for i in range(1, squares + 1):
                if self.siteMap.isValid(self.location.row - 1, self.location.column):
                    self.location.row -= 1
                    self.checkForPaintDamage(i, squares)
                    self.visit(self.location.row, self.location.column)
                else:
                    self.terminate(outOfSite=True)

    def visit(self, row, column):
        """
        visits the square block in the given row and column
        :param row(int): the row if the visiting square block
        :param column(int): the column if the visiting square block
        """
        # Detect the type of the square block
        squareType = self.siteMap.siteMap[row][column]

        if squareType == SquareType.NONREMOVABLE_TREE:
            # If visiting a protected tree, add the relevant cost and terminate the simulation
            self.expense.addProtectedTreeDestruction()
            self.terminate()
        else:
            # If not a protected tree, add relevant cost, update the square block type to CLEAR, and
            # reduce the number of uncleared square block in the expenses
            if self.siteMap.siteMap[row][column] != SquareType.CLEAR:
                self.expense.removeUnclearedSquare()
            self.expense.updateFuelConsumption(squareType)
            self.siteMap.siteMap[row][column] = SquareType.CLEAR

    def terminate(self, quit=False, outOfSite=False):
        """
        Throws an exception to be caught by the simulator
        :param quit(bool): if True, termination is because user entered quit command
        :param outOfSite(bool): if True, bulldozer has moved out of the site map
        """
        # Throws an exception to be caught by the simulator
        if quit:
            raise Exception(QUITSIMULATION)
        elif outOfSite:
            raise Exception(OUTOFSITEMOVE)
        else:
            raise Exception(MOVEONPROTECTEDTREE)

    def updateCommandHistory(self, commandStr):
        """
        Adds the given command string to the command history
        :param commandStr(str): given command
        """
        # Determine the type of command from the string
        commandType = self.getCommandType(commandStr)
        # Add proper string to the command history
        if commandType == CommandType.ADVANCE:
            squaresStr = commandStr.split()[1]
            self.history.append("Advance {}".format(squaresStr))
        elif commandType == CommandType.TURN_LEFT:
            self.history.append("Turn left")
        elif commandType == CommandType.TURN_RIGHT:
            self.history.append("Turn right")
        elif commandType == CommandType.QUIT:
            self.history.append("Quit")

    def checkForPaintDamage(self, advancedSquare, maxAdvance):
        """
        Checks if the bulldozer is passing through a removable tree
        If so, it adds paint damage cost to the expenses
        If advancedSquare < maxAdvance, it means that it should pass without stopping
        :param advancedSquare(int): the number of square blocks that has been advanced so far
        :param maxAdvance(int): the number of square blocks that should be advanced
        """
        # If advancedSquare == maxAdvance, it's not passing through. It's stopping there
        if advancedSquare < maxAdvance:
            squareType = self.siteMap.siteMap[self.location.row][self.location.column]
            if squareType == SquareType.REMOVABLE_TREE:
                # a removable tree in such cases incurs paint damage cost
                self.expense.addPaintDamage()

    def generateReport(self):
        """
        Generates a report including the command history and costs
        """
        print("\nThese are the commands you issued:\n")
        print(", ".join(self.history))

        print("\nThe costs for this land clearing operation were:\n")
        self.expense.generateCostReport()
