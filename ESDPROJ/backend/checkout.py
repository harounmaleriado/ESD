import os

import stripe
from flask import Flask, redirect, request

app = Flask(__name__)

stripe.api_key = 'sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ'

@app.route('/checkout', methods=['POST'])
def create_checkout_session():
    if request.method == 'POST':
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8888/success',
            cancel_url='http://localhost:8888/cancel',
        )
        return redirect(session.url, code=303)

if __name__ == '__main__':
    app.run(port=8888, debug= True)
