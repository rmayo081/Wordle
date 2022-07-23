#!/usr/bin/env python3
import os
import pymongo
import hashlib
#Library developed to handle Databse IO and word dictionary

connect = pymongo.MongoClient("mongodb://localhost:27017/")
db = connect['PyWordle']
history = db['history']
userDB = db['users']

userAttempt : dict = None #my attempt to speed up queries by storing the result after the first attempt to login

loggedIn = False

def updateScores(add: int):
    set = [0] * 10
    
    try:
        with open('scores.txt', 'r') as file:
            lines = file.readlines()
        i = 0
        for line in lines:
            score = int(line.split()[2])
            set[i] = score
            i += 1
            
            
    except:
        pass #do nothing
    finally:
        if add >= 10:
            set[9] += 1
        else:
            set[add - 1] += 1
        file = open('scores.txt', 'w')
        file.write('1 : {}\n'.format(set[0]))
        file.write('2 : {}\n'.format(set[1]))
        file.write('3 : {}\n'.format(set[2]))
        file.write('4 : {}\n'.format(set[3]))
        file.write('5 : {}\n'.format(set[4]))
        file.write('6 : {}\n'.format(set[5]))
        file.write('7 : {}\n'.format(set[6]))
        file.write('8 : {}\n'.format(set[7]))
        file.write('9 : {}\n'.format(set[8]))
        file.write('10+ : {}\n'.format(set[9]))
        file.close()


def updateMongo(add: int):
    
    
    if add >= 10:
        query = {'_id': 10}
    else:
        query = {'_id': add}
        
    score = history.find_one(query)['score']
    score += 1
    
    history.update_one(query, {'$set': {'score' : score}})
    
#print the score history from MongoDB and highlight the user's score in green   
def printHistory(g: int):
    i = 0
    if g >= 10:
        g = 10
    hist = history.find({}, {'_id' : 0})
    set = False
    print('Trys   |   Score')
    for sc in hist:
        i += 1
        
        if g == i:
            print('\u001b[32m', end='')
            set = True
        
        if i == 10:
            print('10+    :   {}'.format(i, sc['score']))
        else:
            print('{}      :   {}'.format(i, sc['score']))
            
        if set:
            print('\u001b[0m',end='')
            set = False
            

def login(user: str, password: str) -> bool:
   
    result = userDB.find_one({'username' : user})
    if result is None:
        return False
    keyToCheck = result['password'][32:]
    salt = result['password'][:32]


    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    if key == keyToCheck:
        loggedIn = True
        return True
    return False

def sign_up(user: str, password: str) -> bool:
    result = userDB.find_one({'username' : user})
    if result is not None:
        return False
    
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    saltedKey = salt + key
    userDB.insert_one({'username': user, 'password': saltedKey})
    loggedIn = True
    return True
    
def isLoggedIn() -> bool:
    return loggedIn