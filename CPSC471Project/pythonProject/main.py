SIZE = 10
debugOn = False


# Madalyn Arsenault
def options(turn, oldWorld, newWorld, world):
    empty = 1
    singleCritter = 2
    singleBirth = 3
    simpleBirth = 4
    edgeyTesting = 5
    complexWorld = 6
    print("Choices for starting biosphere:")
    print("\t(1) Empty\n\t(2) Single critter\n\t(3) Single birth")
    print("\t(4) Simple birth\n\t(5) Edgey testing\n\t(6) It's a complex world")
    choice = int(input("Please make a selection: "))
    if choice == empty:
        emptyUpdate(turn, oldWorld, newWorld, world)
    if choice == singleCritter:
        singleCritterUpdate(turn, oldWorld, newWorld, world)
    if choice == singleBirth:
        singleBirthUpdate(turn, oldWorld, newWorld, world)
    if choice == simpleBirth:
        simpleBirthUpdate(turn, oldWorld, newWorld, world)
    if choice == edgeyTesting:
        edgeyTestingUpdate(turn, oldWorld, newWorld, world)
    if choice == complexWorld:
        complexWorldUpdate(turn, oldWorld, newWorld, world)


def emptyUpdate(turn, oldWorld, newWorld, world):
    for r in range(0, SIZE, 1):
        for c in range(0, SIZE, 1):
            checkRow = 0
            checkColumn = 0
            turn = turn + 1
            oldWorld = oneEmpty()
            newWorld = updateWorld(oldWorld, world)
            display(turn, oldWorld, newWorld)
            enter = input("Hit enter to continue ('q' to quit)")
            while enter != 0:
                turn = turn + 1
                oldWorld = newWorld
                newWorld = updateWorld(oldWorld, world)
                display(turn, oldWorld, newWorld)
                enter = input("Hit enter to continue ('q' to quit)")


def singleCritterUpdate(turn, oldWorld, newWorld, world):
    for r in range(0, SIZE, 1):
        for c in range(0, SIZE, 1):
            checkRow = 0
            checkColumn = 0
            turn = turn + 1
            oldWorld = twoSingleCritter()
            newWorld = updateWorld(oldWorld, world)
            display(turn, oldWorld, newWorld)
            enter = input("Hit enter to continue ('q' to quit)")
            while enter != 0:
                turn = turn + 1
                oldWorld = newWorld
                newWorld = updateWorld(oldWorld, world)
                display(turn, oldWorld, newWorld)
                enter = input("Hit enter to continue ('q' to quit)")


def singleBirthUpdate(turn, oldWorld, newWorld, world):
    for r in range(0, SIZE, 1):
        for c in range(0, SIZE, 1):
            checkRow = 0
            checkColumn = 0
            turn = turn + 1
            oldWorld = threeSingleBirth()
            newWorld = updateWorld(oldWorld, newWorld)
            display(turn, oldWorld, newWorld)
            enter = input("Hit enter to continue ('q' to quit)")
            while enter != 0:
                turn = turn + 1
                oldWorld = newWorld
                newWorld = updateWorld(oldWorld, newWorld)
                display(turn, oldWorld, newWorld)
                enter = input("Hit enter to continue ('q' to quit)")


def simpleBirthUpdate(turn, oldWorld, newWorld, world):
    for r in range(0, SIZE, 1):
        for c in range(0, SIZE, 1):
            turn = turn + 1
            oldWorld = fourthSimpleBirth()
            newWorld = updateWorld(oldWorld, world)
            display(turn, oldWorld, newWorld)
            enter = input("Hit enter to continue ('q' to quit)")
            while enter != 0:
                turn = turn + 1
                oldWorld = newWorld
                newWorld = updateWorld(oldWorld, world)
                display(turn, oldWorld, newWorld)
                enter = input("Hit enter to continue ('q' to quit)")


