from distutils.log import error
import random
from PIL import ImageGrab
import pyautogui
import time
from pynput.keyboard import Key, Controller

#FOR NYT DARK MODE WORDLE
INVALID = (58, 58, 60)
VALID = (83, 141, 78)
INWORD = (181, 159, 59)

class MousePos():
    def __init__(self,x,y,bbox):
        self.x = x
        self.y = y
        self.bbox = bbox

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

def updateWord(word, guess,cor):
    guess = guess.lower()
    for i in range(5):
        if word.word[i].correctLetter == "":
            correctness = cor[i]
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
    f = open("words.txt", "r")
    unique_words = []
    for x in f:
        unique_words.append(x.strip())
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

def setMousePos():
    mousePos = pyautogui.position()
    x = mousePos[0]
    y = mousePos[1]
    return MousePos(x,y,(x,y,x+330,y+400))

def initMouse():
    input("Once you press enter you will have 5 seconds to align the mouse with the top left of the play aera to set the bounding box")
    time.sleep(5)
    mp = setMousePos()
    return mp

def evalRow(mp, row):
    im =  ImageGrab.grab(bbox=mp.bbox)
    width, height = im.size
    cropH = int(height/6)
    upperBound = cropH * row
    lowerBound = upperBound + cropH
    a = im.crop((0, upperBound, width, lowerBound))
    width, height = a.size
    cropW = int(width/5)
    correctness = []
    for i in range(5):
        leftBound = cropW * i
        rightBound = leftBound + cropW
        b = a.crop((leftBound,0,rightBound,height))
        letterWidth, letterHeight = b.size
        evalX = int(letterWidth/2 + letterWidth/4)
        evalY = int(letterHeight/2 + letterHeight/4)
        b = b.convert('RGB')
        rgb = b.getpixel((evalX, evalY))
        if rgb == VALID:
            correctness.append(1)
        elif rgb == INWORD:
            correctness.append(2)
        elif rgb == INVALID:
            correctness.append(3)
        else:
            error("INVALID RGB VALUE IN ROW " + str(row) + " LETTER " + str(i))
    return correctness

def type(keyboard,word):
    for char in word:
        keyboard.press(char)
        keyboard.release(char)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

# set up variables and get the bbox pos
alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
keyboard = Controller()
starters = ['slice','tried','crane','reach','bakes','roast','adieu']
random.shuffle(starters)
word = Word(alphabet)
mp = initMouse()

#make init guess
input("Once you press enter you will have 3 seconds to select the game window before the bot plays")
time.sleep(3)
type(keyboard,starters[0])
time.sleep(2.5)
cor = evalRow(mp,0)
updateWord(word,starters[0],cor)
suggestions = suggestWord(word,[])

for i in range(1,6):
    random.shuffle(suggestions)
    type(keyboard,suggestions[0])
    time.sleep(3)
    cor = evalRow(mp,i)
    if (all(x == 1 for x in cor)):
        exit()
    updateWord(word,suggestions[0],cor)
    suggestions = suggestWord(word,suggestions)