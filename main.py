"""
Main entry point for Rock-Paper-Scissors-Plus Game Referee
ADK Agent setup with HIGHLY POLISHED, animated, dramatic UX
"""

import sys
import io
import time
import os
import random
from typing import Optional

# Set UTF-8 encoding for Windows console compatibility
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from config import VALID_MOVES, MAX_ROUNDS, DEFAULT_STATE
from game_logic import generate_bot_move, get_move_emoji
from game_tools import (
    validate_move_tool,
    resolve_round_tool,
    update_game_state_tool,
    check_game_end_tool,
    reset_game_tool,
    get_game_state_tool
)


# ANSI Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    BLINK = '\033[5m'

    WIN = '\033[92m\033[1m'
    LOSE = '\033[91m\033[1m'
    DRAW = '\033[93m\033[1m'
    BOMB = '\033[95m\033[1m'
    INFO = '\033[96m\033[1m'


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def type_text(text: str, delay: float = 0.02, color: str = ''):
    """Type out text character by character for dramatic effect."""
    for char in text:
        sys.stdout.write(f"{color}{char}{Colors.END}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_loading_bar(text: str = "Loading"):
    """Show a loading animation."""
    print(f"\n{Colors.CYAN}{text}", end='', flush=True)
    for _ in range(20):
        time.sleep(0.05)
        print(".", end='', flush=True)
    print(f"{Colors.END}\n")


def dramatic_pause(duration: float = 0.5):
    """Create suspense with a pause."""
    time.sleep(duration)


def print_banner():
    """Print epic animated welcome banner."""
    clear_screen()

    banner = f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              🎮 ROCK - PAPER - SCISSORS - PLUS 🎮                ║
║                                                                   ║
║         ⚡ THE ULTIMATE BATTLE ARENA ⚡                          ║
║                                                                   ║
║                   🏆 BEST OF 3 ROUNDS 🏆                         ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)


def print_rules():
    """Print game rules with nice formatting."""
    rules = f"""
{Colors.BOLD}{Colors.YELLOW}
╔═══════════════════════════ GAME RULES ═══════════════════════════╗
║                                                                   ║
{Colors.END}
{Colors.CYAN}  ✓ 3 ROUNDS - Most wins claims victory!{Colors.END}
{Colors.GREEN}  ✓ Choose: ROCK 🪨  PAPER 📄  SCISSORS ✂️  BOMB 💣{Colors.END}
{Colors.MAGENTA}  ✓ 💣 BOMB beats everything (ONE TIME ONLY!){Colors.END}
{Colors.RED}  ⚠️  Invalid moves = AUTO-FORFEIT{Colors.END}

{Colors.BOLD}{Colors.YELLOW}║                                                                   ║
╚════════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.INFO}Commands:{Colors.CYAN} 'new game'{Colors.END} | {Colors.RED}'quit'{Colors.END}

"""
    print(rules)


# Bot personality - reactions and taunts
BOT_REACTIONS = {
    "win": [
        "Heh, too easy! 😎",
        "Nice try, human! 🤖",
        "Predictable! 🎯",
        "01000111 01000101 01010100 01000110 01001100 01010101 01000100!",
        "My algorithms never miss! 💪"
    ],
    "lose": [
        "What?! Impossible! 😱",
        "Lucky move... 🤨",
        "I'll get you next round! 🔥",
        "Recalculating strategies... 🧮",
        "Beginner's luck! 🎰"
    ],
    "draw": [
        "Great minds think alike! 🤝",
        "Stalemate! Interesting... 🤔",
        "We're evenly matched! ⚖️",
        "Impressive! You're good! 👏"
    ],
    "bomb_win": [
        "NOOO! My defenses! 💥",
        "Critical system failure! 🚨",
        "ERROR! BOMB DETECTED! ⚠️",
        "You had a bomb?! Sneaky! 😈"
    ],
    "taunt": [
        "Your move, human... ⏳",
        "Make your choice! 🎲",
        "I'm waiting... 😏",
        "Show me what you got! 💪",
        "Tick tock... ⏰"
    ]
}


def get_bot_reaction(situation: str) -> str:
    """Get a random bot reaction."""
    return random.choice(BOT_REACTIONS.get(situation, BOT_REACTIONS["taunt"]))


def get_round_display(round_num: int, max_rounds: int) -> str:
    """Get an animated progress bar."""
    filled = '█' * round_num
    empty = '░' * (max_rounds - round_num)
    return f"{Colors.BOLD}{Colors.CYAN}[{Colors.MAGENTA}{filled}{Colors.END}{empty}] Round {round_num}/{max_rounds}"


