from game_api import *
from boards import *
INF = float('inf')

def is_game_over_connectfour(board) :
    "Returns True if game is over, otherwise False."
    numPossible = board.num_rows * board.num_cols
    isFull = board.count_pieces() == numPossible
    existsWinner = False
    for chain in board.get_all_chains():
        if len(chain)>=4:
            existsWinner = True
    return isFull or existsWinner


def next_boards_connectfour(board) :
    """Returns a list of ConnectFourBoard objects that could result from the
    next move, or an empty list if no moves can be made."""
    if is_game_over_connectfour(board):
        return []
    newBoards = []
    for col_num in xrange(board.num_cols):
        if not board.is_column_full(col_num):
            newBoards.append(board.add_piece(col_num))
    return newBoards


def endgame_score_connectfour(board, is_current_player_maximizer) :
    """Given an endgame board, returns 1000 if the maximizer has won,
    -1000 if the minimizer has won, or 0 in case of a tie."""
    if is_current_player_maximizer:
        return -1000
    if not is_current_player_maximizer:
        return 1000
    return 0

def endgame_score_connectfour_faster(board, is_current_player_maximizer) :
    """Given an endgame board, returns an endgame score with abs(score) >= 1000,
    returning larger absolute scores for winning sooner."""
    if is_current_player_maximizer:
        return -1000 - 1000*(1.0/board.count_pieces())
    if not is_current_player_maximizer:
        return 1000 + 1000*(1.0/board.count_pieces())
    return 0

def heuristic_connectfour(board, is_current_player_maximizer) :
    """Given a non-endgame board, returns a heuristic score with
    abs(score) < 1000, where higher numbers indicate that the board is better
    for the maximizer."""
    cp = board.players[0]
    cpChains = board.get_all_chains(True)
    cpAvg = avgLength(cpChains)
    
    
    pp  = board.players[1]
    ppChains = board.get_all_chains(False)
    ppAvg = avgLength(ppChains)
    heuristic = ppAvg*len(ppChains) - cpAvg*len(cpChains) + 1.0/board.count_pieces()
    if is_current_player_maximizer:
        return -1*(heuristic)
    if not is_current_player_maximizer:
        return heuristic
    return 0

def avgLength(listOfLists):
    lenSum = 0.0
    for list in listOfLists:
        lenSum+=len(list)
    return 1.0*lenSum/len(listOfLists)

# Now we can create AbstractGameState objects for Connect Four, using some of
# the functions you implemented above.  You can use the following examples to
# test your dfs and minimax implementations in Part 2.

