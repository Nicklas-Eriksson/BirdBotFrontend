import imp
import socket
import pickle
from web.dataProcess.analyzeData import Analyze

# class client:
#     HEADERSIZE = 10 # Used for prepare that reciving system on the size of the file transfer.

#     def StartClient(searchWord, searchFrom, numberOfTweets):
#         s = socket.socket()
#         host = 'DESKTOP-17ML2OB'
#         port = 1234

#         print('Connecting to server...')
#         s.connect((host,port))
#         print('Server connection established!')
        
#         print("Compressing user inputs...")
#         inputTuple = (searchWord, searchFrom, numberOfTweets)
#         print("Compression done!")

#         print("Sending data...")
#         compressedMsg = pickle.dumps(inputTuple)
#         s.send(compressedMsg)
#         print("Data transmitted!")

#         print("Waiting for response...")
#         #10~ pages of text can be recived with this method. 20480 bytes // 20 KB.
#         msg = s.recv(20480)
#         print("Message recived!")

#         print("Decoding message...")
#         decodedCompressedMsg = pickle.loads(msg)
#         print("Message decoded!")

#         print("Terminating connection to server...")
#         s.close()
#         print("Connection terminated!")

#         out = Analyze.Mood(decodedCompressedMsg, inputTuple)
#         return out

class client:

    def StartClient(searchWord, searchFrom, numberOfTweets):
        HEADERSIZE = 10 # Used for prepare that reciving system on the size of the file transfer.
        s = socket.socket()
        host = 'DESKTOP-17ML2OB'
        port = 1234

        print('Connecting to server...')
        s.connect((host,port))
        print('Server connection established!')
        
        print("Compressing user inputs...")
        inputTuple = (searchWord, searchFrom, numberOfTweets)
        print("Compression done!")

        print("Sending data...")
        compressedMsg = pickle.dumps(inputTuple)
        s.send(compressedMsg)
        print("Data transmitted!")

        print("Waiting for response...")

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

                    out = Analyze.Mood(decodedCompressedMsg, inputTuple)
                    return out