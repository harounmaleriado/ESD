const stripe = require('stripe')('sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ');
const express = require('express');
const app = express();
const cors = require('cors');
const fs = require('fs');
const paymentIntentsFile = 'paymentIntents.json';

const bodyParser = require('body-parser');
const paymentRoutes = require('./paymentintent');
const admin = require('./firebaseAdmin');
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

app.post('/verify-token', async (req, res) => {
  try {
    const token = req.body.token;
    const decodedToken = await admin.auth().verifyIdToken(token);
    res.send(`Token belongs to user with ID: ${decodedToken.uid}`);
  } catch (error) {
    res.status(401).send('Token verification failed');
  }
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});


