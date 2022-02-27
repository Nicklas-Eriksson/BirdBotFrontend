from web.__init__ import start

''' START PROGRAM FROM MAIN'''
app = start()

if __name__ == "__main__":
    app.run(debug=True)