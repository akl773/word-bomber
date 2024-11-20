from threading import Timer
from dataclasses import dataclass, field
from typing import List, Set
from words import WordFrequencyClassifier


@dataclass
class Player:
    name: str
    lives: int = 3
    words_used: Set[str] = field(default_factory=set)

    def lose_life(self):
        self.lives -= 1

    def has_lives(self) -> bool:
        return self.lives > 0


class WordGame:
    def __init__(self, players: List[str], word_classifier: WordFrequencyClassifier, initial_level: int = 5):
        """
        Initialize the WordGame.
        :param players: List of player names.
        :param word_classifier: Instance of WordFrequencyClassifier.
        :param initial_level: Starting difficulty level (1-10).
        """
        self.players = [Player(name.strip()) for name in players if name.strip()]
        self.word_classifier = word_classifier
        self.level = initial_level
        self.last_successful_level = initial_level
        self.current_word = ""
        self.middle_letters = ""
        self.current_player_index = 0
        self.all_correct_in_round = True  # Tracks if all players answered correctly in the current round

    def select_word(self) -> bool:
        try:
            self.current_word = self.word_classifier.get_word_by_level(self.level)
        except ValueError as e:
            print(f"Error selecting word: {e}")
            return False
        mid_idx = len(self.current_word) // 2
        self.middle_letters = self.current_word[max(0, mid_idx - 1):mid_idx + 2]
        return True

    def next_player(self) -> Player:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]

    def all_players_eliminated(self) -> bool:
        return all(not player.has_lives() for player in self.players)

    def start_game(self):
        print("\n" + "=" * 50)
        print("🔥 Welcome to the Word Game! 🔥")
        print("=" * 50)
        if not self.select_word():
            print("Failed to start the game due to word selection issues.")
            return

        print(f"🎯 Starting word: **{self.current_word}**")
        print(f"🔤 Middle letters to use: **{self.middle_letters}**")

        while not self.all_players_eliminated():
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

        print("\n" + "=" * 50)
        print("🏁 Game over!")
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

    def get_input_with_timeout(self, timeout: int) -> str:
        result = [None]
        timer = Timer(timeout, lambda: None)

        try:
            timer.start()
            result[0] = input("Your word: ").strip()
        except Exception as e:
            print(e)
        finally:
            timer.cancel()

        return result[0]

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


if __name__ == "__main__":
    print("👋 Welcome to the Word Game setup!")
    word_classifier = WordFrequencyClassifier()
    player_names = input("Enter player names (comma-separated): ").split(",")
    try:
        initial_level = int(input("Enter starting difficulty level (1-10): "))
        if not 1 <= initial_level <= 10:
            raise ValueError("Level must be between 1 and 10.")
    except ValueError as e:
        print(f"⚠️ Invalid input: {e}. Defaulting to level 5.")
        initial_level = 5

    game = WordGame(player_names, word_classifier, initial_level=initial_level)
    game.start_game()
