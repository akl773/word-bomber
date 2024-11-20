
# Word Bomber

Word Bomber is a fun and interactive word game where players compete by quickly responding with valid words containing specific letters. Players must act fast before the timer runs out, or they lose a life! The game gets progressively harder, adding more challenges as players succeed.

## Features

- **Multiplayer Fun**: Play with friends by adding multiple players.
- **Dynamic Word Challenges**: Words change dynamically based on player success.
- **Timeout Mechanism**: Players lose a life if they fail to respond within the given time.
- **Difficulty Levels**: Adjustable starting difficulty to suit all players.
- **Word Validation**: Ensures submitted words are valid and follow the game's rules.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd word-bomber
   ```

2. Run the setup script to automate the environment creation and dependencies installation:
   ```bash
   ./setup.sh
   ```

3. Activate the virtual environment (if not already activated):
   ```bash
   source .env/bin/activate
   ```

4. Run the game:
   ```bash
   python main.py
   ```

## Requirements

- Python 3.8 or later
- Dependencies listed in `requirements.txt`

## How to Play

1. Run the game using `python main.py`.
2. Enter player names and choose the starting difficulty level.
3. Take turns responding with words containing the specified middle letters.
4. Act quickly to avoid losing lives!
5. The game ends when all players are out of lives or choose to stop.

## File Structure

- `main.py`: The main entry point of the game.
- `words.py`: Handles word classification and validation logic.
- `requirements.txt`: Specifies project dependencies.
- `setup.sh`: Automates environment setup, dependency installation, and downloading the NLTK `brown` corpus.
- `.gitignore`: Lists files and folders to exclude from Git.

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Enjoy playing Word Bomber with your friends and family!
