from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()
SecretKey = os.getenv("SecretKey")

#Generates a 16 character reset code.
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

    #Generates a reset token that lives for 5 minutes.
    def GetToken():
        s = serializer(SecretKey, 300)#5min
        c = Generate.GenCode()
        return (s.dumps({c: 1}).decode('utf-8'), c, s)