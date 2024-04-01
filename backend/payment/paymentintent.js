const express = require('express');
const router = express.Router();
const stripe = require('stripe')(process.env.sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ);
const { recordPayment } = require('./redis');

app.post('/create-payment-intent', async (req, res) => {

    try {
        const paymentIntent = await stripe.paymentIntents.create({
            amount: req.body.amount,
            currency: 'sgd',
            // Additional options can be specified here (e.g., customer, payment method types)
        });

        router.post('/confirm', async (req, res) => {
            const { orderId, paymentIntentId } = req.body;
            try {
                // Confirm the payment with Stripe or another method
                const confirmedPayment = await stripe.paymentIntents.confirm(paymentIntentId);

                // If payment was successful, record in Redis
                if (confirmedPayment.status === 'succeeded') {
                    const paymentDetails = {
                        ProductId: "123", // Ideally, these details are dynamically determined
                        UserID: "abc",
                        PaymentAmount: "100",
                        payment_intent_id: confirmedPayment.id,
                    };

                    await recordPayment(orderId, paymentDetails);

                    res.json({ success: true, message: 'Payment processed and recorded successfully.' });
                }
            } catch (error) {
                res.status(500).json({ error: error.message });
            }
        });
        res.json({
            clientSecret: paymentIntent.client_secret,
        });
    } catch (err) {
        res.status(500).send({ error: err.message });
    }
});
