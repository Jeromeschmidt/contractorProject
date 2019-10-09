from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime
from twilio.rest import Client
import os
import stripe

from dotenv import load_dotenv
load_dotenv()

host = os.environ.get('MONGODB_URI')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items


twilio_account_sid = os.getenv("account_sid")
twilio_auth_token = os.getenv("auth_token")

twilioClient = Client(twilio_account_sid, twilio_auth_token)

stripe.api_key = os.getenv("stripe_key")
stripe_pub_key = os.getenv("stripe_pub_key")


app = Flask(__name__)

#home page that will show many items
@app.route('/')
def store_index():
    """Show all items."""
    return render_template('store_index.html', items=items.find())

#owner landing page
@app.route('/owner')
def owner():
    """takes user to owner landing page"""
    return render_template('owner.html', items=items.find())

#displays a single item to owner
@app.route('/owner/<item_id>')
def owner_view_item(item_id):
    """Show a single item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('owner_view_item.html', item=item)

#creates a new item
@app.route('/item', methods=['POST'])
def item_submit():
    """Submit a new item."""
    item = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'images': request.form.get('images').split(),
        'created_at': datetime.now(),
        'in_shopping_cart': False
    }
    item_id = items.insert_one(item).inserted_id
    return render_template('owner.html', items=items.find())

#adds a new item
@app.route('/owner/add_item')
def add_item():
    """Create a new item."""
    return render_template('item_new.html', item={}, title='New item')

#lets the owner edit an item
@app.route('/owner/<item_id>/edit', methods=['POST'])
def edit_item(item_id):
    """edit an item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('edit_item.html', item=item, title='edit item')

#updates an edited item
@app.route('/owner/<item_id>', methods=['POST'])
def item_update(item_id):
    """Submit an edited playlist."""
    updated_item = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'images': request.form.get('images').split()
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})
    return redirect(url_for('owner', item_id=item_id))

#lets owner delete an item
@app.route('/owner/<item_id>/delete', methods=['POST'])
def item_delete(item_id):
    """Delete one item."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('owner'))

#displays a specific item
@app.route('/<item_id>')
def item_show(item_id):
    """Show a single item."""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('item_show.html', item=item)

#shows the users shopping cart
@app.route('/shopping_cart')
def shopping_cart():
    """display user's shopping cart"""
    return render_template('shopping_cart.html', items=items.find())

#adds an item to the shopping cart
@app.route('/shopping_cart/<item_id>/add_to_cart', methods=['POST'])
def add_to_shopping_cart(item_id):
    """display user's shopping cart"""
    items.update_one({'_id':ObjectId(item_id)}, {"$set": {"in_shopping_cart" : True}}, upsert=False)
    return render_template('shopping_cart.html', items=items.find())

#deletes an item from the shopping cart
@app.route('/shopping_cart/<item_id>/delete_from_cart', methods=['POST'])
def delete_from_shopping_cart(item_id):
    """display user's shopping cart"""
    items.update_one({'_id':ObjectId(item_id)}, {"$set": {"in_shopping_cart" : False}}, upsert=False)
    return render_template('shopping_cart.html', items=items.find())

#finds the total amount due for items in shopping cart
def amount_in_cart():
    amount = 0
    for item in items.find():
        if item["in_shopping_cart"]:
            amount = amount + int(item["price"])
    amount = amount*100
    return amount

#takes the user to a checkout page
@app.route('/shopping_cart/checkout')
def checkout():
    """display user's shopping cart"""
    return render_template('checkout.html', key=stripe_pub_key, amount=amount_in_cart())

#takes the user to a thank you page, and sends a  text message to owner
@app.route('/shopping_cart/checkout/thanks', methods=['POST'])
def thanks():
    #processes stripe payment
    try:
        amount = amount_in_cart()

        customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
        )

        stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
        )
    except stripe.error.StripeError:
        return render_template('error.html')
    """display a thank you to user and send them a text message"""
    #send text message to user
    message = twilioClient.messages.create(body="Another purchase!", from_='+18044915709', to='+14028407963')
    #clear cart
    items.update_many({}, {"$set": {"in_shopping_cart" : False}}, upsert=False)
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
