def TweetResult(result):
    from web.serverClient import client    
    resTuple = ('BirdBot2022', result)
    res = client.Tweet(resTuple)
    
    return res