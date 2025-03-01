# imports
import nltk

nltk.download("words")
from nltk.corpus import words


def get_user_input():
    sides = []
    used_letters = set()  # Keep track of all letters used across all entries

    for i in range(4):  # Repeat 4 times
        while True:
            print(f"\nSide {i + 1}:")
            set1 = input("Enter first letter: ").strip().lower()
            set2 = input("Enter second letter: ").strip().lower()
            set3 = input("Enter third letter: ").strip().lower()

            # Convert input into a set for uniqueness check
            one_side_set = {set1, set2, set3}

            # Validate: each must be a single letter, unique within entry, and not used before
            if (
                all(len(s) == 1 and s.isalpha() for s in one_side_set)
                and len(one_side_set) == 3
                and one_side_set.isdisjoint(used_letters)
            ):

                sides.append((set1, set2, set3))
                used_letters.update(one_side_set)  # Add new letters to the used set
                break  # Move to the next entry
            else:
                print(
                    "Invalid input! Ensure all are single unique letters, and no duplicates across all entries."
                )

    return sides, used_letters


def filter_words_by_letters(allowed_letters, word_list):
    def initial_is_valid(word):
        # Must be at least 3 letters long
        if len(word) < 3:
            return False
        # Must only contain allowed letters
        if not set(word).issubset(allowed_letters):
            return False
        # No consecutive duplicate letters
        for i in range(len(word) - 1):
            if word[i] == word[i + 1]:
                return False
        return True

    filtered_words = [word for word in word_list if initial_is_valid(word)]
    return filtered_words


# Loop through every pair of words of words on the filtered word list
# Check if the pair of words is valid - here are the rules:
# there words must share a last and first letter, e.g like - every. like ends in e and every starts in e
# the two words must use ever letter in the entire set (all 12 letters)
# each consecutive letter of the individual word must come from the a different set in user entries


def is_valid_word_pair(word1, word2, sides, full_letter_set):
    """
    Checks if a pair of words meets all conditions:
    - word1 ends with the same letter that word2 starts with.
    - Both words together use all 12 letters.
    - Each consecutive letter in a word must come from a different user entry set.
    """
    # Check if word1 ends with the first letter of word2
    if word1[-1] != word2[0]:
        return False

    # Ensure the combined word set uses all 12 letters
    combined_letters = set(word1) | set(word2)
    if combined_letters != full_letter_set:
        return False

    # Check if each consecutive letter comes from a different side
    def follows_side_rule(word):
        for i in range(len(word) - 1):
            letter1 = word[i]
            letter2 = word[i + 1]

            # Find which sets these letters belong to
            side1 = next((side for side in sides if letter1 in side), None)
            side2 = next((side for side in sides if letter2 in side), None)

            # If letters are in the same entry, rule is broken
            if side1 == side2:
                return False
        return True

    return follows_side_rule(word1) and follows_side_rule(word2)


def find_valid_word_pairs(filtered_word_list, user_entries, full_letter_set):
    """
    Loops through every pair of words and prints valid pairs.
    """
    valid_pairs = []

    for i, word1 in enumerate(filtered_word_list):
        for j, word2 in enumerate(filtered_word_list):
            if i != j and is_valid_word_pair(
                word1, word2, user_entries, full_letter_set
            ):
                valid_pairs.append((word1, word2))

    # Print valid pairs
    print("\nValid Word Pairs:")
    for pair in valid_pairs[:20]:  # Show only first 20 pairs for brevity
        print(f"{pair[0]} -> {pair[1]}")

    print(f"\nTotal valid pairs found: {len(valid_pairs)}")
    return valid_pairs


def main():
    # Create Word List
    word_list = set(words.words())

    # Input Letters
    sides, letters = get_user_input()
    print("\nYou entered:")
    for i, (set1, set2, set3) in enumerate(sides, start=1):
        print(f"Entry {i}: {set1}, {set2}, {set3}")

    # Filter word list
    filtered_word_list = filter_words_by_letters(letters, word_list)

    # Find valid words
    valid_word_pairs = find_valid_word_pairs(filtered_word_list, sides, letters)


main()
