from nltk.corpus import brown, words
import random

class Positions:
    def __init__(self,nullLetters,correctLetter,avaliableLetters):
        self.nullLetters = nullLetters
        self.correctLetter = correctLetter
        self.avaliableLetters = avaliableLetters.copy()
    def __str__(self):
        if self.correctLetter == "":
            return "(" + str(self.nullLetters) + "," + str(self.avaliableLetters) + ")\n"
        else:
            return "(" + str(self.correctLetter) + ")\n"
class Word:
    def __init__(self,alphabet):
        self.word = []
        self.unsetLetters = []
        for _ in range(0,5):
            self.word.append(Positions([],"",alphabet))
    def __str__(self):
        print("[")
        for i in range(0,5):
            print(self.word[i])
        print("]")
        return ""


def updateWord(word, guess):
    if len(guess) == 5:
        guess = guess.lower()
        for i in range(5):
            if word.word[i].correctLetter == "":
                correctness = int(input("Is " + guess[i] + " correct? 1 for yes, 2 for in word, 3 for incorrect: "))
                if correctness == 1:
                    word.word[i].correctLetter = guess[i]
                    if guess[i] in word.unsetLetters:
                        word.unsetLetters.remove(guess[i])
                if correctness == 2:
                    word.word[i].nullLetters.append(guess[i])
                    word.word[i].avaliableLetters.remove(guess[i])
                    if guess[i] not in word.unsetLetters:
                        word.unsetLetters.append(guess[i])
                if correctness == 3:
                    for j in range(5):
                        if guess[i] not in word.word[j].nullLetters:
                            word.word[j].nullLetters.append(guess[i])
                        if guess[i] in word.word[j].avaliableLetters:
                            word.word[j].avaliableLetters.remove(guess[i])

def getUniqueWords():
    filtered_words = list(filter(lambda x: len(x) == 5, words.words()))
    filtered_words = list(filter(lambda x: x.isalpha(), filtered_words))
    filtered_words = list(map(lambda x: x.lower(), filtered_words))
    unique_words = set(filtered_words)
    unique_words = list(unique_words)
    return unique_words


def suggestWord(word, unique_words):
    if unique_words == []:
        unique_words = getUniqueWords()    
    valid_words = []
    for possible_word in unique_words:
        flag = True
        for char in word.unsetLetters:
            if char not in possible_word:
                flag = False
        for i in range(5):
            if word.word[i].correctLetter != "":
                if word.word[i].correctLetter != possible_word[i]:
                    flag = False
            else:
                if possible_word[i] in word.word[i].nullLetters:
                    flag = False
                if possible_word[i] not in word.word[i].avaliableLetters:
                    flag = False
        if flag:
            valid_words.append(possible_word)
    return valid_words
        
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
word = Word(alphabet)
updateWord(word,input("Enter a guess: "))
suggestions = suggestWord(word,[])
for _ in range(0,5):
    random.shuffle(suggestions)
    removeable = []
    for sugg in suggestions:
        print(sugg)
        x = int(input("Does this word work? 1 for yes, 2 for no, 0 for won game: "))
        if x == 1:
            updateWord(word,sugg)
            removeable.append(sugg)
            break
        if x == 2:
            removeable.append(sugg)
        if x == 0:
            exit()
    for remove in removeable:
        suggestions.remove(remove)
    suggestions = suggestWord(word,suggestions)