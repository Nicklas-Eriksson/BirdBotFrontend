from web import start
from flask import Flask, render_template

app = start()

if __name__ == "__main__":
    app.run(debug=True)