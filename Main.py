from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# '/<accName>' is used when the directory has a name
# '/' indicates the root directory of the website
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/shoppingcart')
def shoppingcart():
    return render_template('shoppingcart.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/login')
def shop():
    return render_template('login.html')


# Means only if you run Main.py then the page will run (app.run())
if __name__ == '__main__':
    app.run()













