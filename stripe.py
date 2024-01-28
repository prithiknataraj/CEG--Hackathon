from flask import Flask, render_template, request, redirect, url_for
import stripe

app = Flask(__name__)

public_key = "pk_test_51OAc4kSCU9tagpDmW1MEp5JyCw7sfmbVqlxs4SYpfxGpoFsCHxbEzW69eKIWK7Sr1XHWx4CROKSLZZ90h7iAHgtT00Zmb1OGcC"
stripe.api_key = "sk_test_51OAc4kSCU9tagpDmxHbWoT7JizAtvE7yZGeKBKWGE7SfojdYPZPW1AIyjmVcS0bXXZF7S0YUsj9unkcXiOFH3Jvn001ZVKT8ir"

@app.route('/')
def index():
    return render_template('stripe_index.html', public_key=public_key)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/payment', methods=['POST'])
def payment():

    # CUSTOMER INFO
    customer = stripe.Customer.create(email=request.form['stripeEmail'],
                                      source=request.form['stripeToken'])

    # PAYMENT INFO
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999, # 19.99
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('thankyou'))

if __name__ == '__main__':
    app.run(debug=True)