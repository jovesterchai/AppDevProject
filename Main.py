from flask import Flask, render_template, request, redirect, url_for, flash
from Forms import CreateFeedback, CreateProduct, R, CreateUserForm, LoginForm   # Input the objects from Forms.py

from Product import Product
import Transaction
import invoice
import shelve, User, Product
import paypalrestsdk as paypal
from paypalrestsdk import *
import Feedback
from werkzeug.utils import secure_filename
import string
import random
import os


UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login2", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    errorResponse=''
    if request.method == 'POST':
        errorResponse='Invalid Credentials'
        correct = False
        if form.validate():
            if form.username.data=='staff':
                if form.password.data=='staff890':
                    return redirect(url_for('retrieveUsers'))
    return render_template("login2.html",form=form,errorResponse=errorResponse)

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
            id = 0
            usersDict = {}
            db = shelve.open('storage.db', 'r')
            try:
                usersDict = db['Users']
                for key in usersDict:
                    user = usersDict[key]
                    if user.get_username()==form.username.data:
                        id = user.get_userID()
                        correct = user.get_password()==form.password.data;
                        if not correct:
                            errorResponse='Invalid password'
            except:
                print("Error in retrieving Users from storage.db.")
            if correct:
                return render_template("Retrieveaccount.html",name=form.username.data,id=id)
    return render_template("useraccount.html",form=form,errorResponse=errorResponse)


@app.route("/Retrieveaccount")
def Retrieveaccount():
    return render_template("Retrieveaccount.html")


@app.route("/logout")
def logout():
    return render_template("home.html")


@app.route("/aboutus")
def aboutus():
    return render_template("us.html")

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
            user = User.User(createUserForm.firstName.data, createUserForm.lastName.data, createUserForm.username.data,createUserForm.password.data,createUserForm.gender.data,createUserForm.country.data,createUserForm.address.data,createUserForm.number.data)
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


@app.route('/updateUser', methods=['GET', 'POST'])
def updateUser():
    id = request.args.get('id', default = 1, type = int)
    updateUserForm = CreateUserForm(request.form)

    if request.method == 'POST' and updateUserForm.validate():
        userDict = {}
        db = shelve.open('storage.db', 'w')
        userDict = db['Users']

        user = userDict[id]
        user.set_firstName(updateUserForm.firstName.data)
        user.set_lastName(updateUserForm.lastName.data)
        user.set_username(updateUserForm.username.data)
        user.set_password(updateUserForm.password.data)
        user.set_gender(updateUserForm.gender.data)
        user.set_country(updateUserForm.country.data)
        user.set_address(updateUserForm.address.data)
        user.set_number(updateUserForm.number.data)

        db['Users'] = userDict
        db.close()
        return render_template('updateUser.html',form=updateUserForm, error='Account has been updated')
    else:
        userDict = {}
        db = shelve.open('storage.db', 'r')
        userDict = db['Users']
        db.close()
        user = userDict[id]
        updateUserForm.firstName.data = user.get_firstName()
        updateUserForm.lastName.data = user.get_lastName()
        updateUserForm.username.data = user.get_username()
        updateUserForm.gender.data = user.get_gender()
        updateUserForm.country.data = user.get_country()
        updateUserForm.address.data = user.get_address()
        updateUserForm.number.data = user.get_number()
    return render_template('updateUser.html',form=updateUserForm, error='')



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


@app.route('/createProduct', methods=['GET', 'POST'])
def createProduct():
    createProductForm = CreateProduct(request.form)
    if request.method == 'POST' and createProductForm.validate():
        itemsDict = {}
        db = shelve.open('items.db', 'c')
        try:
            itemsDict = db['Product']
            Product.Product.countID = db['CountID']
        except:
            print('Error in retrieving Items from items.db.')
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(createProductForm.itemID.data) + '.jpg')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            item = Product.Product(createProductForm.itemID.data, createProductForm.name.data,
                                   createProductForm.price.data, createProductForm.color.data,
                                   createProductForm.size.data, createProductForm.quantity.data,
                                   createProductForm.gender.data, createProductForm.description.data)

            itemsDict[item.get_itemID()] = item
            db['Product'] = itemsDict
            db['CountID'] = Product.Product.countID
            db.close()

            return redirect(url_for('retrieveProducts'))
    return render_template('createProduct.html', form=createProductForm, status='admin')



