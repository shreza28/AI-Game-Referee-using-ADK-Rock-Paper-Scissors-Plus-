import random
from typing import Dict, Literal, Optional
from config import VALID_MOVES, WIN_MATRIX


def is_valid_move(move: str) -> bool:
    """
    Check if a move is valid.

    Args:
        move: The move to validate

    Returns:
        True if move is valid, False otherwise
    """
    normalized = move.lower().strip()
    return normalized in VALID_MOVES


def normalize_move(move: str) -> Optional[str]:
    """
    Normalize user input to a valid move name.

    Args:
        move: Raw user input

    Returns:
        Normalized move name or None if invalid
    """
    if not move:
        return None
    normalized = move.lower().strip()
    return normalized if normalized in VALID_MOVES else None


def determine_winner(user_move: str, bot_move: str) -> Dict:
    """
    Determine the winner of a round given both moves.

    Args:
        user_move: User's validated move
        bot_move: Bot's chosen move

    Returns:
        Dictionary with winner, reason, and bomb_used flag
    """
    # Handle bomb special cases first
    if user_move == "bomb" and bot_move == "bomb":
        return {
            "winner": "draw",
            "reason": "Both players used bomb! It's a draw.",
            "bomb_used": True
        }
    elif user_move == "bomb":
        return {
            "winner": "user",
            "reason": f"💥 BOOM! Your bomb obliterated the bot's {bot_move}!",
            "bomb_used": True
        }
    elif bot_move == "bomb":
        return {
            "winner": "bot",
            "reason": f"💥 BOOM! Bot's bomb obliterated your {user_move}!",
            "bomb_used": True
        }

    # Standard RPS rules
    if user_move == bot_move:
        return {
            "winner": "draw",
            "reason": f"Both chose {user_move}. It's a draw!",
            "bomb_used": False
        }

    # Check win matrix
    if WIN_MATRIX[user_move] == bot_move:
        return {
            "winner": "user",
            "reason": f"{user_move.capitalize()} beats {bot_move}!",
            "bomb_used": False
        }
    else:
        return {
            "winner": "bot",
            "reason": f"{bot_move.capitalize()} beats {user_move}!",
            "bomb_used": False
        }


def can_use_bomb(bomb_used: bool) -> bool:
    """
    Check if bomb can be used.

    Args:
        bomb_used: Whether bomb has already been used

    Returns:
        True if bomb is available, False otherwise
    """
    return not bomb_used


def generate_bot_move(user_bomb_used: bool, bot_bomb_used: bool, current_round: int) -> str:
    """
    Generate a bot move with basic strategy.

    Strategy:
    - Save bomb for critical rounds
    - Use bomb strategically if user hasn't used theirs
    - Otherwise vary moves randomly

    Args:
        user_bomb_used: Whether user has used their bomb
        bot_bomb_used: Whether bot has used its bomb
        current_round: Current round number (0-2)

    Returns:
        Bot's chosen move
    """
    normal_moves = ["rock", "paper", "scissors"]

    if not bot_bomb_used:
        if current_round == 2 and not user_bomb_used:
            if random.random() < 0.7:  
                return "bomb"

        if current_round == 0 and random.random() < 0.2:
            return "bomb"

        if current_round == 1 and random.random() < 0.4:
            return "bomb"

    return random.choice(normal_moves)


def calculate_final_winner(user_score: int, bot_score: int) -> Literal["user", "bot", "tie"]:
    """
    Calculate the overall winner based on scores.

    Args:
        user_score: User's total wins
        bot_score: Bot's total wins

    Returns:
        "user", "bot", or "tie"
    """
    if user_score > bot_score:
        return "user"
    elif bot_score > user_score:
        return "bot"
    else:
        return "tie"


def format_score(user_score: int, bot_score: int) -> str:
    """
    Format the score for display.

    Args:
        user_score: User's score
        bot_score: Bot's score

    Returns:
        Formatted score string
    """
    return f"You {user_score} - {bot_score} Bot"


def get_move_emoji(move: str) -> str:
    """
    Get emoji for a move.

    Args:
        move: The move name

    Returns:
        Emoji string
    """
    emojis = {
        "rock": "🪨",
        "paper": "📄",
        "scissors": "✂️",
        "bomb": "💣"
    }
    return emojis.get(move, "")
