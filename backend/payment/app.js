const stripe = require('stripe')('sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ');
const express = require('express');
const app = express();
const cors = require('cors');
const fs = require('fs');
const paymentIntentsFile = 'paymentIntents.json';
app.use(express.json());
app.use(cors());


app.post('/create-checkout-session', async (req, res) => {
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price_data: {
        currency: 'sgd',
        product_data: {
          name: req.body.name,
          description: req.body.description,
          images: [req.body.imgUrl],
        },
        unit_amount: req.body.price * 100,
      },
      quantity: 1,
    }],
    mode: 'payment',
    payment_intent_data: {
      capture_method: 'manual',
    },
    success_url: 'http://localhost:8889/pages/profile.html', // Adjust accordingly
    cancel_url: 'http://localhost:8889/cancel.html', // Adjust accordingly
  });
  console.log(session.payment_intent);

  let paymentIntents = {};
  if (fs.existsSync(paymentIntentsFile)) {
    paymentIntents = JSON.parse(fs.readFileSync(paymentIntentsFile));
  }

  // Example: Associating a payment intent ID with a product ID
const productPaymentIntents = {}; // This should ideally be stored in a persistent database

// When creating a checkout session
const productID = req.body.productId; // Make sure this ID is passed in from the client
productPaymentIntents[productID] = session.payment_intent;

fs.writeFileSync(paymentIntentsFile, JSON.stringify(paymentIntents));

res.json({ id: session.id });
});

app.post('/capture-payment', async (req, res) => {
  try {
    const { paymentIntentId } = req.body;
    if (!paymentIntentId) {
      return res.status(400).json({ success: false, message: 'PaymentIntentId is required' });
    }
    const paymentIntent = await stripe.paymentIntents.capture(paymentIntentId);
    res.json({ success: true, paymentIntent });
  } catch (error) {
    console.error('Capture payment error:', error);
    res.status(500).json({ success: false, message: error.message });
  }
});

// Example product-payment intent association (this should be persistent, e.g., in a database)
const productPaymentIntents = {}; // This object should ideally be populated dynamically

app.get('/get-payment-intent-by-product/:productId', (req, res) => {
  const productId = req.params.productId;
  const paymentIntentId = productPaymentIntents[productId];

  if (!paymentIntentId) {
    return res.status(404).json({ error: 'Payment intent ID not found for product.' });
  }

  res.json({ paymentIntentId });
});


app.use(express.json());

app.post('/api/refund', async (req, res) => {
    const { itemId } = req.body;

    try {
        // Lookup the paymentIntentId or chargeId based on itemId
        // This is a placeholder. You'll need to implement this based on your data storage
        const paymentIntentId = await findPaymentIntentIdByItemId(itemId);

        const refund = await stripe.refunds.create({
            payment_intent: paymentIntentId,
            // For partial refunds, specify an amount:
            // amount: 1000, // amount in cents
        });

        res.json({ success: true, refund });
    } catch (err) {
        console.error(err);
        res.status(500).json({ success: false, message: "Failed to process refund." });
    }
});


app.listen(3000, () => console.log('Running on port 3000'));
