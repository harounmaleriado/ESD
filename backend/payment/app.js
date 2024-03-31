const stripe = require('stripe')('sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ');
const express = require('express');
const app = express();
const cors = require('cors');
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
        unit_amount: req.body.price * 100, // Convert price to cents
      },
      quantity: 1,
    }],
    mode: 'payment',
    success_url: 'https://your-website.com/success',
    cancel_url: 'https://your-website.com/cancel',
  });

  res.json({ id: session.id });
});

app.listen(3000, () => console.log('Running on port 3000'));