@app.route('/retrieveProducts')
def retrieveProducts():
    itemsDict = {}
    db = shelve.open('items.db', 'r')
    itemsDict = db['Product']
    db.close()

    itemsList = []
    for key in itemsDict:
        item = itemsDict.get(key)
        itemsList.append(item)

    return render_template('retrieveProducts.html', itemsList=itemsList, count=len(itemsList), status='user')


@app.route('/deleteProduct/<int:id>', methods=['POST'])
def deleteProduct(id):
    itemsDict = {}
    db = shelve.open('items.db', 'w')
    itemsDict = db['Product']

    itemsDict.pop(id)

    db['Product'] = itemsDict
    db.close()

    return redirect(url_for('retrieveProducts'))


@app.route('/updateProduct/<int:id>', methods=['GET', 'POST'])
def updateProduct(id):
    updateProductForm = CreateProduct(request.form)
    if request.method == 'POST' and updateProductForm.validate():
        itemDict = {}
        db = shelve.open('items.db', 'w')
        itemDict = db['Product']

        item = itemDict.get(id)

        item.set_itemID(updateProductForm.itemID.data)
        item.set_name(updateProductForm.name.data)
        item.set_price(updateProductForm.price.data)
        item.set_color(updateProductForm.color.data)
        item.set_size(updateProductForm.size.data)
        item.set_quantity(updateProductForm.quantity.data)
        item.set_gender(updateProductForm.gender.data)
        item.set_description(updateProductForm.description.data)

        db['Product'] = itemDict
        db.close()

        return redirect(url_for('retrieveProducts', form=updateProductForm, error='Product has been updated'))
    else:
        itemDict = {}
        db = shelve.open('items.db', 'r')
        itemDict = db['Product']
        db.close()

        item = itemDict.get(id)
        updateProductForm.itemID.data = item.get_itemID()
        updateProductForm.name.data = item.get_name()
        updateProductForm.price.data = item.get_price()
        updateProductForm.color.data = item.get_color()
        updateProductForm.size.data = item.get_size()
        updateProductForm.quantity.data = item.get_quantity()
        updateProductForm.gender.data = item.get_gender()
        updateProductForm.description.data = item.get_description()

    return render_template('updateProduct.html',form=updateProductForm, error='')


@app.route('/clothesInfo/<int:id>', methods=['GET', 'POST'])
def clothesInfo(id):
    createProductForm = CreateProduct(request.form)
    if request.method == 'POST' and createProductForm.validate():
        itemDict = {}
        db = shelve.open('items.db', 'w')
        itemDict = db['Product']

        item = itemDict.get(id)
        item.set_name(createProductForm.name.data)
        item.set_price(createProductForm.price.data)
        item.set_color(createProductForm.color.data)
        item.set_size(createProductForm.size.data)
        item.set_description(createProductForm.description.data)

        db['Product'] = itemDict
        db.close()

        itemsList = []
        for key in itemDict:
            item = itemDict.get(key)
            itemsList.append(item)

        return redirect(url_for('retrieveProducts'))

    else:
        itemDict = {}
        db = shelve.open('items.db', 'r')
        itemDict = db['Product']
        db.close()

        item = itemDict.get(id)
        createProductForm.name.data = item.get_name()
        createProductForm.price.data = item.get_price()
        createProductForm.color.data = item.get_color()
        createProductForm.size.data = item.get_size()
        createProductForm.quantity.data = item.get_quantity()
        createProductForm.gender.data = item.get_gender()
        createProductForm.description.data = item.get_description()

        itemsList = []
        for key in itemDict:
            item = itemDict.get(key)
            itemsList.append(item)

        return render_template('clothesInfo.html', status='user', form=createProductForm, id=id, discount=False, color=createProductForm.color.data, price=createProductForm.price.data, name=createProductForm.name.data, gender=createProductForm.gender.data)

    







@app.route('/feedback')
def feedback():
    return render_template('feedback.html')


