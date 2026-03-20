from state import GameState

def minimax(state: GameState, depth: int, maximize: bool) -> tuple[int | float, GameState | None]:
    # check if the game has ended
    if depth < 1 or state.is_terminal():
        return state.max_score - state.min_score, None
    
    # generate possible children nodes
    state_children = state.generate_nodes()
    best_score = 0
    best_move = None

    # maximize
    if maximize:
        best_score = float("-inf")

        for child in state_children:
            eval_score, _ = minimax(child, depth - 1, not maximize)

            if eval_score > best_score:
                best_score = eval_score
                best_move = child
    else:
        # minimize
        best_score = float("inf")

        for child in state_children:
            eval_score, _ = minimax(child, depth - 1, not maximize)

            if eval_score < best_score:
                best_score = eval_score
                best_move = child

    return best_score, best_move


def alpha_beta(state: GameState, depth: int, alpha: float, beta: float, maximize: bool) -> tuple[int | float, GameState | None]:
    # check if the game has ended
    if depth < 1 or state.is_terminal():
        return state.max_score - state.min_score, None
    
    # generate possible children nodes
    state_children = state.generate_nodes()
    best_score = 0
    best_move = None

    # maximize
    if maximize:
        best_score = float("-inf")

        for child in state_children:
            eval_score, _ = alpha_beta(child, depth - 1, alpha, beta, not maximize)

            if eval_score > best_score:
                best_score = eval_score
                best_move = child

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
    else:
        # minimize
        best_score = float("inf")

        for child in state_children:
            eval_score, _ = alpha_beta(child, depth - 1, alpha, beta, not maximize)

            if eval_score < best_score:
                best_score = eval_score
                best_move = child

            beta = min(beta, best_score)
            if beta <= alpha:
                break

    return best_score, best_move