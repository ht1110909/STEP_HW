from collections import Counter

#given a dictionary, return all the possible anagrams

#calculate score
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

def calculate_score(word):
    """
    i was not sure if I was suppoed to calculate score on my own or
    use script
    """
    score = 0
    for character in list(word):
        score += SCORES[ord(character) - ord('a')]
    return score

def load_dictionary(dictionary_file):
    with open(dictionary_file, 'r') as file:
        return [line.strip() for line in file if line.strip()]

#sort dictionary
def sort_dictionary(dictionary):
    """
    dictionary is a text file
    """
    new_dict = []
    with open(dictionary, 'r') as file:
        for word in file:
            new_dict.append(("".join(sorted(word.strip())), word.strip()))
    new_dict = sorted(new_dict, key = lambda words:words[0])
    return new_dict


def find_anagram(dictionary, word):
    #sort given word
    sorted_word = "".join(sorted(word))
    sorted_dictioanry = sort_dictionary(dictionary)
    anagram = binary_search(sorted_dictioanry, sorted_word)
    return anagram

def find_all(dictinoary, word):
    """
    It is extremely slow when it comes to 10000 lines of words!
    """
    if not word:
        return []

    word_counter = Counter(word)
    results = []

    for candidate in dictinoary:
        candidate_counter = Counter(candidate)
        if all(word_counter[ch] >= count for ch, count in candidate_counter.items()):
            results.append(candidate)

    return results

def binary_search(dictionary, word):
    """
    run binary search on a given dictionary and a word,
    both already sorted alphabetically
    """
    if not dictionary:
        return None

    num_words = len(dictionary)
    middle = num_words//2
    looking_word = dictionary[middle][0]
    #print(looking_word)
    if looking_word == word:
        return dictionary[middle][1]
    if looking_word < word:
        return binary_search(dictionary[middle+1:], word)
    if looking_word > word:
        return binary_search(dictionary[:middle], word)
    return None


def process_file(dictionary_words, input_file, output_file):
    dictionary = load_dictionary(dictionary_words)
    with open(input_file, 'r') as inputfile, open(output_file, 'w') as outfile:
        for line in inputfile:
            line = line.strip()
            if not line:
                continue
            anagrams = find_all(dictionary, line)
            anagrams.sort(key = calculate_score, reverse=True)

            if anagrams:
                best = anagrams[0]
                outfile.write(f"{best}\n")
            else:
                raise ValueError("no anagrams found")


if __name__ == "__main__":

    """test cases for find_anagram"""
    #basic case
    dictionary = 'words.txt'

    anagram1 = find_anagram(dictionary, 'nanaba')
    assert anagram1 == 'banana'

    #edge case
    #no anagram found
    anagram2 = find_anagram(dictionary, 'thiswordshouldnotexist')
    assert anagram2 == None

    #two possible anagram (cat and act)
    anagram3 = find_anagram(dictionary, 'tac')
    assert anagram3 == 'cat' or anagram3 == 'act'

    #empty string input
    anagram4 = find_anagram(dictionary, '')
    assert anagram4 == None

    #one character input
    anagram5 = find_anagram(dictionary, 'a')
    assert anagram5 == None

    #very long existing word
    anagram6 = find_anagram(dictionary, 'phalcncegraphtroeoele')
    assert anagram6 == 'electroencephalograph'

    """test cases for find_all"""
    dictionary = load_dictionary('words.txt')

    results = find_all(dictionary, 'forest')
    assert 'forest' in results
    assert 'for' in results
    assert 'rest' in results

    results2 = find_all(dictionary, 'nanaba')
    assert 'banana' in results2

    results3 = find_all(dictionary, 'bbbbbb')
    #print(results3)
    assert results3 == []

    results4 = find_all(dictionary, '')
    assert results4 == []

    process_file('words.txt', 'large.txt', 'large_answer.txt')