def show_reveal_animation(user_move: str, bot_move: str):
    """Show dramatic reveal animation."""
    print(f"\n{Colors.CYAN}{'═' * 65}{Colors.END}")
    print(f"{Colors.BOLD}🎯 REVEALING MOVES...{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 65}{Colors.END}\n")

    # Show user move
    print(f"  {Colors.BOLD}YOUR MOVE:{Colors.END}", end='', flush=True)
    for _ in range(3):
        time.sleep(0.2)
        print(".", end='', flush=True)
    user_emoji = get_move_emoji(user_move)
    print(f" {Colors.GREEN}{user_emoji} {user_move.upper()}{Colors.END} ✓")

    # Dramatic pause before bot move
    print(f"\n  {Colors.BOLD}BOT THINKING{Colors.END}", end='', flush=True)
    for _ in range(5):
        time.sleep(0.15)
        print(".", end='', flush=True)
    print()

    # Reveal bot move with suspense
    bot_emoji = get_move_emoji(bot_move)
    print(f"\n  {Colors.BOLD}BOT'S MOVE:{Colors.END} {Colors.RED}{bot_emoji} {bot_move.upper()}{Colors.END} 💥\n")


class GameSession:
    """Session class for ADK simulation."""

    def __init__(self):
        self.state = DEFAULT_STATE.copy()


class GameRefereeAgent:
    """AI Game Referee with personality and dramatic flair."""

    def __init__(self):
        self.session = GameSession()

    def process_user_input(self, user_input: str) -> str:
        """Process user input with dramatic responses."""
        if user_input.lower().strip() in ["quit", "exit", "q"]:
            return self._handle_quit()

        if user_input.lower().strip() in ["new game", "restart", "reset"]:
            reset_game_tool(self.session)
            return self._get_new_game_message()

        if self.session.state.get("game_over", False):
            return self._format_game_over_menu()

        validation = validate_move_tool(self.session, user_input)

        if not validation["valid"]:
            self._handle_invalid_round(validation["error"])
            return self._format_invalid_response(validation["error"])

        # Generate bot move
        bot_move = generate_bot_move(
            self.session.state.get("user_bomb_used", False),
            self.session.state.get("bot_bomb_used", False),
            self.session.state.get("round", 0)
        )

        # Resolve round
        round_result = resolve_round_tool(
            self.session,
            validation["move"],
            bot_move
        )

        # Update state
        update_game_state_tool(
            self.session,
            round_result["winner"],
            round_result["user_move"],
            round_result["bot_move"],
            round_result["reason"]
        )

        game_status = check_game_end_tool(self.session)

        if game_status["game_over"]:
            return self._format_game_over_response(round_result, game_status)
        else:
            return self._format_round_response(round_result, game_status)

    def _get_new_game_message(self) -> str:
        """New game start message."""
        return f"""
{Colors.GREEN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                    ✨ NEW GAME STARTED! ✨                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}
{self._format_game_header()}
{Colors.INFO}Your move?{Colors.END} {Colors.BOLD}(rock/paper/scissors/bomb){Colors.END}: """

    def _format_game_header(self) -> str:
        """Format game status header."""
        state = self.session.state
        bomb_status = f"{Colors.MAGENTA}💣 READY{Colors.END}" if not state["user_bomb_used"] else f"{Colors.RED}💣 USED{Colors.END}"
        score_color = Colors.GREEN if state['user_score'] >= state['bot_score'] else Colors.RED

        return f"""{Colors.CYAN}{'─' * 65}{Colors.END}
  {Colors.BOLD}SCORE:{Colors.END} {score_color}YOU: {state['user_score']}{Colors.END} │ {Colors.RED}BOT: {state['bot_score']}{Colors.END} │ {bomb_status}
{Colors.CYAN}{'─' * 65}{Colors.END}
"""

    def _handle_invalid_round(self, error: str):
        """Handle invalid input."""
        update_game_state_tool(
            self.session,
            "bot",
            "invalid",
            "forfeit",
            error
        )

    def _format_round_response(self, round_result: dict, game_status: dict) -> str:
        """Format dramatic round response."""
        round_num = self.session.state["round"]
        winner = round_result["winner"]

        # Build the response
        response = f"\n{Colors.CYAN}{'═' * 65}{Colors.END}\n"
        response += f"  {get_round_display(round_num, MAX_ROUNDS)}\n"
        response += f"{Colors.CYAN}{'═' * 65}{Colors.END}"

        # Add reveal animation placeholder
        response += f"""

{Colors.BOLD}{self._get_round_announcement(winner, round_result)}{Colors.END}

{round_result['reason']}

{Colors.CYAN}{'─' * 65}{Colors.END}
"""

        # Bot reaction
        if winner == "user":
            if round_result["bomb_used"]:
                response += f"\n{Colors.MAGENTA}🤖 BOT: {get_bot_reaction('bomb_win')}{Colors.END}\n"
            else:
                response += f"\n{Colors.RED}🤖 BOT: {get_bot_reaction('lose')}{Colors.END}\n"
        elif winner == "bot":
            response += f"\n{Colors.RED}🤖 BOT: {get_bot_reaction('win')}{Colors.END}\n"
        else:
            response += f"\n{Colors.YELLOW}🤖 BOT: {get_bot_reaction('draw')}{Colors.END}\n"

        return response + f"\n{self._format_game_header()}" + f"{Colors.INFO}Your move?{Colors.END} {Colors.BOLD}(rock/paper/scissors/bomb){Colors.END}: "

    def _get_round_announcement(self, winner: str, result: dict) -> str:
        """Get dramatic round announcement."""
        if winner == "user":
            if result["bomb_used"]:
                return f"💥💥💥 NUCLEAR STRIKE! YOU WIN! 💥💥💥"
            return f"🎉🎉🎉 VICTORY IS YOURS! 🎉🎉🎉"
        elif winner == "bot":
            return f"😢😢😢 DEFEAT! 😢😢😢"
        return f"🤝🤝🤝 DRAW! 🤝🤝🤝"

    def _format_invalid_response(self, error: str) -> str:
        """Format invalid input response."""
        round_num = self.session.state["round"]

        response = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                     ⚠️  INVALID MOVE! ⚠️                         ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}

