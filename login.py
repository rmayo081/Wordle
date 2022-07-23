import lexicon as l
# WIP component for logging/signing up and storing user scoring data
user : str = None
while not l.isLoggedIn():
    print('log in, sign up, or quit')
    inpt = input()
    if inpt.lower() == 'log in':
        print('username?')
        user = input()
        print('password?')
        pswd = input()
        if not l.login(user, pswd):
            print('invalid username or password')
    
    elif inpt.lower() == 'sign up':
        print('new username?')
        user = input()
        print('new password?')
        pswd = input()
        l.sign_up(user, pswd)
    elif inpt.lower() == 'quit':
        print('ok')
        break
    else:
        print('invalid input')
        
        
    