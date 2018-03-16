from minimax_helpers import *


def minimax_decision(gameState, depth):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.

    You can ignore the special case of calling this function
    from a terminal state.
    """
    return max(gameState.get_legal_moves(),
               key=lambda m: min_value(gameState.forecast_move(m), depth - 1))