{Colors.YELLOW}{error}{Colors.END}

{Colors.RED}Round forfeited! Bot wins by default.{Colors.END}

{Colors.CYAN}{'─' * 65}{Colors.END}
"""
        return response + self._format_game_header() + f"{Colors.INFO}Your move?{Colors.END} {Colors.BOLD}(rock/paper/scissors/bomb){Colors.END}: "

    def _format_game_over_response(self, round_result: dict, game_status: dict) -> str:
        """Format epic game over response."""
        winner = game_status["winner"]

        if winner == "user":
            banner = self._get_victory_banner()
            color = Colors.GREEN
        elif winner == "bot":
            banner = self._get_defeat_banner()
            color = Colors.RED
        else:
            banner = self._get_tie_banner()
            color = Colors.YELLOW

        response = f"\n{banner}\n\n"

        # Final result
        response += f"{color}{Colors.BOLD}{'═' * 65}{Colors.END}\n"
        response += f"                    FINAL ROUND RESULT{Colors.END}\n"
        response += f"{color}{Colors.BOLD}{'═' * 65}{Colors.END}\n\n"

        user_emoji = get_move_emoji(round_result["user_move"])
        bot_emoji = get_move_emoji(round_result["bot_move"])

        response += f"  {Colors.BOLD}YOUR MOVE:{Colors.END}     {Colors.GREEN}{user_emoji} {round_result['user_move'].upper()}{Colors.END}\n"
        response += f"  {Colors.BOLD}BOT'S MOVE:{Colors.END}     {Colors.RED}{bot_emoji} {round_result['bot_move'].upper()}{Colors.END}\n\n"

        response += f"  {color}{round_result['reason']}{Colors.END}\n\n"

        # Match summary
        response += self._format_match_summary()

        response += f"\n{Colors.CYAN}{'═' * 65}{Colors.END}\n"
        response += f"\n{Colors.BOLD}What's next?{Colors.END}\n"
        response += f"  • {Colors.GREEN}'new game'{Colors.END} - Play again\n"
        response += f"  • {Colors.RED}'quit'{Colors.END} - Exit\n\n"
        response += f"Your choice: "

        return response

    def _format_game_over_menu(self) -> str:
        """Game over menu."""
        state = self.session.state
        return f"""
{Colors.YELLOW}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                      GAME ALREADY OVER                            ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}

{self._format_game_header()}
{Colors.BOLD}What's next?{Colors.END}
  • {Colors.GREEN}'new game'{Colors.END} - Play again
  • {Colors.RED}'quit'{Colors.END} - Exit

