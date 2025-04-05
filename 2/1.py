from itertools import permutations
from collections import Counter

word = "АБРАКАДАБРА"
letter_counts = Counter(word)


def count_unique_words(word, length):
    unique_words = set()
    for p in permutations(word, length):
        unique_words.add(p)
    return len(unique_words)


result = count_unique_words(word, 5)
print(f"Количество различных 5-буквенных слов: {result}")
