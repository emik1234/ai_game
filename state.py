from __future__ import annotations

class GameState:
    def __init__(self, current_sequence: list[int], max_score: int, min_score: int, max_turn: bool) -> None:
        self.current_sequence = current_sequence
        self.max_score = max_score
        self.min_score = min_score
        self.max_turn = max_turn

    def is_terminal(self) -> bool:
        if len(self.current_sequence) <= 1:
            return True
        
        return False

    def generate_nodes(self) -> list[GameState]:
        children = []

        for index in range(0, len(self.current_sequence) - 1):
            new_max = self.max_score
            new_min = self.min_score

            # calculate sum of the adjacent numbers
            val1 = self.current_sequence[index]
            val2 = self.current_sequence[index + 1]

            # calculate score of the numbers
            total_score = val1 + val2

            points = 0
            replacement_number = 0
            modify_opponent_score = False

            if total_score > 7:
                points = 2
                replacement_number = 1
            elif total_score < 7:
                points = -1
                replacement_number = 3
                modify_opponent_score = True
            else:
                points = -1
                replacement_number = 2

            if self.max_turn:
                if modify_opponent_score:
                    new_min += points
                else:
                    new_max += points
            else:
                if modify_opponent_score:
                    new_max += points
                else:
                    new_min += points


            # create a list copy
            new_numbers = self.current_sequence[:index] + [replacement_number] + self.current_sequence[index + 2:]
            
            # create a new state
            new_state = GameState(new_numbers, new_max, new_min, not self.max_turn)
            children.append(new_state)

        return children
