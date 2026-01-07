# 🎮 Rock-Paper-Scissors-Plus Game Referee

An AI-powered chatbot that acts as a referee for an enhanced Rock-Paper-Scissors game with bomb mechanics. Built with Python and designed for integration with Google ADK.

## Game Overview

**Best of 3 rounds** with special mechanics:
- **Valid moves**: rock, paper, scissors, or bomb (once per game)
- **Bomb** beats all other moves
- **Bomb vs bomb** = draw
- **Invalid inputs** waste the round
- **Auto-termination** after 3 rounds

## Features

- ✅ Intelligent move validation and interpretation
- ✅ Strategic bot AI with smart bomb usage
- ✅ Complete game state tracking
- ✅ Clear, conversational interface
- ✅ Graceful error handling
- ✅ Match history and summaries
- ✅ Clean separation: Intent → Logic → Response

## Architecture

```
┌─────────────────────────────────┐
│     User Input (CLI Interface)  │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Intent Understanding Layer    │
│   (GameRefereeAgent)            │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│      ADK Tools Layer            │
│  • validate_move                │
│  • resolve_round                │
│  • update_game_state            │
│  • check_game_end               │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│      Game Logic Layer           │
│  (Pure functions)               │
│  • Rules enforcement            │
│  • Win calculation              │
│  • Bot strategy                 │
└────────────┬────────────────────┘
             ↓
┌─────────────────────────────────┐
│   Response Generation           │
│   (Formatted output)            │
└─────────────────────────────────┘
```

## 📁 Project Structure

```
rps_game_referee/
├── config.py           # Game constants and configuration
├── game_logic.py       # Core game rules (pure functions)
├── game_tools.py       # ADK tools for state management
├── main.py             # Agent setup and CLI interface
├── requirements.txt    # Dependencies
├── README.md           # This file

```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- No external dependencies required (uses stdlib only)

### Installation

1. **Clone or download the project**
   ```bash
   cd assignment upliance
   ```

2. **Verify Python version**
   ```bash
   python --version  # Should be 3.8+
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

##  Acknowledgments

- Google ADK documentation and examples
- Assignment requirements and specifications
- Rock-Paper-Scissors game theory

