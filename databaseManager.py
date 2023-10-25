import settings
import random

fPath = '.\db\gambling.mydb'



# Check if user ID is already in database returning True or False
def CheckIsUserInDB(ID):
    with open(fPath, 'r') as fR:
        for line in fR:
            if str(ID) in line:
                return True
    CreateUserInDB(ID)
    return False
    
def CreateUserInDB(ID):
    with open(fPath, 'a') as fA:
        fA.write(f'{ID}:{settings.GetDefaultBankFunds()}\n')

def GetUserFunds(ID):
    with open(fPath, 'r') as fR:
        for line in fR:
            _id, _funds = line.split(':')
            return int(_funds.strip('\n'))

def SetUserFunds(ID, amount):
    return None


def StartRoulette(amount, choice):
    percent = random.randrange(0, 100)
    spin = ''

    if percent <= 45:
        spin = 'red'
    if percent <= 90:
        spin = 'black'
    if percent > 90:
        spin = 'white'

    if choice == spin:
        if choice == 'red':
            return f'{spin}:{int(amount) * 2}'
        elif choice == 'black':
            return f'{spin}:{int(amount) * 2}'
        elif choice == 'white':
            return f'{spin}:{int(amount) * 14}'
    else:
        return f'{spin}:{0}'
        