import regex as re
import random
import string
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import os
from dotenv import load_dotenv

load_dotenv()
SecretKey = os.getenv("SecretKey")

class Edit:
    def Login(username, password):
        username = "".join(username.split())
        password = "".join(password.split())
            
        return (username, password)

    def RemoveWhitespaceRegister(email, firstName, surname, username, password, rePassword):
        email = "".join(email.split())
        firstName = "".join(firstName.split())
        surname = "".join(surname.split())
        username = "".join(username.split())
        password = "".join(password.split())
        rePassword = "".join(rePassword.split())

        return (email, firstName, surname, username, password, rePassword)

    def RemoveWhitespaceLogin(username, password):
        username = "".join(username.split())
        password = "".join(password.split())

        return (username, password)

    def RemoveWhitespaceSearch(searchWord):
        searchWord = searchWord.strip()

        return (searchWord)

    def ValidateEmail(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def ValidatePassword(password):
        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return True
        else:
            return False

class GenerateOrg:
    def GetResetCode():
        code = ""
        i = 0
        
        while i < 8:
            tempInt = random.randint(0, 9)
            tempChar = random.choice(string.ascii_letters)
            code += str(str(tempInt) + tempChar)
            i += 1
        
        return code

class Generate:
    def GenCode():
        code = ""
        i = 0
        
        while i < 8:
            tempInt = random.randint(0, 9)
            tempChar = random.choice(string.ascii_letters)
            code += str(str(tempInt) + tempChar)
            i += 1
        
        return code

    def GetToken():
        s = serializer(SecretKey, 300)#5min
        c = Generate.GenCode()
        return (s.dumps({c: 1}).decode('utf-8'), c, s)