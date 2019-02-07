class Diamond(object):
    """
    Primary class to be used to calculate targeting range and range damage
    Can later be adapted to movement range calculations
    """

    # temporary values used for testing
    Range = 3
    X = 5
    Y = 5

    for i in range(-Range, Range + 1):
        print(X, Y + i)
        # check if the coordinates are valid
        # if valid, add to the list of affected tiles

        sideX = (Range - abs(i))
        if sideX != 0:
            for v in range(1, sideX + 1):
                print(X + v, Y + i)
                print(X + (-1 * v), Y + i)
                # check if the coordinates are valid
                # if valid, add to the list of affected tiles

    # return a list of tuples of affected tiles
