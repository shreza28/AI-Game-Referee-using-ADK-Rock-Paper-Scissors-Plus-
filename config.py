"""
Configuration and constants for Rock-Paper-Scissors-Plus Game Referee
"""

# Game constants
VALID_MOVES = ["rock", "paper", "scissors", "bomb"]
MAX_ROUNDS = 3
BOMB_LIMIT = 1  # per player

# Win rules matrix - what each move beats
WIN_MATRIX = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
    "bomb": ["rock", "paper", "scissors"]  # bomb beats all normal moves
}

# Game state schema
STATE_SCHEMA = {
    "round": int,           # Current round number (0-3)
    "user_score": int,      # User's wins
    "bot_score": int,       # Bot's wins
    "user_bomb_used": bool, # Whether user used bomb
    "bot_bomb_used": bool,  # Whether bot used bomb
    "game_over": bool,      # Game completion flag
    "winner": str,          # "user", "bot", or "tie"
    "history": list         # List of round results
}

# Default state for new games
DEFAULT_STATE = {
    "round": 0,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_over": False,
    "winner": None,
    "history": []
}

# Response templates
GAME_INTRO = """Welcome to Rock-Paper-Scissors-Plus! 🎮

Rules: Best of 3 rounds. Choose: rock, paper, scissors, or bomb (once per game).
Bomb beats everything except another bomb. Invalid moves waste your turn.
"""

ROUND_PROMPT = "Your move? (rock/paper/scissors/bomb): "
