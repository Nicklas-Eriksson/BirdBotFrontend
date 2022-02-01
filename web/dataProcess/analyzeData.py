from dataclasses import replace
from glob import glob
import regex as re
from textblob import TextBlob
from googletrans import Translator

inconclusiveResults = []
inconclusive = 0
neutral = 0
slightlyUnhappy = 0
extremelyUnhappy = 0
slightlyHappy = 0
extremelyHappy = 0
totalNumber = 0

class Analyze:
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

        for post in data:
            userId = post[0]
            username = post[1]
            handle = post[2]
            date = post[3]
            tweet = post[4]
            commentCountid = post[5]
            retweetCount = post[6]
            likes = post[7]
                        
            if tweet:              
                a.GradeMood(a.CleanUpPost(tweet))
        
        # if len(inconclusiveResults) > 0:
        #     t = Translator()            
        #     global inconclusive
        #     inconclusive = 0 #Reset the inconclusive counter

        #     for post in inconclusiveResults:
        #         print("Old post:" + post)
        #         out = t.translate(post, dest='en')
        #         print(out)
        #         a.GradeMood(out)

        return a.CalculatePercent(inputTuple)       

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

            percents = [(100*(inconclusive)/(totalNumber), "Inconclusive", inconclusive)]
            percents += [(100*(neutral)/(totalNumber), "Neutral", neutral)]
            percents += [(100*(slightlyUnhappy)/(totalNumber), "Sligthly unhappy", slightlyUnhappy)]
            percents += [(100*(extremelyUnhappy)/(totalNumber), "Extremely unhappy", extremelyUnhappy)]
            percents += [(100*(slightlyHappy)/(totalNumber), "Sligthly happy", slightlyHappy)]
            percents += [(100*(extremelyHappy)/(totalNumber), "Extremely happy", extremelyHappy)]   

            return (percents, inputTuple, totalNumber)

        except Exception as e:
            print(e)

            return None