# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

import json
import os
import stripe

from flask import Flask, jsonify, request

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_9dc498f9c2aefbac7559e63722f97d6108c9ab3a4001c08865f1452ea70a2632'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'charge.captured':
      charge = event['data']['object']
    elif event['type'] == 'charge.expired':
      charge = event['data']['object']
    elif event['type'] == 'charge.failed':
      charge = event['data']['object']
    elif event['type'] == 'charge.pending':
      charge = event['data']['object']
    elif event['type'] == 'charge.refunded':
      charge = event['data']['object']
    elif event['type'] == 'charge.succeeded':
      charge = event['data']['object']
    elif event['type'] == 'charge.updated':
      charge = event['data']['object']
    elif event['type'] == 'charge.dispute.closed':
      dispute = event['data']['object']
    elif event['type'] == 'charge.dispute.created':
      dispute = event['data']['object']
    elif event['type'] == 'charge.dispute.funds_reinstated':
      dispute = event['data']['object']
    elif event['type'] == 'charge.dispute.funds_withdrawn':
      dispute = event['data']['object']
    elif event['type'] == 'charge.dispute.updated':
      dispute = event['data']['object']
    elif event['type'] == 'charge.refund.updated':
      refund = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_failed':
      session = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_succeeded':
      session = event['data']['object']
    elif event['type'] == 'checkout.session.completed':
      session = event['data']['object']
    elif event['type'] == 'payment_intent.amount_capturable_updated':
      payment_intent = event['data']['object']
    elif event['type'] == 'person.created':
      person = event['data']['object']
    elif event['type'] == 'refund.created':
      refund = event['data']['object']
    elif event['type'] == 'refund.updated':
      refund = event['data']['object']
    elif event['type'] == 'source.refund_attributes_required':
      source = event['data']['object']
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)

# Import necessary libraries
import stripe

# Handle the webhook event
def handle_event(event):
    # Handle different event types here
    if event['type'] == 'charge.succeeded':
        # Extract charge ID from the event
        charge_id = event['data']['object']['id']
        # Process the successful charge event
        # For example, update your database with the charge ID

    elif event['type'] == 'payment_intent.succeeded':
        # Extract payment intent ID from the event
        payment_intent_id = event['data']['object']['id']
        # Process the successful payment intent event
        # For example, update your database with the payment intent ID
