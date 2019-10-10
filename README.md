# Contractor Shoe Store

### Features:
* Only allows owner to add, edit, and delete items
* Lets normal users add items they want to buy to a shopping cart
* Once a user is ready to checkout, the Stripe checkout API is used to collect payment information and process payment
* After payment is accepted, user is taken to a thank you page and owner is sent a text message using the Twilio API
* Shopping cart is then emptied
* Route tests are included for 100% of routes
