from typing import Dict, Optional
from game_logic import (
    normalize_move,
    determine_winner,
    generate_bot_move,
    calculate_final_winner,
    format_score
)
from config import VALID_MOVES, MAX_ROUNDS, DEFAULT_STATE


def validate_move_tool(session, move: str) -> Dict:
    """
    Validates a user's move against game rules.

    ADK Tool: Checks if the move is valid and if bomb can be used.

    Args:
        session: ADK session object with state
        move: The user's input move

    Returns:
        Dictionary with validation result
    """
    # Initialize state if needed
    if not hasattr(session, 'state') or not session.state:
        session.state = DEFAULT_STATE.copy()

    # Normalize input
    normalized = normalize_move(move)

    # Check validity
    if not normalized:
        return {
            "valid": False,
            "move": None,
            "can_use_bomb": not session.state.get("user_bomb_used", False),
            "error": f"Invalid move '{move}'. Choose: rock, paper, scissors, or bomb"
        }

    # Check bomb usage
    if normalized == "bomb":
        if session.state.get("user_bomb_used", False):
            return {
                "valid": False,
                "move": None,
                "can_use_bomb": False,
                "error": "You've already used your bomb this game!"
            }

    return {
        "valid": True,
        "move": normalized,
        "can_use_bomb": not session.state.get("user_bomb_used", False),
        "error": None
    }


def resolve_round_tool(session, user_move: str, bot_move: str) -> Dict:
    """
    Determines the winner of a round given both moves.

    ADK Tool: Calculates round outcome based on game rules.

    Args:
        session: ADK session object
        user_move: User's validated move
        bot_move: Bot's chosen move

    Returns:
        Dictionary with round result
    """
    # Determine winner using game logic
    result = determine_winner(user_move, bot_move)

    return {
        "winner": result["winner"],
        "reason": result["reason"],
        "bomb_used": result["bomb_used"],
        "user_move": user_move,
        "bot_move": bot_move
    }


def update_game_state_tool(session, winner: str, user_move: str,
                          bot_move: str, reason: str) -> Dict:
    """
    Updates the game state after a completed round.

    ADK Tool: Mutates session state with new round information.

    Args:
        session: ADK session object
        winner: Round winner ("user", "bot", or "draw")
        user_move: User's move
        bot_move: Bot's move
        reason: Outcome explanation

    Returns:
        Dictionary with updated state
    """
    # Initialize state if needed
    if not hasattr(session, 'state') or not session.state:
        session.state = DEFAULT_STATE.copy()

    # Increment round
    current_round = session.state.get("round", 0)
    session.state["round"] = current_round + 1

    # Update scores
    if winner == "user":
        session.state["user_score"] += 1
    elif winner == "bot":
        session.state["bot_score"] += 1

    # Track bomb usage
    if user_move == "bomb":
        session.state["user_bomb_used"] = True
    if bot_move == "bomb":
        session.state["bot_bomb_used"] = True

    # Record history
    if "history" not in session.state:
        session.state["history"] = []

    session.state["history"].append({
        "round": session.state["round"],
        "user_move": user_move,
        "bot_move": bot_move,
        "winner": winner,
        "reason": reason
    })

    return {
        "success": True,
        "round": session.state["round"],
        "user_score": session.state["user_score"],
        "bot_score": session.state["bot_score"],
        "user_bomb_used": session.state["user_bomb_used"],
        "bot_bomb_used": session.state["bot_bomb_used"],
        "message": f"Round {session.state['round']} complete"
    }


def check_game_end_tool(session) -> Dict:
    """
    Checks if the game should end and determines the winner.

    ADK Tool: Evaluates game completion and calculates final result.

    Args:
        session: ADK session object

    Returns:
        Dictionary with game end status
    """
    # Initialize state if needed
    if not hasattr(session, 'state') or not session.state:
        session.state = DEFAULT_STATE.copy()

    current_round = session.state.get("round", 0)
    user_score = session.state.get("user_score", 0)
    bot_score = session.state.get("bot_score", 0)

    # Check if game complete
    if current_round >= MAX_ROUNDS:
        session.state["game_over"] = True
        winner = calculate_final_winner(user_score, bot_score)
        session.state["winner"] = winner

        if winner == "user":
            reason = f"🎉 You won {user_score}-{bot_score}!"
        elif winner == "bot":
            reason = f"🤖 Bot won {bot_score}-{user_score}."
        else:
            reason = f"🤝 It's a tie at {user_score}-{bot_score}!"

        return {
            "game_over": True,
            "winner": winner,
            "final_score": {
                "user": user_score,
                "bot": bot_score
            },
            "reason": reason,
            "score_display": format_score(user_score, bot_score)
        }

    return {
        "game_over": False,
        "winner": None,
        "final_score": {
            "user": user_score,
            "bot": bot_score
        },
        "reason": f"Round {current_round + 1} of {MAX_ROUNDS}",
        "score_display": format_score(user_score, bot_score)
    }


def reset_game_tool(session) -> Dict:
    """
    Resets the game state for a new game.

    ADK Tool: Initializes a fresh game state.

    Args:
        session: ADK session object

    Returns:
        Dictionary with new game state
    """
    session.state = DEFAULT_STATE.copy()

    return {
        "success": True,
        "message": "New game started!",
        "state": session.state
    }


def get_game_state_tool(session) -> Dict:
    """
    Retrieves the current game state.

    ADK Tool: Returns current state for display purposes.

    Args:
        session: ADK session object

    Returns:
        Current game state
    """
    # Initialize state if needed
    if not hasattr(session, 'state') or not session.state:
        session.state = DEFAULT_STATE.copy()

    return {
        "round": session.state.get("round", 0),
        "user_score": session.state.get("user_score", 0),
        "bot_score": session.state.get("bot_score", 0),
        "user_bomb_used": session.state.get("user_bomb_used", False),
        "bot_bomb_used": session.state.get("bot_bomb_used", False),
        "game_over": session.state.get("game_over", False),
        "winner": session.state.get("winner"),
        "history": session.state.get("history", [])
    }
