from random import seed, randint
from time import time

# Module to handle file IO

def readFile(filename: str = 'sgb-words.txt'):    
    
    cnt = 0
    
    with open(filename,'r') as file:
        lines = file.readlines()
    cnt = (len(lines) * 2) + 1
    
    #select a random index
    seed(time()); 

    index = randint(0, len(lines) - 1)
    
    selection = (lines[0].split())[0]
    
    i = 0
    words = [[] for _ in range(cnt)]
    for line in lines:

        for word in line.split():
            if i == index:
               selection = word
            
                
            i += 1
            idx = hash(word) % cnt
            
            
            if len(words[idx]) != 0:
                # print('occupied bucket found: size is {} at index {}'.format(len(words[idx]), idx))
                for x in words[idx]:
                    # print(x)
                    if word == x:
                        print('duplicate word detected')
                        exit(1)
            words[idx].append(word)        
            

    return (words, selection)

def inList(words : list, curr : str):
    idx = hash(curr) % len(words)
    if len(words[idx]) == 0:
        return False
    for w in words[idx]:
        if w == curr:
            return True
    return False

#function pulled from the following stack overflow post: https://stackoverflow.com/questions/15285534/isprime-function-for-python-language
#Used to determine the proper size of the hashtable to minimize collisions
def is_prime(n: int) -> bool:
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  # since all primes > 3 are of the form 6n ± 1
  # start with f=5 (which is prime)
  # and test f, f+2 for being prime
  # then loop by 6. 
  f = 5
  while f <= r:
    print('\t',f)
    if n % f == 0: return False
    if n % (f+2) == 0: return False
    f += 6
  return True    
