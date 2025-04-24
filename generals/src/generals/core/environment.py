from typing import List, Tuple
from generals.core.board import Board
from generals.core.player import Player
from generals.core.combat_resolver import CombatResolver


class Environment:
    def __init__(self, players: List[Player], grid_size: int = 10):
        """Initialize the game environment."""
        self.players = players  # List of players (e.g., AStarPlayer, NeuralNetPlayer)
        self.board = Board(grid_size)  # Initialize 10x10 grid
        self.combat_resolver = CombatResolver()  # Combat logic
        self.current_turn = 0  # Tracks current player (0 or 1)
        self.done = False  # Game over flag

    def reset(self) -> dict:
        """Reset the game to initial state, return initial state for first player."""
        self.board.initialize()  # Set up terrain, cities, units
        self.current_turn = 0
        self.done = False
        return self.get_state(self.players[0])

    def step(self, action: dict) -> Tuple[dict, float, bool]:
        """Apply an action, return (next_state, reward, done)."""
        current_player = self.players[self.current_turn]
        # Validate and apply action (e.g., move, attack)
        self.apply_action(current_player, action)
        # Update game state
        self.board.update_visibility()
        # Check if game is over
        self.done = self.check_game_over()
        # Compute reward
        reward = self.compute_reward(current_player)
        # Switch to next player
        self.current_turn = (self.current_turn + 1) % len(self.players)
        next_state = self.get_state(self.players[self.current_turn])
        return next_state, reward, self.done

    def get_state(self, player: Player) -> dict:
        """Return the current state for the given player, filtered by fog of war."""
        # Return tensor-based state (terrain, units, cities, visibility)
        pass

    def compute_reward(self, player: Player) -> float:
        """Calculate the reward for the player's turn."""
        # Sparse: +1 for win, -1 for loss
        # Dense: +0.1 for city capture, etc.
        pass

    def apply_action(self, player: Player, action: dict):
        """Apply the player's action to the board."""
        # Delegate to Board or CombatResolver based on action type
        pass

    def check_game_over(self) -> bool:
        """Check if the game has ended (e.g., all cities captured)."""
        pass

    def run_game(self):
        """Run the game loop until completion (for non-RL use)."""
        while not self.done:
            current_player = self.players[self.current_turn]
            state = self.get_state(current_player)
            action = current_player.take_turn(state)
            self.step(action)
