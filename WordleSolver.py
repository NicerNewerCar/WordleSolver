from nltk.corpus import brown, words
import random
# correctness -1 is not set, 1 is correct spot, 2 is in word, and 3 is incorrect
# position -1 is not set, 1 is first letter, 2 is second letter, 3 is third letter, etc.
class Letter:
    def __init__(self, char, correctness, position, null_positions):
        self.char = char
        self.correctness = correctness
        self.position = position
        self.null_positions = null_positions
    def __str__(self):
        return self.char + " " + str(self.correctness) + " " + str(self.position) + " " + str(self.null_positions)

def create_alphabet():
    alphabet = {
        'a' : Letter('a', -1, -1, []),
        'b' : Letter('b', -1, -1, []),
        'c' : Letter('c', -1, -1, []),
        'd' : Letter('d', -1, -1, []),
        'e' : Letter('e', -1, -1, []),
        'f' : Letter('f', -1, -1, []),
        'g' : Letter('g', -1, -1, []),
        'h' : Letter('h', -1, -1, []),
        'i' : Letter('i', -1, -1, []),
        'j' : Letter('j', -1, -1, []),
        'k' : Letter('k', -1, -1, []),
        'l' : Letter('l', -1, -1, []),
        'm' : Letter('m', -1, -1, []),
        'n' : Letter('n', -1, -1, []),
        'o' : Letter('o', -1, -1, []),
        'p' : Letter('p', -1, -1, []),
        'q' : Letter('q', -1, -1, []),
        'r' : Letter('r', -1, -1, []),
        's' : Letter('s', -1, -1, []),
        't' : Letter('t', -1, -1, []),
        'u' : Letter('u', -1, -1, []),
        'v' : Letter('v', -1, -1, []),
        'w' : Letter('w', -1, -1, []),
        'x' : Letter('x', -1, -1, []),
        'y' : Letter('y', -1, -1, []),
        'z' : Letter('z', -1, -1, [])
    }
    return alphabet

def print_alphabet(alphabet):
    print("char cor pos null")
    for key in alphabet:
        print(alphabet[key])

def check_keys_in_word(word,keys):
    for char in word:
        if char in keys:
            return True
    return False

def check_keys(word,keys):
    for char in keys:
        if char not in word:
            return False
    return True

def get_word_and_correctness(word,alphabet):
    if word == None:
        word = input("Enter a word: ")
        word = word.lower()
    for i in range(len(word)):
        char = word[i]
        if char in alphabet and alphabet[char].correctness not in [1,3]:
            alphabet[char].correctness = int(input("Is " + char + " correct? 1 for yes, 2 for in word, 3 for incorrect: "))
            if alphabet[char].correctness == 1:
                alphabet[char].position = i + 1
            if alphabet[char].correctness == 2:
                alphabet[char].null_positions += [i + 1]     

def split(word): 
    return [char for char in word]  

def suggest_word(alphabet):
    filtered_words = list(filter(lambda x: len(x) == 5, words.words()))
    filtered_words = list(filter(lambda x: x.isalpha(), filtered_words))
    filtered_words = list(map(lambda x: x.lower(), filtered_words))
    unique_words = set(filtered_words)
    unique_words = list(unique_words)
    setLetters = {}
    for key in alphabet:
        if alphabet[key].position != -1:
            setLetters[alphabet[key].position] = key
    unSetLetters = {}
    for key in alphabet:
        if alphabet[key].correctness == 2:
            unSetLetters[key] = alphabet[key].null_positions
    voidLetters = {}
    for key in alphabet:
        if alphabet[key].correctness == 3:
            voidLetters[key] = key
    split_words = list(map(lambda x: split(x), unique_words))


    possible_words = []
    if len(setLetters) > 0:
        for word in split_words:
            counter = 0
            for key in setLetters:
                if word[key-1] == setLetters[key]:
                    counter += 1
            if counter == len(setLetters):
                possible_words.append(''.join(word))
        words_to_remove = []
        for word in possible_words:
            if check_keys(''.join(word),list(unSetLetters.keys())):
                for key in unSetLetters:
                    for i in range(len(unSetLetters[key])):
                        if word[unSetLetters[key][i]-1] == key:
                            words_to_remove.append(''.join(word))
            else:
                words_to_remove.append(''.join(word))
            if check_keys_in_word(''.join(word),list(voidLetters.keys())):
                words_to_remove.append(''.join(word))
        words_to_remove = list(set(words_to_remove))
        for word in words_to_remove:
            possible_words.remove(word)



    elif len(unSetLetters) > 0:
        for word in split_words:
            if check_keys(''.join(word),list(unSetLetters.keys())):
                for key in unSetLetters:
                    counter = 0
                    for i in range(len(unSetLetters[key])):
                        if word[unSetLetters[key][i]-1] == key:
                            counter += 1
                    if counter == 0:
                        possible_words.append(''.join(word))
        words_to_remove = []
        for word in possible_words:
            if check_keys_in_word(word,list(voidLetters.keys())):
                words_to_remove.append(word)
        words_to_remove = list(set(words_to_remove))
        for word in words_to_remove:
            possible_words.remove(word)
        possible_words = list(set(possible_words))



    else:
        for word in split_words:
            if not check_keys_in_word(word,list(voidLetters.keys())):
                possible_words.append(''.join(word))
    return possible_words

        
            



# TODO:
#1. Add a function that grabs the users screen
#2. Add a function that analyzes the screen and updates the alphabet
#3. Add a function that simulates the user typing the word
#4. Remove names/places from the list of words

alphabet = create_alphabet()
starters = ['slice','tried','crane','reach','bakes','roast','adieu']
random.shuffle(starters)
print("Suggested starting word: ", starters[0])
get_word_and_correctness(None,alphabet)
for _ in range(5):
    suggestions = suggest_word(alphabet)
    random.shuffle(suggestions)
    for word in suggestions:
        print(word)
        x = int(input("Does this word work? 1 for yes, 2 for no: "))
        if x == 1:
            get_word_and_correctness(word,alphabet)
            break
    # get_word_and_correctness(None,alphabet)