# This AbstractGameState represents a new ConnectFourBoard, before the game has started:
state_starting_connectfour = AbstractGameState(snapshot = ConnectFourBoard(),
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "NEARLY_OVER" from boards.py:
state_NEARLY_OVER = AbstractGameState(snapshot = NEARLY_OVER,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)

# This AbstractGameState represents the ConnectFourBoard "BOARD_UHOH" from boards.py:
state_UHOH = AbstractGameState(snapshot = BOARD_UHOH,
                                 is_game_over_fn = is_game_over_connectfour,
                                 generate_next_states_fn = next_boards_connectfour,
                                 endgame_score_fn = endgame_score_connectfour_faster)


#### PART 2 ###########################################
# Note: Functions in Part 2 use the AbstractGameState API, not ConnectFourBoard.

def dfs_maximizing(state) :
    #    """Performs depth-first search to find path with highest endgame score.
    #    Returns a tuple containing:
    #     0. the best path (a list of AbstractGameState objects),
    #     1. the score of the leaf node (a number), and
    #     2. the number of static evaluations performed (a number)"""
    if state.is_game_over():
        return [[state],state.get_endgame_score(True),1]
    else:
        children = state.generate_next_states()
        bestChildScore = -INF
        bestChildPath = []
        totalStaticEvals = 0
        for child in children:
            childRecurse = dfs_maximizing(child)
            totalStaticEvals += childRecurse[2]
            if childRecurse[1]>bestChildScore:
                bestChildScore = childRecurse[1]
                bestChildPath = childRecurse[0]
        newPath = [state]+bestChildPath
        return [newPath, bestChildScore, totalStaticEvals]
        


def minimax_endgame_search(state, maximize=True) :
    """Performs minimax search, searching all leaf nodes and statically
    evaluating all endgame scores.  Same return type as dfs_maximizing."""
    if state.is_game_over():
        return [[state],state.get_endgame_score(maximize),1]
    else:
        children = state.generate_next_states()
        bestChildPath = []
        totalStaticEvals = 0
        if maximize:
            bestChildScore = -INF
            for child in children:
                childRecurse = minimax_endgame_search(child,False)
                totalStaticEvals += childRecurse[2]
                if childRecurse[1]>bestChildScore:
                    bestChildScore = childRecurse[1]
                    bestChildPath = childRecurse[0]
        else:
            bestChildScore = INF
            for child in children:
                childRecurse = minimax_endgame_search(child,True)
                totalStaticEvals += childRecurse[2]
                if childRecurse[1]<bestChildScore:
                    bestChildScore = childRecurse[1]
                    bestChildPath = childRecurse[0]
        newPath = [state]+bestChildPath
        return [newPath, bestChildScore, totalStaticEvals]


# Uncomment the line below to try your minimax_endgame_search on an
# AbstractGameState representing the ConnectFourBoard "NEARLY_OVER" from boards.py:

#pretty_print_dfs_type(minimax_endgame_search(state_NEARLY_OVER))


def minimax_search(state, heuristic_fn=always_zero, depth_limit=INF, maximize=True) :
    "Performs standard minimax search.  Same return type as dfs_maximizing."
    childDepthLimit = depth_limit-1
    if state.is_game_over():
        return [[state],state.get_endgame_score(maximize),1]
    elif depth_limit==0:
        score = heuristic_fn(state.get_snapshot(),maximize)
        return [[state],score,1]
    else:
        children = state.generate_next_states()
        bestChildPath = []
        totalStaticEvals = 0
        if maximize:
            bestChildScore = -INF
            for child in children:
                childRecurse = minimax_search(child,heuristic_fn,childDepthLimit,False)
                totalStaticEvals += childRecurse[2]
                if childRecurse[1]>bestChildScore:
                    bestChildScore = childRecurse[1]
                    bestChildPath = childRecurse[0]
        else:
            bestChildScore = INF
            for child in children:
                childRecurse = minimax_search(child,heuristic_fn,childDepthLimit,True)
                totalStaticEvals += childRecurse[2]
                if childRecurse[1]<bestChildScore:
                    bestChildScore = childRecurse[1]
                    bestChildPath = childRecurse[0]
        newPath = [state]+bestChildPath
        return [newPath, bestChildScore, totalStaticEvals]


# Uncomment the line below to try minimax_search with "BOARD_UHOH" and
# depth_limit=1.  Try increasing the value of depth_limit to see what happens:

#pretty_print_dfs_type(minimax_search(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=1))


def minimax_search_alphabeta(state, alpha=-INF, beta=INF, heuristic_fn=always_zero,
                             depth_limit=INF, maximize=True) :
    "Performs minimax with alpha-beta pruning.  Same return type as dfs_maximizing."
    childDepthLimit = depth_limit-1
    if state.is_game_over():
        return [[state],state.get_endgame_score(maximize),1]
    elif depth_limit==0:
        score = heuristic_fn(state.get_snapshot(),maximize)
        return [[state],score,1]
    else:
        children = state.generate_next_states()
        bestChildPath = []
        totalStaticEvals = 0
        if maximize:
            bestChildScore = -INF
            for child in children:
                childRecurse = minimax_search_alphabeta(child,alpha,beta,heuristic_fn,childDepthLimit,False)
                totalStaticEvals += childRecurse[2]
                if childRecurse[1]>bestChildScore:
                    bestChildScore = childRecurse[1]
                    bestChildPath = childRecurse[0]
                alpha = max(alpha,bestChildScore)
                if beta<=alpha:
                    break

        else:
            bestChildScore = INF
            for child in children:
                childRecurse = minimax_search_alphabeta(child,alpha,beta,heuristic_fn,childDepthLimit,True)
                totalStaticEvals += childRecurse[2]
                if childRecurse[1]<bestChildScore:
                    bestChildScore = childRecurse[1]
                    bestChildPath = childRecurse[0]
                beta = min(beta, bestChildScore)
                if beta<=alpha:
                    break
        newPath = [state]+bestChildPath
        return [newPath, bestChildScore, totalStaticEvals]


# Uncomment the line below to try minimax_search_alphabeta with "BOARD_UHOH" and
# depth_limit=4.  Compare with the number of evaluations from minimax_search for
# different values of depth_limit.

#pretty_print_dfs_type(minimax_search_alphabeta(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4))


def progressive_deepening(state, heuristic_fn=always_zero, depth_limit=INF,
                          maximize=True) :
    """Runs minimax with alpha-beta pruning. At each level, updates anytime_value
    with the tuple returned from minimax_search_alphabeta. Returns anytime_value."""
    anytime_value = AnytimeValue()   # TA Note: Use this to store values.
    for nowDepthLimit in xrange(1,depth_limit+1):
        result = minimax_search_alphabeta(state, -INF, INF, heuristic_fn,
                                          nowDepthLimit, maximize)
        anytime_value.set_value(result)
    return anytime_value

# Uncomment the line below to try progressive_deepening with "BOARD_UHOH" and
# depth_limit=4.  Compare the total number of evaluations with the number of
# evaluations from minimax_search or minimax_search_alphabeta.

#progressive_deepening(state_UHOH, heuristic_fn=heuristic_connectfour, depth_limit=4).pretty_print()


#### SURVEY ###################################################

NAME = "Rebecca Corcillo"
COLLABORATORS = "Nobody"
HOW_MANY_HOURS_THIS_LAB_TOOK = "15"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!

def wrapper_connectfour(board_array, players, whose_turn = None) :
    board = ConnectFourBoard(board_array = board_array,
                             players = players,
                             whose_turn = whose_turn)
    return AbstractGameState(snapshot = board,
                             is_game_over_fn = is_game_over_connectfour,
                             generate_next_states_fn = next_boards_connectfour,
                             endgame_score_fn = endgame_score_connectfour_faster)
