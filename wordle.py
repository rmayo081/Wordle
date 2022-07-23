#!/usr/bin/env python3
import FileIO as io #import the FileIO.py module
import lexicon as lex #import lexicon.py module
import sys

#Main file of this program. Handles user input and the command line UI


# check if a target word {word} contains a character {ch}
# the lists checkgreen and checkyel are markers of if the user has already guessed a character
def containsChar(ch, word, checkgreen, checkyel): 
    for i in range(0, len(word) - 1):
        if ch == word[i]:
            if not checkgreen[i] and not checkyel[i]:
                checkyel[i] = True
                return True
    return False
# change terminal text color to green with ANSI characters
def toGreen():
    print('\u001b[32m', end='')
# change terminal text color to yellow with ANSI characters    
def toYellow():
    print('\u001b[33m', end='')
# change terminal text color to the default with ANSI characters
def reset():
    print('\u001b[0m',end='')

words = [] #list of words
wordCount = 0 #number of words in the list

if len(sys.argv) == 1:
    words, target = io.readFile()
else:
    sys.argv.pop(0)
    #populate the words list with the lists in the command line args
    for arg in sys.argv:
        words, target = io.readFile(arg)

#print('word is {}'.format(target))

guesses = 0;

flag = True #bool flag to mark when to stop the loop
cmd = '' #string for the user command

while flag: #program loop
    cmd = input() #take user input
    
    if cmd == 'quit': #user quit the program
        flag = False
        
    elif len(cmd) != 5 or not io.inList(words, cmd): #the guess wasn't long enough or wasn't in the dictionary
        print('invalid guess')
        
    elif cmd == target: #user gets the word right
        print('correct guess, got it in {}'.format(guesses + 1))
        # lex.updateScores(guesses + 1)
        lex.updateMongo(guesses + 1)
        flag = False
        
    else: #guess wasn't right, so we'll check the letters
        guesses += 1
        green = [False] * 5 #boolean list of markers to keep track of what letters were guessed right in the right position
        yel = [False] * 5 #boolean list of markers to keep track of what letters were guessed right, but wrong position
        currentColor = 0; #marker for current terminal color, 0 is default, 1 is yellow, 2 is green
        
        for i in range(0, 5): #check for correct letters in correct positions, print them in green
            if target[i] == cmd[i]:
                green[i] = True
                if currentColor != 2:
                    currentColor = 2;
                    #color to green
                    toGreen()
                print(cmd[i], end='')
                
                
            elif containsChar(cmd[i], target, green, yel): #check if a letter is in the target word, color it yellow if it wasn't already guessed
                if currentColor != 1:
                    currentColor = 1
                    #color to yellow
                    toYellow()
                print(cmd[i], end='')
                
            else: #a letter was wrong, so print it in the default color
                if currentColor != 0: 
                    currentColor = 0
                    #change to default
                    reset()
                print(cmd[i], end='')
                
        else: #print a newline character and make the terminal color default
            print('\n', end='')
            if currentColor != 0:
                    currentColor = 0
                    #change to default
                    reset()
        
lex.printHistory(guesses + 1)