@app.route('/transaction/<id>', methods=['GET', 'POST'])
def transaction(id):
    updateUserForm = R(request.form)
    if request.method =='POST':
        print("hi")
        #POST
        formDict = {}
        db = shelve.open('form.db', 'c')
        try:
            formDict = db['Details']
            print(updateUserForm.email.data)
            print(updateUserForm.address.data)
            print(updateUserForm.city.data)
            print(updateUserForm.zip.data)
            user = Transaction.Details(id, updateUserForm.email.data, updateUserForm.address.data, updateUserForm.city.data, updateUserForm.zip.data)
            idx = len(formDict)
            formDict[idx] = user
            db['Details'] = formDict


            print( "was stored in shelve successfully with userID =", idx)
            print(formDict)
            db.close()
            itemsDict = {}
            db = shelve.open('items.db', 'r')
            itemsDict = db['Product']
            db.close()

            itemsList = []
            for key in itemsDict:
                item = itemsDict.get(key)
                itemsList.append(item)
            print(itemsDict)
            return render_template('receipt.html', invoice=user, itemsList=itemsDict, count=len(itemsList))
        except:
            print("Error in retrieving Users from storage.db.")
    else:
        #GET
        return render_template('transaction.html', form=updateUserForm, id=id)

@app.route('/receipt')
def receipt():
    itemsDict = {}
    db = shelve.open('items.db', 'r')
    itemsDict = db['Product']
    db.close()

    itemsList = []
    for key in itemsDict:
        item = itemsDict.get(key)
        itemsList.append(item)

    return render_template('receipt.html', itemsList=itemsList, count=len(itemsList))




@app.route('/shop')
def shops():
    itemsDict = {}
    db = shelve.open('items.db', 'r')
    itemsDict = db['Product']
    db.close()

    itemsList = []
    for key in itemsDict:
        item = itemsDict.get(key)
        itemsList.append(item)

    return render_template('shop.html', itemsList=itemsList, count=len(itemsList), status='admin')


@app.route('/contactUs', methods=['GET', 'POST'])
def createFeedback():
    updateFeedbackForm = CreateFeedback(request.form)
    if request.method == 'POST' and updateFeedbackForm.validate():
        feedbackDict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedbackDict = db['Feedback']
        except:
            print('Error in retrieving feedback from Feedback.db.')

        feedback = Feedback.Feedback(updateFeedbackForm.name.data, updateFeedbackForm.number.data, updateFeedbackForm.feedbackZ.data)
        feedbackDict[feedback.get_feedbackID()] = feedback
        db['Feedback'] = feedbackDict
        db.close()

        return redirect(url_for('home'))
    return render_template('contactUs.html', form=updateFeedbackForm, status='admin')

@app.route('/retrieveFeedback')
def retrieveFeedback():
    feedbackDict = {}
    db = shelve.open('feedback.db', 'r')
    feedbackDict = db['Feedback']
    db.close()

    feedbackList = []
    for key in feedbackDict:
        feedback = feedbackDict.get(key)
        feedbackList.append(feedback)

    return render_template('retrieveFeedback.html', feedbackList=feedbackList, count=len(feedbackList), status='admin')

@app.route('/cart')
def cart():
    itemsDict = {}
    db = shelve.open('items.db', 'r')
    itemsDict = db['Product']
    db.close()

    itemsList = []
    for key in itemsDict:
        item = itemsDict.get(key)
        itemsList.append(item)

    return render_template('shoppingCart.html', itemsList=itemsList, count=len(itemsList), status='admin')

@app.route('/deleteFeedback/<int:id>', methods=['POST'])
def deleteFeedback(id):
    feedbackDict = {}
    db = shelve.open('feedback.db', 'w')
    feedbackDict = db['Feedback']

    feedbackDict.pop(id)

    db['Feedback'] = feedbackDict
    db.close()

    return redirect(url_for('retrieveFeedback'))


@app.route("/invoice")
def invoice():
    db = shelve.open('form.db', 'c')
    formDict = db['Details']
    db.close()

    formList = []
    for key in formDict:
        item = formDict.get(key)
        formList.append(item)
    return render_template("invoice.html", invoices=formDict, count=len(formList))



if __name__ == '__main__':
    app.run()







