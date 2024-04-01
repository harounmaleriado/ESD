from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

# Set your Stripe secret key
stripe.api_key = "sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ"

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/refund', methods=['POST'])
def refund_request():
    try:
        reason = request.json['reason']
        payment_intent_id = request.json['payment_intent_id']  # Retrieve payment intent ID from the request
        
        # Retrieve payment intent
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        # Retrieve charge ID from payment intent
        charge_id = payment_intent.charges.data[0].id

        # Initiate refund request through Stripe
        refund = stripe.Refund.create(
            charge=charge_id,
            reason=reason
        )

        # Return success message along with payment intent details
        return jsonify({'message': 'Refund request successful.', 'refund_id': refund.id}), 200
    except stripe.error.StripeError as e:
        # Return specific Stripe-related error message
        return jsonify({'message': 'Stripe Error: {}'.format(str(e))}), 500
    except Exception as e:
        # Return generic error message
        return jsonify({'message': 'Error: {}'.format(str(e))}), 500

if __name__ == '__main__':
    app.run(debug=True)
