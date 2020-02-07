from flask import Flask, render_template, request, redirect, url_for, flash, session
from Forms import CreateUserForm, LoginForm
import shelve, User
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/contactUs")
def contactUs():
    return render_template("contactUs.html")


@app.route("/login2", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if form.username.data=='staff':
                if form.password.data=='staff890':
                    return redirect(url_for('retrieveUsers'))
    return render_template("login2.html",form=form)

def checkUserExists(name):
    db = shelve.open('storage.db', 'r')
    try:
        usersDict = db['Users']
        for key in usersDict:
            user = usersDict[key]
            if user.get_username()==name:
                return True
    except:
        print("Error in retrieving Users from storage.db.")
    return False


@app.route('/useraccount', methods=['GET','POST'])
def useraccount():
    form = LoginForm(request.form)
    correct = False
    errorResponse=''
    if request.method == 'POST':
        errorResponse='User does not exist'
        if form.validate():
            correct = False
            usersDict = {}
            db = shelve.open('storage.db', 'r')
            try:
                usersDict = db['Users']
                for key in usersDict:
                    user = usersDict[key]
                    if user.get_username()==form.username.data:
                        correct = user.get_password()==form.password.data;
                        if not correct:
                            errorResponse='Invalid password'
            except:
                print("Error in retrieving Users from storage.db.")
            if correct:
                return render_template("Retrieveaccount.html",name=form.username.data)
    return render_template("useraccount.html",form=form,errorResponse=errorResponse)


@app.route("/Retrieveaccount")
def Retrieveaccount():
    return render_template("Retrieveaccount.html")


@app.route("/logout")
def logout():
    return render_template("home.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route('/createUser', methods=['GET', 'POST'])
def createUser():
    createUserForm = CreateUserForm(request.form)
    username = createUserForm.username.data
    password = createUserForm.password.data
    domain = username
    if request.method == 'POST' and createUserForm.validate():
        usersDict = {}
        db = shelve.open('storage.db', 'c')
        try:
            usersDict = db['Users']
            User.User.countID = db['usercount']
        except:
            print("Error in retrieving Users from storage.db.")
        if checkUserExists(createUserForm.username.data):
            return render_template('createUser.html', form=createUserForm,error='User name exists')
        else:
            user = User.User(createUserForm.firstName.data, createUserForm.lastName.data, createUserForm.username.data,createUserForm.password.data,createUserForm.gender.data)
            usersDict[user.get_userID()] = user
            db['Users'] = usersDict
            # Test codes
            usersDict = db['Users']
            user = usersDict[user.get_userID()]
            print(user.get_firstName(), user.get_lastName(), "was stored in shelve successfully with userID =",
                  user.get_username())
            db.close()
        return redirect(url_for('home'))
    return render_template('createUser.html', form=createUserForm,error='')


@app.route('/retrieveUsers')
def retrieveUsers():
 usersDict = {}
 db = shelve.open('storage.db', 'r')
 usersDict = db['Users']
 db.close()


 usersList = []
 for key in usersDict:
  user = usersDict.get(key)
  usersList.append(user)

 return render_template('retrieveUsers.html', usersList=usersList, count=len(usersList))


@app.route('/updateUser/<id>/', methods=['GET', 'POST'])
def updateUser(id):
    updateUserForm = CreateUserForm(request.form)
    if request.method == 'POST' and updateUserForm.validate():
        userDict = {}
        db = shelve.open('storage.db', 'w')
        userDict = db['Users']

        user = userDict.get(id)
        user.set_firstName(updateUserForm.firstName.data)
        user.set_lastName(updateUserForm.lastName.data)
        user.set_username(updateUserForm.username.data)
        user.set_password(updateUserForm.password.data)
        user.set_gender(updateUserForm.gender.data)

        db['Users'] = userDict
        db.close()
        return redirect(url_for('retrieveUsers'))
    else:
        userDict = {}
        db = shelve.open('storage.db', 'r')
        userDict = db['Users']
        db.close()
        user = userDict.get(id)
        updateUserForm.firstName.data = user.get_firstName()
        updateUserForm.lastName.data = user.get_lastName()
        updateUserForm.username.data = user.get_username()
        updateUserForm.gender.data = user.get_gender()
        return render_template('updateUser.html',form=updateUserForm)


@app.route('/deleteUser/<int:id>/', methods=['POST'])
def deleteUser(id):
    # retrieve all user data
    userDict = {}
    db = shelve.open('storage.db', 'w')
    userDict = db['Users']

    userDict.pop(id)  # action of removing the record
    db['Users'] = userDict  # put back to persistence
    db.close()

    # after we delete successful
    return redirect(url_for('retrieveUsers'))


if __name__ == "__main__":
    app.run()
