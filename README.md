# Birdbot 2022
    A school project by Nicklas Eriksson


# Description:
This program is a website that analyzes the mood of Twitter.
The program analyzes the top or latest tweets of a given search word or phrase. 
The data is analyzed using a third party program (Natural Langue Toolkit) that 
scores the post on a scale from -1.00 to + 1.00 (negative to positive). The user 
makes a request to analyze a certain amount of tweets based on user input (word/phrase). 
The request is forwarded to another program responsible for gathering the 
data and delivering it back to the website. The user can also choose to post the result of 
the data analysis from the Twitter account of the bot.

▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ 

# Third party programs:

Frontend:
Website:
    The visualization is made in Python with the use of Flask which utilizes HTML and CSS.

    Flask link: https://flask.palletsprojects.com/en/2.0.x/ 

Backend:
Database: 
    Flask-SQLalchemy for storing user data.

    Flask-SQLalchemy link: https://flask-sqlalchemy.palletsprojects.com/en/2.x/

Data analysis:
    Natural language toolkit (NLTK) is a program that scores a text on a scale from -1.00 to
    + 1.00 (negative to positive).
    ____________________________________________________________________
    TextBlob is a library for processing textual data. It provides a consistent API for diving
    into common natural language processing (NLP) tasks such as part-of-speech tagging, non
    phrase extraction, sentiment analysis, and more. (From their own site)
    
    
    NLTK link: https://www.nltk.org/
    TextBlob link: https://textblob.readthedocs.io/en/dev/

Language translation:
    Google Translate API
    GT is used to translate tweets from other languages to English so that the NLTK
    (listed above), can score the results. Without the translation API these tweets were scored
    as inconclusive.

    Google Translate API link: https://cloud.google.com/translate

Password encrypting:
    Werkzeug
    Werkzeug is a third party program that allows for encrypting and decrypting strings with
    the use of salting (adding unique identifiers for safer hashing). This allows the
    database to store  encrypted passwords with increased security.

    Werkzeug link: https://werkzeug.palletsprojects.com/en/2.0.x/utils/

▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ 