def edgeyTestingUpdate(turn, oldWorld, newWorld, world):
    for r in range(0, SIZE, 1):
        for c in range(0, SIZE, 1):
            checkRow = 0
            checkColumn = 0
            turn = turn + 1
            oldWorld = fifthCreateListEdgeCases()
            newWorld = updateWorld(oldWorld, world)
            display(turn, oldWorld, newWorld)
            enter = input("Hit enter to continue ('q' to quit)")
            while enter != 0:
                turn = turn + 1
                oldWorld = newWorld
                newWorld = updateWorld(oldWorld, world)
                display(turn, oldWorld, newWorld)
                enter = input("Hit enter to continue ('q' to quit)")


def complexWorldUpdate(turn, oldWorld, newWorld, world):
    for r in range(0, SIZE, 1):
        for c in range(0, SIZE, 1):
            checkRow = 0
            checkColumn = 0
            turn = turn + 1
            oldWorld = sixthComplexCases()
            newWorld = updateWorld(oldWorld, world)
            display(turn, oldWorld, newWorld)
            enter = input("Hit enter to continue ('q' to quit)")
            while enter != 0:
                turn = turn + 1
                oldWorld = newWorld
                newWorld = updateWorld(oldWorld, world)
                display(turn, oldWorld, newWorld)
                enter = input("Hit enter to continue ('q' to quit)")


def checkNeighbour(checkRow, checkColumn, oldWorld):
    searchMin = -1
    searchMax = 2
    neighbourColumn = 0
    neighbourRow = 0
    neighbourList = []
    for r in range(searchMin, searchMax):
        for c in range(searchMin, searchMax):
            neighbourRow = checkRow + r
            neighbourColumn = checkColumn + c

            validNeighbour = True

            if (neighbourRow) == checkRow and (neighbourColumn) == checkColumn:
                validNeighbour = False

            if (neighbourRow) < 0 or (neighbourRow) >= SIZE:
                validNeighbour = False

            if (neighbourColumn) < 0 or (neighbourColumn) >= SIZE:
                validNeighbour = False

            if validNeighbour:
                neighbourList.append(oldWorld[r][c])

    return (neighbourList)


def updateWorld(oldWorld, newWorld):
    r = 10
    c = 10
    i = 10
    getsKilled = []
    staysAlive = []
    isBorn = []
    livingNeighbourCount = []
    check_Neighbour = []

    for r in range(0, SIZE, 1):
        for c in range(0, SIZE, 1):

            check_Neighbour = checkNeighbour(r, c, oldWorld)

            for i in check_Neighbour:
                if i == "*":
                    livingNeighbourCount.append(i)

            if oldWorld[r][c] == "*":
                if len(livingNeighbourCount) < 2 or len(livingNeighbourCount) > 3:
                    getsKilled.append((r, c))

                elif len(livingNeighbourCount) == 3 or len(livingNeighbourCount) == 2:
                    stayAlive.append((r, c))

            else:
                if len(livingNeighbourCount) == 3:
                    isBorn.append((r, c))

        for r, c in getsKilled:
            newWorld[r][c] = ' '

        for r, c in isBorn:
            newWorld[r][c] = '*'

    return (newWorld)


# Game of Life simulation
# Author:  James Tam
# Version: June 6, 2020
# This version of the program initializes the oldWorld (during the turn)
# and the newWorld (appearance of the world after the turn) as well as
# displaying the two versions side by side. Since the original state of
# the biosphere was empty the state of the new state is correct. However,
# no rules of births and deaths was applied in this version of the
# simulation.

# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
# """
#  @oneEmpty()
# @Arguments: None
# @The biosphere is initialized to a completely empty state.
# @Return value: A reference to a 2D list, the initialized biosphere.
def oneEmpty():
    world = []
    world = [
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    ]
    return (world)


# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
"""
  @twoSingleCritter()
  @Arguments: None
  @The biosphere is empty except for one location which contains a 
  @Critter.
  @Return value: A reference to a 2D list, the initialized biosphere.
"""


