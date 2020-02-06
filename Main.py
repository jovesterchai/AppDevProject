from flask import *
from Forms import CreateFeedback, CreateProduct, R   # Input the objects from Forms.py
from Product import Product

import invoice
import shelve, User, Product
import paypalrestsdk as paypal
from paypalrestsdk import *
import Feedback


app = Flask(__name__)


# '/' indicates the root directory of the website
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/createProduct', methods=['GET', 'POST'])
def createProduct():
    createProductForm = CreateProduct(request.form)
    if request.method == 'POST' and createProductForm.validate():
        itemsDict = {}
        db = shelve.open('items.db', 'c')

        try:
            itemsDict = db['Product']
        except:
            print('Error in retrieving Items from items.db.')

        item = Product.Product(createProductForm.itemID.data, createProductForm.name.data, createProductForm.price.data, createProductForm.color.data, createProductForm.size.data, createProductForm.quantity.data, createProductForm.gender.data, createProductForm.description.data)
        itemsDict[item.get_itemID()] = item
        db['Product'] = itemsDict
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

        return render_template('clothesInfo.html', status='user', form=createProductForm, id=id, discount=False, name=createProductForm.name.data, gender=createProductForm.gender.data)

    
paypal.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "ARJH-zCA-RA5S_IfUZVN24eiWHjHKtfsWJ8bSY8q6G2YEs_HjEhGTHMSMC9p89n1usSef78-wKLxd00y",
    "client_secret": "EHpf5bw8kc_jHI8xPG40RDI9D4dRgBEKorQu9XsMJUI4stky2GMC-tXse4eXoaN-FjYDEZva-m6gb95S"})


def to_json(func):
    def wrapper(*args, **kwargs):
        get_fun = func(*args, **kwargs)
        return json.dumps(get_fun)

    return wrapper


@app.route('/t')
def index():
    history = paypal.Payment.all({"count": 50})
    history_dic = {}
    history_list = []
    for payment in history.payments:
        history_dic['payment_id'] = payment.id
        history_dic['sale_id'] = payment.transactions[0].related_resources[0].sale.id
        history_dic['amount'] = payment.transactions[0].amount.total + " " + history.payments[0].transactions[
            0].amount.currency
        history_list.append(history_dic)
        history_dic = {}
    return render_template("index.html", **locals())


@app.route('/paypal_Return/<int:id>', methods=['GET'])
def paypal_Return(id):
    updateProductForm = R(request.form)
    # ID of the payment. This ID is provided when creating payment.
    paymentId = request.args['paymentId']
    payer_id = request.args['PayerID']
    payment = paypal.Payment.find(paymentId)

    # PayerID is required to approve the payment.
    if payment.execute({"payer_id": payer_id}):  # return True or False
        print("Payment[%s] execute successfully" % (payment.id))
        return render_template('receipt.html', id=id)
    else:
        print(payment.error)
        return 'Payment execute ERROR!'


@app.route('/paypal_payment/<int:id>', methods=['GET'])
def paypal_payment(id):
    # Payment
    # A Payment Resource; create one using
    # the above types and intent as 'sale'
    payment = paypal.Payment({
        "intent": "sale",

        # Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"},

        # Redirect URLs
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5000/paypal_Return?success=true",
            "cancel_url": "http://127.0.0.1:5000/paypal_Return?cancel=true"},

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "60.00",
                    "currency": "USD",
                    "quantity": 1}]},

            # Amount
            # Let's you specify a payment amount.
            "amount": {
                "total": "60.0",
                "currency": "USD"},
            "description": "test 123 This is the payment transaction description."}]})

    # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                # Convert to str to avoid google appengine unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (link.href))
                return redirect(redirect_url)
    else:
        print("Error while creating payment:")
        print(payment.error)
        return "Error while creating payment"


@app.route('/credit_card_payment', methods=['GET'])
def credit_card_payment():
    # Payment
    # A Payment Resource; create one using
    # the above types and intent as 'sale'
    payment = Payment({
        "intent": "sale",

        # Payer
        # A resource representing a Payer that funds a payment
        # Use the List of `FundingInstrument` and the Payment Method
        # as 'credit_card'
        "payer": {
            "payment_method": "credit_card",

            # FundingInstrument
            # A resource representing a Payeer's funding instrument.
            # Use a Payer ID (A unique identifier of the payer generated
            # and provided by the facilitator. This is required when
            # creating or using a tokenized funding instrument)
            # and the `CreditCardDetails`
            "funding_instruments": [{

                # CreditCard
                # A resource representing a credit card that can be
                # used to fund a payment.
                "credit_card": {
                    "type": "visa",
                    "number": "4032037537194421",
                    "expire_month": "11",
                    "expire_year": "2021",
                    "cvv2": "875",
                    "first_name": "twtrubiks",
                    "last_name": "test",

                    # Address
                    # Base Address used as shipping or billing
                    # address in a payment. [Optional]
                    "billing_address": {
                        "line1": "1 Main St",
                        "city": "San Jose",
                        "state": "CA",
                        "postal_code": "95131",
                        "country_code": "US"}}}]},

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": [{
                    "name": "item",
                    "sku": "item",
                    "price": "30.00",
                    "currency": "USD",
                    "quantity": 1}]},

            # Amount
            # Let's you specify a payment amount.
            "amount": {
                "total": "30.00",
                "currency": "USD"},
            "description": "This is the payment transaction description."}]})

    # Create Payment and return status( True or False )
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        return "Payment " + payment.id + " created successfully"
    else:
        # Display Error message
        print("Error while creating payment:")
        print(payment.error)
        return "Payment Error!"


@app.route('/API/refund_payment', methods=['POST'])
@to_json
def refund_payment():
    sale_id = request.json.get('sale_id')
    amount = request.json.get('amount')
    sale = Sale.find(sale_id)

    # Make Refund API call
    # Set amount only if the refund is partial
    refund = sale.refund({
        "amount": {
            "total": int(amount),
            "currency": "USD"}})

    if refund.success():
        print("Refund[%s] Success" % (refund.id))
        return 11
    else:
        print("Unable to Refund")
        print(refund.error)
        return 44


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/transaction/<id>', methods=['GET', 'POST'])
def transaction(id):
    if request.method == 'POST':
        invoice2 = invoice.Invoice(id,0)
        db = shelve.open('invoice.db', 'c')
        db['Invoice'] = {}
        invoiceDict = db['Invoice']
        invoiceDict[len(invoiceDict)] = invoice2
        db['Invoice'] = invoiceDict
        itemsDict = {}
        db = shelve.open('items.db', 'r')
        itemsDict = db['Product']
        db.close()

        itemsList = []
        for key in itemsDict:
            item = itemsDict.get(key)
            itemsList.append(item)
        print(itemsDict)
        return render_template('receipt.html', invoice=invoice2, itemsList=itemsDict, count=len(itemsList))
    else:
        updateProductForm = R(request.form)


        return render_template('transaction.html', form=updateProductForm, id=id)


@app.route('/receipt')
def invoicetest():
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


@app.route('/login')
def login():
    return render_template('login.html')


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

        feedback = Feedback.Feedback(updateFeedbackForm.name.data, updateFeedbackForm.country.data, updateFeedbackForm.feedbackZ.data)
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

if __name__ == '__main__':
    app.run()







