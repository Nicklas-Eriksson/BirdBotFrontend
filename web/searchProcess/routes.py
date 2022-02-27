from cgitb import reset
from flask_login import login_required
from web import utility
from web.utility import Edit
from flask import Blueprint, flash, render_template, request, redirect, url_for
from web.serverClient import client
from web.searchProcess.utility import TweetResult

searchBlueprint = Blueprint('searchBlueprint', __name__)
tweets = "Empty"
username = "Unknown"
token = None
result = None

@searchBlueprint.route('/search/<username>', methods=['GET', 'POST'])
@searchBlueprint.route('/<username>', methods=['GET', 'POST'])
@login_required
def search(username):
    if request.method == 'POST':
        if request.form.get('swapBtn') == 'swap':
            return redirect(url_for('signInBlueprint.logout'))        
        
        else:
            global dataTuple
            searchWord = request.form.get('searchWord')
            numberOfTweets = request.form.get('numberOfTweets')
            searchFrom = request.form.get('searchFrom')

            if searchWord:
                searchWord = Edit.RemoveWhitespaceSearch(searchWord)
                dataTuple = client.Scrape(searchWord, searchFrom, numberOfTweets)
                global result
                # result = "{searchWord} was analyzed with Natural Language Toolkit:\nInconclusive: {nr} results at {percent}%\nNeutral: {nr} results at {percent}%\nSligthly unhappy: {nr} results at {percent}%\nExtremely unhappy: {nr} results at {percent}%\nSligthly happy: {nr} results at {percent}%\nExtremely happy: {nr} results at {percent}%\nSearch was made from {searchFrom}\nWith a sample size of {numberOfTweets}"
                result = "\'"+searchWord+"\'" +" was analyzed with Natural Language Toolkit:\n"
                for post in dataTuple[0]:
                    result += post[1] +": "+str(post[0])+"%\n"
                
                result += "\nSearch was made from " +searchFrom+".\nSample size of "+ numberOfTweets+"."
                             
                return redirect(url_for('searchBlueprint.result'))

    else:
        return render_template('search.html', values=username)

@searchBlueprint.route('/result', methods=['GET', 'POST'])
@login_required
def result():
    if request.method == 'POST':        
        if request.form.get('tweetBtn') == 'tweet':
                res = TweetResult(result)
                if res == True:
                    flash('Tweet created!', category='success')
                else:
                    flash('Whoops! Something went wrong...', category='error')
        elif request.form.get('swapBtn') == 'swap':
            return redirect(url_for('searchBlueprint.search', username = username))
            
    return render_template('result.html', values=dataTuple)