# Functions: 
User sign in:
1. Register:
    The user is asked to enter: email address, first name, last name, username, password
    and to verify the password. The inputs are stripped of starting and trailing whitespaces.
    All inputs need to be filled in according to the requirements (below) for the submit
    button to accept the input. 

    Requirements: 
    1. Email address needs an @ symbol, needs to be at least 4 characters long and cannot
    already be registered with the site.
    2. Username cannot already be taken by another user.
    3. Password need to be at least 8 or more characters, consist of letters (a-z), contain
    at least one number (0-9) and one special character (@#$%^&+=).
    4. Passwords need to match to be valid.

    If all requirements are fulfilled a user will be created with the credentials given.
    The user password will be hashed and salted before stored in the SQL-database.
    
2. Login:
    The user is asked to enter: username and password.
    The inputs are stripped of starting and trailing whitespaces.
    An SQL-query is done against the username. If a match is found the password is checked
    against the stored hashed password using the check_password_hash function. If the user
    exists they are redirected to the search page. The user is thereafter stored in the session
    history as logged in via the 'remember me' cookie. If the web history contains the
    'remember me' cookie to the website will directly redirected the user to the search page.

3. Logout:
    If the user logs out the user is redirected to the login page.
    The 'remember me cookie' will also be cleaned up from the web browser.

4. Forgot password:
    If the user forgets the password to their account they can click the
    'forgot password?'-button. These are the steps for restoring the password:
    1. The user is asked to enter the email address connected with their account.
        If said account is registered in the SQL-database an email will be sent to it.
        The user is prompted with a success pop up on their screen for 1.5 seconds if the
        email is a match and will thereafter be redirected to insert their reset code sent
        to them via email.
    2. The reset password email will contain a 16 character code provided by the website.
        The code will be active for 5 minutes before it expires. 
    3. When entering the reset code:
        1. Input is trimmed of whitespaces.
        2. Code is validated against current reset code sent to the user.
        If the user-input and the reset code is a match, the user is prompted by a success
        message for 1.5 seconds before being redirected to where they can reset their password.
    4. The user is asked to enter a new password and to verify that password.
       If the passwords match, they are set as the user's new password and the SQL-database
       is updated.
______________________________________________________________________________________________

Search: 
1. The user is prompted to enter their search word/phrase.
2. The user picks how many tweets they want to scrape from a drop down menu.
3. The user picks if tweets should be scraped from latest or top results.
4. When the user presses the 'search' button a client connection to the Twitter scraper
bot is established. The search requested is compressed and sent via the socket stream to
the server where the scrape is executed. When all the data is collected it is sent back to
the client (website).
5. Data now gets decompressed and sent through the TextBlob software where the text is
simplified and words are transformed to their roots. Thereafter the data is given to the
NLTK-software where it scores the text from -1.00 to +1.00 (negative to positive).
6. If posts are in another language the NLTK will rate them as 0.00, which means they are
inconclusive. All inconclusive posts will go through the google translate API where they
will be translated (if possible) to English.
7. All translated posts will go through the NLTK software again for another scoring attempt. 
8. The results are sent to the result page for display.

Result:
The results are displayed on this page. The analyzed posts will be put into one of
six brackets:
Inconclusive, unhappy(NLTK score <= -0.25), slightly unhappy(NLTK score => -0.25 & < 0.00>),
neutral, slightly happy (NLTK score > 0.00 & < +0.25>), happy (NLTK score => +0.25)

Tweet result:
1. The user may use the bot to tweet the result of the data analysis by a clicking a button
on the result screen. 
3. The result is formatted to a string that fit inside Twitters 280-characters policy.
4. The formatted string is compressed using Pickle and sent as a data stream to the
awaiting server.
▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ 

# Utility Method descriptions:

Folder:
1. analyzeDataProcess:
Class Analyze:
Responsible for analyzing the data from the scraper. Analyzes the mood with NLTK, Textblob
and the google translate API.

Functions:
1. Mood:
    1. The content of the actual tweet is extracted, excluding username, retweets, likes etc.  
    2. The post is sent to the 'CleanUpPost'-function.
2. CleanUpPost:
    1. This function uses regex to replace unwanted words and/or symbols.
    For example: Hyperlink (replaced with 'link'), reply to @SomeUser (replaced with @User)
    2. The post is sent to the 'GradeMood'-function.
3. GradeMood:
    1. The post is converted into a TextBlob (see #Third party programs).
    2. The post is sent to the 'NLTK' and is given a score.
    3. The post is sent to the 'CalculatePercent'-function.
4. Inconclusive posts:
    If a post is deemed inconclusive, it is run through the Google translate API where
    it is translated to English if possible.
5. CalculatePercent:
    1. Based on the number of successful analyzed posts a percent number is given to the
    different brackets.

______________________________________________________________________________________________
mainProcess:
Class Edit:
    Responsible for fixing and validating user input during the sign in process.

Functions:
1. Login
    1. The user's username is queried against the database to see if the username is
    registered.
    2. If so, the user's password is verified against the database.
2. RemoveWhitespaceRegister
   1. The user's inputs are taken from the input fields.
   2. The strings are cleaned from white spaces.
3. RemoveWhitespaceLogin
   1. The user's inputs are taken from the input fields.
   2. The strings are cleaned from white spaces.
4. RemoveWhitespaceSearch
   1. The user's inputs are taken from the input fields.
   2. The strings are cleaned from white spaces.
5. ValidateEmail
   Checks if email is valid by checking if it contains necessary characters such as @.
   Match done with regex. (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
6. ValidatePassword
   Checks if the password match the criteria given (containing at least 8 characters,
   uppercase, lowercase, numbers and a special character).
   Match done with regex. (r'[A-Za-z0-9@#$%^&+=]{8,})
▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ 

# Route Method descriptions:
Sign in routes:

1. Register:
    1. Retrieves inputs from the user (email, first name, surname, username, password and
    repeat password).
    2. The retrieved input is stripped of whitespaces and validated with regex to see if
    email and passwords match the criteria given.
    3. The database is queried to see if the email is already registered or if the username
    is taken.
    4. The user's password is salted
    and hashed for increased security.
    5. The user is created and stored in the database.

    * If the user's credentials are not entered / do not match the given criteria / are
      taken an 'error'-popup will be displayed to the user indicating what has gone wrong.
      If a user is successfully created a 'success'-popup will be displayed.

    6. The user is redirected to the login screen.

2. login:
    1. Retrieves inputs from the user, username and password.
    2. Input is stripped of whitespaces.
    3. The database is queried to see if the username exists in the database.
    4. The password is de-hashed and cross referenced.

    * If the user's credentials are not entered / do not match the given criteria an
      'error'-popup will be displayed to the user indicating what has gone wrong.
      If a user's credentials match the one in the database, a 'success'-popup will
      be displayed instead.

    5. The user is redirected to the search page.
    6. The cookie 'remember me' is added to session history. When the user visits
    the website next time, they will remain logged in.

3. logout:
    1. Logs out the user.
    2. The user is redirected to the login page again.
    3. The cookie 'remember me' will be removed from session history.
______________________________________________________________________________________________

Forgot password, steps:

Initial steps:
1. The user presses the 'forgot password?' button.
2. The user is redirected to the reset password page.
3. The user enters the email address connected to their account.
4. The email address is validated using regex and trimmed of whitespaces.
5. The database is queried against the email address.
6. If the email is registered a email will be sent to the given address.
A 'success'-popup is displayed stating that the email has been sent to the given
address. If the address is not in the database an 'error' popup will be displayed. 
7. The user is redirected to the enter reset code page.

Email sent:
1. The user is sent a 16 character randomly generated code. The 16 character code is valid
 during a time span of 5 minutes. After the time is up the code will be invalidated. 
2. The user's code is checked against the active code the user gets to change their password.
If the code is correct a 'success'-popup will be displayed.
If the code is invalid an 'error'-popup will be displayed.
3. The user is redirected to reset password page

Reset password:
1. The user is asked for a new password and to verify it.
2. The input is checked against the given criteria and checked against each other for a match.
3. If the input is successful the user's new password will be salted and hashed before stored
in the SQL-database.

* A 'success'-popup will now be displayed. If credentials did not match or if the passwords
  is not valid an 'error'-popup will be displayed. The user is now redirected to the
  login page.
______________________________________________________________________________________________

Search steps:
Search:
1. The function takes the inputs from the user and removes leading and trailing withes spaces.
All inputs are sent to the 'StartClient' function.

2. StartClient:
    1. A connection to the scraper server is created.
    2. The user's input are put into a tuple and compressed using Pickle's 'dumps'-function
    (creates a serialized representation of a python object).
    3. The compressed inputs are sent to the server that is listening for a connection. When
    the data is sent the client waits for a response from the server containing the collected
    tweets as compressed data. 
    4. The compressed message that is recieved from the server is decompressed. The massage
    recieved is transmitted using a data stream where first a message is transmitted
    containing the length of the incomming message. The packages transmitted will arrive in
    chunks of 32 bytes. 
    5. Once the full message is recieved the connection between the server and the client
    is terminated. 
    6. The server goes back to listening for other connections. The client's socket
    (the website) is closed.
    7. The message is sent as a tuple to the 'Analyze.Mood'-class and function where the
    data analysis is executed.
    8. The returned value of the data-analyzes is sent back to the search class.

______________________________________________________________________________________________

Results:
1. The results in the result screen are calculated by the 'CalculateMood'-function.
2. The results are displayed in percentages according to how they scored in mood.   

Tweet it:
1. If the user presses the 'Tweet it!' button the result of the page will be formatted into
a string matching Twitters 280-characters policy.
2. The post gets compressed using Pickle.
3. The compressed message is sent to the server using the socket data stream.
4. If the bot manages to create a post the server will send back a verification message.

▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ ▄ 

# Python Lib:

Reset password email:
    SMTP protocol client (Simple Mail Transfer Protocol)
    SMTP is used for sending emails to users.

    SMTP link: https://docs.python.org/3/library/smtplib.html

Server:
    Socket and Pickle
    A socket server is initialized by the Twitter scraper and runs while the
    website runs. The website then establishes a client connection to the server for
    making requests and receiving requested data.
    ____________________________________________________________________
    Pickle is used for compressing, serializing and de-serializing the data object before
    sending the data to the server and/or client.

    Socket link: https://docs.python.org/3/library/socket.html
    Pickle link: https://docs.python.org/3/library/pickle.html
    
Regex:
    Regex is a python module which provides regular expression matching.

    Regex link: https://docs.python.org/3/library/re.html
