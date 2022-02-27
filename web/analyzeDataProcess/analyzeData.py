from dataclasses import replace
from glob import glob
import regex as re
from textblob import TextBlob
from googletrans import Translator
import math

inconclusiveResults = []
inconclusive = 0
neutral = 0
slightlyUnhappy = 0
extremelyUnhappy = 0
slightlyHappy = 0
extremelyHappy = 0
totalNumber = 0

class Analyze:
    #Analyzes the mood of the tweets with Natural language toolkit (NLTK)
    def Mood(data, inputTuple):
        a = Analyze()
        global inconclusive
        global neutral
        global slightlyUnhappy
        global extremelyUnhappy
        global slightlyHappy
        global extremelyHappy
        global totalNumber
        inconclusiveResults = []
        inconclusive = 0
        neutral = 0
        slightlyUnhappy = 0
        extremelyUnhappy = 0
        slightlyHappy = 0
        extremelyHappy = 0
        totalNumber = 0

        print("Input Tuple len: " + str(len(inputTuple)))
        tempIndex = 1
        for post in data:
            # userId = post[0]
            # username = post[1]
            # handle = post[2]
            # date = post[3]
            print("Post " + str(tempIndex) + ": ")
            print(post)
            try:
                tweet = post[4]
                print("try block done")
            except:
                print("except block done")
                tweet = '.'
            print(str(tempIndex))
            tempIndex += 1
            # commentCountid = post[5]
            # retweetCount = post[6]
            # likes = post[7]
                        
            if tweet:              
                a.GradeMood(a.CleanUpPost(tweet))

        #GOOGLE TRANSLATE API.
        #Turn off if it exceeds api limit
        if len(inconclusiveResults) > 0:
            t = Translator()            
            inconclusive = 0 #Reset the inconclusive counter

            for post in inconclusiveResults:
                print("Old post:" + post)
                out = t.translate(post, dest='en')
                print(out)
                a.GradeMood(out)
        #Turn off if it exceeds api limit

        return a.CalculatePercent(inputTuple)       

    #Grades the mood from into 6 different categories.
    # Inconclusive, neutral, slightly unhappy/happy, extremely unhappy/happy.
    def GradeMood(a, tweet):   
        try:
            blob = TextBlob(tweet)
            sentiment = blob.sentiment.polarity
            try:
                if sentiment == 0.00:
                    global inconclusive
                    inconclusive += 1
                    global inconclusiveResults
                    inconclusiveResults += [tweet]                    
                elif sentiment > -0.25 and sentiment < 0.25:
                    global neutral
                    neutral += 1
                elif sentiment < -0.00:
                    global slightlyUnhappy
                    slightlyUnhappy += 1
                elif sentiment < -0.25:
                    global extremelyUnhappy
                    extremelyUnhappy += 1
                elif sentiment > 0.00:
                    global slightlyHappy
                    slightlyHappy += 1
                elif sentiment > 0.25:
                    global extremelyHappy
                    extremelyHappy += 1
            except:
                print("Fail @: NLTK analysis")
        except:
            print("Fail @: sentiment analysis")
    
    #Cleans up the tweet
    def CleanUpPost(a, tweet):
        try:
            tweet = re.sub(r'"', '', tweet)
            tweet = re.sub(r'\n', '', tweet)
            tweet = re.sub(r'\t', '', tweet)
            tweet = re.sub(r'@\S+', '@User', tweet)
            tweet = re.sub(r'http\S+', 'link:_', tweet)
            tweet = re.sub(r'Läs in bild', '', tweet)
            tweet = re.sub(r'Svarar', '', tweet)
            tweet = re.sub(r'tn', '', tweet)
            tweet = re.sub(r'KB', '', tweet)
            tweet = re.sub(r'\b\d+\b', '', tweet)            
        except:
            print("Fail @: regex sentiment clean up")

        return tweet

    #Calculates the mood percent for the result display. 
    def CalculatePercent(a, inputTuple):
        try:
            global inconclusive
            global neutral
            global slightlyUnhappy
            global extremelyUnhappy
            global slightlyHappy
            global extremelyHappy
            global totalNumber
            totalNumber =  inconclusive + neutral + slightlyUnhappy + extremelyUnhappy + slightlyHappy + extremelyHappy

            percents = [(math.floor(100*(inconclusive)/(totalNumber)*10)/10, "Inconclusive", inconclusive)]
            percents += [(math.floor(100*(neutral)/(totalNumber)*10)/10, "Neutral", neutral)]
            percents += [(math.floor(100*(slightlyUnhappy)/(totalNumber)*10)/10, "Slightly unhappy", slightlyUnhappy)]
            percents += [(math.floor(100*(extremelyUnhappy)/(totalNumber)*10)/10, "Extremely unhappy", extremelyUnhappy)]
            percents += [(math.floor(100*(slightlyHappy)/(totalNumber)*10)/10, "Slightly happy", slightlyHappy)]
            percents += [(math.floor(100*(extremelyHappy)/(totalNumber*10)/10), "Extremely happy", extremelyHappy)]

            return (percents, inputTuple, totalNumber)

        except Exception as e:
            print(e)

            return None