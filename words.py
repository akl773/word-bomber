import nltk
from nltk.corpus import brown


def ensure_nltk_data(resource):
    """ Ensure that the nltk data is available """
    try:
        nltk.data.find(f'corpora/{resource}')
    except LookupError:
        print(f"Downloading {resource}...")
        nltk.download(resource)


ensure_nltk_data('brown')


class WordFrequencyClassifier:
    def __init__(self):
        # Get word frequencies from Brown Corpus
        self.word_freq = nltk.FreqDist(brown.words())
        self.word_levels = self.__categorize_words()

    def __categorize_words(self):
        # Sort words by frequency
        sorted_words = sorted(self.word_freq.items(), key=lambda x: x[1], reverse=True)

        # Divide into 10 levels
        total_words = len(sorted_words)
        level_size = total_words // 10

        levels = {i: [] for i in range(1, 11)}
        for level in range(1, 11):
            start = (level - 1) * level_size
            end = level * level_size
            level_words = [word for word, _ in sorted_words[start:end]]
            levels[level] = level_words

        return levels

    def get_word_by_level(self, level):
        from random import choice
        return choice(self.word_levels[level])

    def is_valid_word(self, word):
        return word.lower() in self.word_freq