Your choice: """

    def _format_match_summary(self) -> str:
        """Generate detailed match summary."""
        state = self.session.state
        summary = f"{Colors.BOLD}📊 MATCH SUMMARY{Colors.END}\n\n"

        for round_data in state.get("history", []):
            r = round_data["round"]
            if round_data["winner"] == "user":
                winner_icon = f"{Colors.GREEN}👤 YOU WIN{Colors.END}"
            elif round_data["winner"] == "bot":
                winner_icon = f"{Colors.RED}🤖 BOT WINS{Colors.END}"
            else:
                winner_icon = f"{Colors.YELLOW}🤝 DRAW{Colors.END}"

            summary += f"  {Colors.CYAN}Round {r}:{Colors.END} {winner_icon}\n"

        summary += f"\n{Colors.BOLD}FINAL:{Colors.END} "
        if state['user_score'] > state['bot_score']:
            summary += f"{Colors.GREEN}YOU WIN {state['user_score']}-{state['bot_score']}{Colors.END} 🏆"
        elif state['bot_score'] > state['user_score']:
            summary += f"{Colors.RED}BOT WINS {state['bot_score']}-{state['user_score']}{Colors.END}"
        else:
            summary += f"{Colors.YELLOW}TIE {state['user_score']}-{state['bot_score']}{Colors.END}"

        return summary

    def _get_victory_banner(self) -> str:
        """Epic victory banner."""
        return f"""{Colors.GREEN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                                                                   ║
║       🏆🏆🏆  ★★★ CHAMPION! ★★★  🏆🏆🏆                        ║
║                                                                   ║
║              YOU HAVE DEFEATED THE BOT!                          ║
║                                                                   ║
║                   CONGRATULATIONS!!!                             ║
║                                                                   ║
║               🎉🎉🎉 VICTORY! 🎉🎉🎉                            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}"""

    def _get_defeat_banner(self) -> str:
        """Defeat banner."""
        return f"""{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                                                                   ║
║              💀 GAME OVER - BOT WINS 💀                          ║
║                                                                   ║
║              BETTER LUCK NEXT TIME, HUMAN                         ║
║                                                                   ║
║                   🤖 0010110101010101 🤖                        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}"""

    def _get_tie_banner(self) -> str:
        """Tie banner."""
        return f"""{Colors.YELLOW}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║                     🤝 PERFECT TIE! 🤝                            ║
║                                                                   ║
║              EVENLY MATCHED OPPONENTS!                            ║
║                                                                   ║
║                 ⚖️ BALANCE ACHIEVED ⚖️                          ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}"""

    def _handle_quit(self) -> str:
        """Handle quit."""
        state = self.session.state
        if state["round"] > 0:
            return f"""
{Colors.CYAN}{'═' * 65}{Colors.END}
{Colors.YELLOW}{Colors.BOLD}                    THANKS FOR PLAYING!{Colors.END}
{Colors.CYAN}{'═' * 65}{Colors.END}

{Colors.BOLD}Final Score:{Colors.END} {Colors.GREEN}You: {state['user_score']}{Colors.END} | {Colors.RED}Bot: {state['bot_score']}{Colors.END}
{Colors.BOLD}Rounds Played:{Colors.END} {state['round']}

{Colors.YELLOW}See you next time! 👋{Colors.END}
"""
        return f"\n{Colors.YELLOW}Thanks for playing! 👋{Colors.END}\n"


def run_cli():
    """Main CLI loop with epic UX."""
    clear_screen()
    print_banner()

    # Animated loading
    print(f"\n{Colors.CYAN}Initializing AI Game Referee", end='', flush=True)
    for i in range(15):
        time.sleep(0.08)
        print(".", end='', flush=True)
    print(f" {Colors.GREEN}READY!{Colors.END}\n")

    agent = GameRefereeAgent()
    print_rules()

    # Initial prompt with bot taunt
    print(agent._format_game_header(), end='')
    print(f"{Colors.INFO}Your move?{Colors.END} {Colors.BOLD}(rock/paper/scissors/bomb){Colors.END} ", end='', flush=True)

    try:
        while True:
            user_input = sys.stdin.readline()

            if not user_input:
                print(f"\n\n{Colors.YELLOW}Thanks for playing! 👋{Colors.END}\n")
                break

            user_input = user_input.strip()

            if not user_input:
                print(f"{Colors.INFO}Your move?{Colors.END} {Colors.BOLD}(rock/paper/scissors/bomb){Colors.END}: ", end='', flush=True)
                continue

            # Process and display
            response = agent.process_user_input(user_input)
            print(response, end="", flush=True)

    except KeyboardInterrupt:
        print(f"\n\n\n{Colors.YELLOW}Game interrupted. Thanks for playing! 👋{Colors.END}\n")
    except Exception as e:
        print(f"\n\n{Colors.RED}⚠️  Error: {e}{Colors.END}\n")


def main():
    """Entry point."""
    run_cli()


if __name__ == "__main__":
    main()
