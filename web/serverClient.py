import socket
import pickle
from web.analyzeDataProcess.analyzeData import Analyze
from dotenv import load_dotenv
import os

HEADERSIZE = 10 # Used for prepare that reciving system on the size of the file transfer.

#Client for connecting to the scraper bot's server.
class client:
    def Scrape(searchWord, searchFrom, numberOfTweets):
        socket = client.StartClient()
        return client.SendScrapeData(socket, searchWord, searchFrom, numberOfTweets)
        
    def Tweet(result):
        socket = client.StartClient()
        msg = client.SendTweetData(socket, result)
        if msg:
            return True
        else:
            return False

    #Boots up the client.
    def StartClient():        
        s = socket.socket()
        load_dotenv()
        ServerPort = int(os.getenv("ServerPort"))
        ServerHost = os.getenv("ServerHost")

        print('Connecting to server...')
        s.connect((ServerHost, ServerPort))
        print('Server connection established!')
        
        return s
    
    #Sends information about what to scrape to the server.
    def SendScrapeData(s, searchWord, searchFrom, numberOfTweets):
        print("Compressing user inputs...")
        inputTuple = (searchWord, searchFrom, numberOfTweets)
        compressedMsg = pickle.dumps(inputTuple)
        print("Compression done!")

        print("Sending data...")
        s.send(compressedMsg)
        print("Data transmitted!")

        print("Waiting for response...")

        decodedCompressedMsg = client.GetFullMessage(s)
        
        return Analyze.Mood(decodedCompressedMsg, inputTuple)

    def SendTweetData(s, result):
        print("Compressing user inputs...")        
        compressedMsg = pickle.dumps(result)
        print("Compression done!")

        print("Sending data...")
        s.send(compressedMsg)
        print("Data transmitted!")

        print("Waiting for response...")

        return client.GetFullMessage(s)
        
    def GetFullMessage(s):
        while True:
            fullMsg = b''
            newMsg = True
            while True:
                        msg = s.recv(32)
                        if newMsg:
                            msgLen = int(msg[:HEADERSIZE])
                            newMsg = False
                        
                        fullMsg += msg

                        # Full message has been transmitted fully.
                        if len(fullMsg) - HEADERSIZE == msgLen:
                            print("Message recived!")
                            newMsg = True

                            print("Decoding message...")
                            decodedCompressedMsg = pickle.loads(fullMsg[HEADERSIZE:])
                            print("Message decoded!")
                            
                            fullMsg = b''

                            print("Terminating connection to server...")
                            s.close()
                            print("Connection terminated!")

                            return decodedCompressedMsg