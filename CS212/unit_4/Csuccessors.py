# -----------------
# User Instructions
# 
# Write a function, csuccessors, that takes a state (as defined below) 
# as input and returns a dictionary of {state:action} pairs. 
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where 
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings: 
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C'
# where 'MM->' means two missionaries travel to the right side.
# 
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

MovesMap = {
    (0, 0): [],
    (0, 1): [([0, -1], [0, 1])],
    (0, 2): [([0, -2], [0, 2])],
    (1, 0): [([-1, 0], [1, 0])],
    (2, 0): [([-2, 0], [2, 0])],
    (1, 1): [([-1, -1], [1, 1])],
    (2, 1): [],
    (1, 2): [],
    (2, 2): []
}

MovesMap[(0, 2)].extend(MovesMap[(0, 1)])
MovesMap[(2, 0)].extend(MovesMap[(1, 0)])

MovesMap[(1, 1)].extend(MovesMap[(1, 0)])
MovesMap[(1, 1)].extend(MovesMap[(0, 1)])

MovesMap[(2, 1)].extend(MovesMap[(1, 1)])
MovesMap[(2, 1)].extend(MovesMap[(2, 0)])

MovesMap[(1, 2)].extend(MovesMap[(1, 1)])
MovesMap[(1, 2)].extend(MovesMap[(0, 2)])

MovesMap[(2, 2)].extend(MovesMap[(1, 2)])
MovesMap[(2, 2)].extend(MovesMap[(2, 1)])


CodesToSymbols = {
    (1, 0): 'M',
    (0, 1): 'C',
    (1, 1): 'MC',
    (2, 0): 'MM',
    (0, 2): 'CC',
}


def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state

    if M1 < C1 and M1 != 0:
        return {}

    move_forward = (B1 == 1)

    # Finding out how many people can move from one to another side
    M_can_move = M1 if move_forward else M2
    C_can_move = C1 if move_forward else C2

    # Limiting max amount of people can move in boat
    M_can_move = min(M_can_move, 2)
    C_can_move = min(C_can_move, 2)

    from_ = (M1, C1) if move_forward else (M2, C2)
    to_ = (M1, C1) if not move_forward else (M2, C2)

    result = dict()

    for move in MovesMap[(M_can_move, C_can_move)]:
        rfrom_ = tuple(map(lambda x,y: x+y, from_, move[0]))
        rto_ = tuple(map(lambda x,y: x+y, to_, move[1]))

        if move_forward:
            result[(rfrom_[0], rfrom_[1], 0, rto_[0], rto_[1], 1)] = "%s->" % CodesToSymbols[tuple(move[1])]
        else:
            result[(rto_[0], rto_[1], 1, rfrom_[0], rfrom_[1], 0)] = "<-%s" % CodesToSymbols[tuple(move[1])]

    return result


def test():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->',
                                               (1, 1, 0, 1, 1, 1): 'MC->',
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M',
                                               (3, 1, 1, 2, 3, 0): '<-MM',
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    return 'tests pass'

print test()