def twoSingleCritter():
    world = []
    world = [
        ["*", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    ]
    print(world)
    return (world)


# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
"""
  @threeSingleBirth()
  @Arguments: None
  @The biosphere is empty except for 3 locations which contain Critters.
  @The 3 Critters are all in proximity to a single location in the 
  @biosphere.
  @Return value: A reference to a 2D list, the initialized biosphere.
"""


def threeSingleBirth():
    world = []
    world = [
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "*", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", "*", " ", " ", " ", " ", " ", " "],
        [" ", "*", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    ]
    return (world)


# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
"""
  @fourthSimpleBirth()
  @Arguments: None
  @The biosphere contains a number of Critters which are close enough
  @proximity to produce new births for a number of turns.
  @Return value: A reference to a 2D list, the initialized biosphere.
"""


def fourthSimpleBirth():
    world = []
    world = [
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "*", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", "*", "*", " ", " ", " ", " ", " ", " "],
        [" ", "*", " ", "*", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        ["*", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    ]
    return (world)


# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
"""
  @fifthCreateListEdgeCases()
  @Arguments: None
  @The biosphere has a Critter located at the edge of the biosphere at
  @each of the 4 compass ponts. Also there is a Critter in each of the
  @corners.
  @Return value: A reference to a 2D list, the initialized biosphere.
"""


def fifthCreateListEdgeCases():
    world = []
    world = [
        ["*", " ", "*", " ", " ", " ", " ", " ", " ", "*"],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "*", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        ["*", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", "*", " ", " ", " ", " ", " ", " ", " ", " "],
        ["*", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", "*"],
        [" ", " ", " ", " ", " ", " ", " ", " ", "*", " "],
        ["*", "*", " ", " ", " ", " ", " ", " ", " ", "*"]
    ]
    return (world)


# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
"""
  @sixthComplexCases()
  @Arguments: None
  @The biosphere contains a starting pattern that will require a 
  @program to handle births, deaths and edge cases. 
  @Return value: A reference to a 2D list, the initialized biosphere.
"""


def sixthComplexCases():
    world = []
    world = [
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "*", " ", " ", " ", " ", " "],
        [" ", "*", " ", " ", " ", "*", " ", " ", " ", " "],
        [" ", " ", " ", "*", "*", "*", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        ["*", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    ]
    return (world)


# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
# '''
# @display()
# @Argument: two references to the 2D list which is game world.
# @The list must be already created and properly initialized
# @prior to calling this function!
# @Return value: None
# @Displays each element of the world with each row all on one line
# @Each element is bound: above, left, right and below with a bar (to
# @make elements easier to see.
# @Each list is displayed side by side
# <Old list>#<TAB><New list>
# '''
def display(turn, oldWorld, newWorld):
    # Displays a row at a time of each list
    print("Turn #%d" % turn)
    print("BEFORE\t\t\tAFTER")
    for r in range(0, SIZE, 1):

        # Row of dashes before each row of old and new list
        # (Dashes for old list)
        for i in range(0, SIZE, 1):
            print("%s" % (" -"), end="")
        print("#\t", end="")
        # (Dashes for new list)
        for i in range(0, SIZE, 1):
            print("%s" % (" -"), end="")
        print()

        # Display one row of old world list
        for c in range(0, SIZE, 1):
            # Display: A vertical bar and then element (old list)
            print("|%s" % (oldWorld[r][c]), end="")
        # Separate the lists with a number sign and a tab
        print("", end="#\t")

        # Display one row of new world list
        for c in range(0, SIZE, 1):
            # Display: A vertical bar and then element (new list)
            print("|%s" % (newWorld[r][c]), end="")
        print("|")

    # Row of dashes after end of last row (old world list)
    for i in range(0, SIZE, 1):
        print("%s" % (" -"), end="")
    print("#\t", end="")

    # Row of dashes after end of each row (new world list)
    for i in range(0, SIZE, 1):
        print("%s" % (" -"), end="")
    print()


#################################################################
# Author:  James Tam
# This function was created entirely by the above author and is
# used with permission.
def start():
    choice = ""
    oldWorld = []
    newWorld = []
    turn = 0
    enter = 0

    world = oneEmpty()
    oldWorld = oneEmpty()
    newWorld = oneEmpty()
    options(turn, oldWorld, newWorld, world)
    display(turn, oldWorld, newWorld)


start()
