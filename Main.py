from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserFeedback   # Input the objects from Forms.py
import shelve, User


app = Flask(__name__)


# '/' indicates the root directory of the website
@app.route('/', methods=['GET', 'POST'])
def clothesInfo():
    return render_template('clothesInfo.html', discount = False)


@app.route('/clothesInfo')
def home():
    return render_template('home.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/transaction')
def transaction():
    return render_template('transaction.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/login')
def login():
    return render_template('login.html')


# Means only if you run Main.py then the page will run (app.run())
if __name__ == '__main__':
    app.run()













