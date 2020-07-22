# This class represents the site map to be cleared by bulldozer
# The map is a grid consisting of M by N squares,
# Each square could be one of the following cases:
#   1- Plain land
#   2- Rocky land
#   3- Removable tree
#   4- Non-removable tree
#   5- cleared land

from os import path
from enum import Enum

from core.simulator_exceptions import (
    FILENOTEXIST,
    READACCESSNOTPROVIDED,
    UNACCEPTABLESQUARE,
    EMPTYFILE,
    NOTAGRID
)


class SquareType(Enum):
    """
    Enum class for identifying different types of square blocks
    Each square block can be a plain land, rocky land, removable tree, protected tree, or an already cleared clock
    """
    PLAIN = 0
    ROCK = 1
    REMOVABLE_TREE = 2
    NONREMOVABLE_TREE = 3
    CLEAR = 4


# A dictionary mapping charactes to square block types
# '*' denotes a cleared block
squareTypeMap = {
    'o': SquareType.PLAIN,
    'r': SquareType.ROCK,
    't': SquareType.REMOVABLE_TREE,
    'T': SquareType.NONREMOVABLE_TREE,
    '*': SquareType.CLEAR
}

# A dictionary mapping square block types to characters
# '*' denotes a cleared block
squareCharacterMap = {
    SquareType.PLAIN: 'o',
    SquareType.ROCK: 'r',
    SquareType.REMOVABLE_TREE: 't',
    SquareType.NONREMOVABLE_TREE: 'T',
    SquareType.CLEAR: '*'
}


class SiteMap(object):
    """
    This class represent the site map to be cleared by bulldozer
    The map is a grid consisting of M by N squares,
    It consists of a 2-D array of SquareTypes as the site map and the number of rows and columns on it
    """

    def __init__(self, filePath):
        """
        Reads the sitemap from file and sets rows and column accordingly
        :param filePath(str): the path to the file
        """
        self.siteMap = self.readFromFile(filePath)
        self.rows = len(self.siteMap)
        self.columns = len(self.siteMap[0])

    def readFromFile(self, filePath):
        """
        Reads the sitemap from file
        returns siteMap, a 2-D array of SquareTypes
        :param filePath(str): the path to the input sitemap file
        """

        # Check if the file exists
        if not path.exists(filePath):
            raise Exception(FILENOTEXIST.format(filePath))

        # Check if read access is provided to the file
        try:
            f = open(filePath, "r")
            content = f.read()
            lines = content.splitlines()
        except OSError:
            raise Exception(READACCESSNOTPROVIDED.format(filePath))

        # Check if the file is empty
        if len(lines) == 0:
            raise Exception(EMPTYFILE)

        # Check if the content of the file represents a grid
        for i in range(1, len(lines)):
            if len(lines[i]) != len(lines[i - 1]):
                raise Exception(NOTAGRID)

        siteMap = []
        for line in lines:
            rowMap = []
            for c in line:
                rowMap.append(self.getSquareType(c))
            siteMap.append(rowMap)
        return siteMap

    def show(self):
        """
        Prints out the sitemap on the console
        """
        print("  -----------------------------------------------------------------  ")

        printableSiteMap = ""
        for row in self.siteMap:
            printableSiteMap += '\t'.join([squareCharacterMap[sqType] for sqType in row])
            printableSiteMap += '\n'

        print(printableSiteMap)
        print("  -----------------------------------------------------------------  ")

    def getSquareType(self, c):
        """
        Returns the type of a square block based on the representing character
        Throws an exception if the character is not valid
        :param c(str): the character representing the square block
        """
        if c in squareTypeMap:
            return squareTypeMap[c]
        else:
            raise Exception(UNACCEPTABLESQUARE.format(c))

    def getClearableSquares(self):
        """
        Calculates total number of non-cleared square blocks
        Note: It does not include the number of protected trees, as they are considered non-clearable
        Returns the calculated number
        :rtype: int
        """
        count = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if self.siteMap[i][j] == SquareType.PLAIN or \
                   self.siteMap[i][j] == SquareType.ROCK or \
                   self.siteMap[i][j] == SquareType.REMOVABLE_TREE:
                    count += 1
        return count

    def isValid(self, row, column):
        """
        Determines if the given row and column stays within the boundaries of the site map
        :param row(int): row of the sitemap
        :param column(int): column of the sitemap
        :rtype: bool
        """
        if row < 0 or column < 0 or row >= self.rows or column >= self.columns:
            return False
        return True
