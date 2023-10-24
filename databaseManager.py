import settings

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
            return (_funds.strip('\n'))