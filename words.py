import csv
from random import choice


class WordFrequencyClassifier:

    def __init__(self, file_path="word_frequency.csv"):
        self.file_path = file_path
        self.word_levels = self.__load_word_data()

    def __load_word_data(self):
        """
        Loads word data from a CSV file and groups words by frequency levels.
        Assumes CSV has columns: 'word', 'frequency'.
        """
        # Define frequency ranges for each level
        frequency_ranges = [
            (9000, float('inf'), 1),
            (8000, 9000, 2),
            (7000, 8000, 3),
            (6000, 7000, 4),
            (5000, 6000, 5),
            (4000, 5000, 6),
            (3000, 4000, 7),
            (2000, 3000, 8),
            (1000, 2000, 9),
            (0, 1000, 10)
        ]

        # Initialize levels dictionary
        levels = {i: [] for i in range(1, 11)}

        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    word = row['word']
                    frequency = int(row['frequency'])

                    # Determine the level based on frequency ranges
                    for min_freq, max_freq, level in frequency_ranges:
                        if min_freq <= frequency < max_freq:
                            levels[level].append(word)
                            break

        except Exception as e:
            print(f"Error loading data: {e}")

        return levels

    def get_word_by_level(self, level):
        """
        Get a random word from the specified level.
        """
        if level < 1 or level > 10:
            raise ValueError("Level must be between 1 and 10.")
        if not self.word_levels[level]:
            raise ValueError(f"No words available for level {level}.")
        return choice(self.word_levels[level])
