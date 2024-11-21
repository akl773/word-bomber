import selectors
import sys
from dataclasses import dataclass, field

from words import WordFrequencyClassifier


@dataclass
class Player:
    name: str
    lives: int = 3
    words_used: set[str] = field(default_factory=set)

    def lose_life(self):
        self.lives -= 1

    def has_lives(self) -> bool:
        return self.lives > 0


class WordGame:
    def __init__(self, players: list[str], word_classifier: WordFrequencyClassifier, initial_level: int = 5):
        """
        Initialize the WordGame.
        :param players: List of player names.
        :param word_classifier: Instance of WordFrequencyClassifier.
        :param initial_level: Starting difficulty level (1-10).
        """
        if len(players) < 2:
            raise ValueError("At least 2 players are required to start the game.")
        if not 1 <= initial_level <= 10:
            raise ValueError("Level must be between 1 and 10.")

        self.players = [Player(name.strip()) for name in players if name.strip()]
        self.word_classifier = word_classifier
        self.level = initial_level
        self.last_successful_level = initial_level
        self.current_word = ""
        self.middle_letters = ""
        self.current_player_index = 0
        self.all_correct_in_round = True  # Tracks if all players answered correctly in the current round

    def select_word(self) -> bool:
        """
        Selects a word for the current level. Ensures the word contains only alphabetic characters.
        :return: True if a valid word is selected, False otherwise.
        """
        try:
            self.current_word = self.word_classifier.get_word_by_level(self.level)

            # Validate the word to ensure it contains only alphabetic characters
            if not self.current_word.isalpha():
                print(f"Invalid word selected: {self.current_word}. Retrying...")
                return self.select_word()

        except ValueError as e:
            print(f"Error selecting word: {e}")
            return False

        # Extract middle letters for the current word
        mid_idx = len(self.current_word) // 2
        self.middle_letters = self.current_word[max(0, mid_idx - 1):mid_idx + 2]
        return True

    def next_player(self) -> Player:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    def start_game(self):
        print("\n" + "=" * 50)
        print("🔥 Welcome to the Word Game! 🔥")
        print("=" * 50)

        if not self.select_word():
            print("Failed to start the game due to word selection issues.")
            return

        print(f"🔤 Middle letters to use: **{self.middle_letters}**")

        while len([player for player in self.players if player.has_lives()]) > 1:
            current_player = self.players[self.current_player_index]
            if not current_player.has_lives():
                self.next_player()
                continue

            print("\n" + "-" * 50)
            print(f"🎮 {current_player.name}'s turn! Lives remaining: {current_player.lives}")
            print(f"📝 Enter a word containing: **{self.middle_letters}** (You have 10 seconds!)")

            word = self.get_input_with_timeout(10)
            if word is None:
                print(f"⏰ {current_player.name} took too long!")
                current_player.lose_life()
                self.all_correct_in_round = False
            elif self.is_valid_submission(word, current_player):
                print(f"✅ Great! **{word}** is a valid word.")
                current_player.words_used.add(word)

                # Select a new word after a correct answer
                if not self.select_word():
                    print("⚠️ Failed to select a new word. Ending game.")
                    break
                print(f"🎯 New middle letters to use: **{self.middle_letters}**")
            else:
                print(f"❌ Invalid word or already used! {current_player.name} loses a life.")
                current_player.lose_life()
                self.all_correct_in_round = False

            if current_player.lives == 0:
                print(f"💀 {current_player.name} is out of the game!")

            self.next_player()

            # Check if the round is over (all players have played once)
            if self.current_player_index == 0:
                self.adjust_difficulty()

        # Declare the winner
        print("\n" + "=" * 50)
        self.display_winner()
        print("=" * 50)

    def adjust_difficulty(self):
        if self.all_correct_in_round:
            print("\n🎉 All players answered correctly! Increasing difficulty level.")
            self.last_successful_level = self.level
            if self.level < 10:
                self.level += 1
        else:
            print("\n🔄 Someone made a mistake. Keeping difficulty level.")
            self.level = self.last_successful_level
        self.all_correct_in_round = True  # Reset for the next round

        if not self.select_word():
            print("⚠️ Failed to select a word for the new level.")

    @staticmethod
    def get_input_with_timeout(timeout: int) -> str | None:
        """
        Prompt the user for input with a timeout. Returns None if the user fails to respond within the timeout.
        """

        print("Your word: ", end="", flush=True)

        # Use a selector to monitor stdin for input
        selector = selectors.DefaultSelector()
        selector.register(sys.stdin, selectors.EVENT_READ)

        # Wait for input or timeout
        events = selector.select(timeout)
        if events:
            user_input = sys.stdin.readline().strip()
            return user_input
        else:
            return None  # Timeout occurred

    def is_valid_submission(self, word: str, player: Player) -> bool:
        return (
                self.middle_letters in word
                and word not in player.words_used
                and self.word_classifier.is_valid_word(word)
        )

    def display_winner(self):
        alive_players = [player for player in self.players if player.has_lives()]
        if alive_players:
            print(f"🏆 Winner(s): {', '.join(player.name for player in alive_players)}")
        else:
            print("🤷 No winners this time!")


def main():
    print("👋 Welcome to the Word Game setup!")
    word_classifier = WordFrequencyClassifier()

    # Ensure at least two players
    while True:
        player_names = input("Enter player names (comma-separated): ").split(",")
        player_names = [name.strip() for name in player_names if name.strip()]  # Remove empty names
        if len(player_names) < 2:
            print("⚠️ At least two players are required to start the game. Please enter again.")
        else:
            break

    # Input starting difficulty level
    try:
        initial_level = int(input("Enter starting difficulty level (1-10): "))
        if not 1 <= initial_level <= 10:
            raise ValueError("Level must be between 1 and 10.")
    except ValueError as e:
        print(f"⚠️ Invalid input: {e}. Defaulting to level 5.")
        initial_level = 5

    # Start the game
    game = WordGame(player_names, word_classifier, initial_level=initial_level)
    game.start_game()


if __name__ == "__main__":
    main()
