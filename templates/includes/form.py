from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateUserFeedback   # Input the objects from Forms.py
import shelve, User, Forms


app = Flask(Forms)


# '/' indicates the root directory of the website

@app.route('/')
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

@app.route('/', methods=['GET', 'POST'])
def register():
    form = Forms.CreateUserFeedback(request.form)
    if request.method == 'POST' and form.validate():
        d = shelve.open('database.db.sql')
        d['name'] = form.name.data
        d['country'] = form.country.data
        d['feedback'] = form.feedback.data
        d['diet'] = form.diet.data
        d[str(d['name'])] = basecode.User(form.name.data, form.age.data, form.gender.data, form.height.data, form.weight.data, form.diet.data)
        d['list1'] = d[str(d['name'])].set_list1([])
        d.close()
        flash('Thanks for registering')
        return redirect(url_for('default'))
    return render_template('flaskform.html', form=form, login=login)


# Means only if you run Main.py then the page will run (app.run())
if name == 'main':
    app.run()
