const express = require('express');
const router = express.Router();
const stripe = require('stripe')(process.env.sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ); // Ensure this is correctly set in your environment variables
const { recordPayment } = require('./redis');
const firebaseAdmin = require('./firebaseAdmin'); // Ensure you've renamed firebaseConfig.js to firebaseAdmin.js if that's what you're using

// Helper function to verify Firebase ID tokens
async function verifyToken(idToken) {
    try {
        const decodedToken = await firebaseAdmin.auth().verifyIdToken(idToken);
        return decodedToken.uid;
    } catch (error) {
        console.error("Error verifying user token", error);
        throw error; // Or handle this appropriately
    }
}

// Route to create a payment intent
router.post('/create-payment-intent', async (req, res) => {
    try {
        const paymentIntent = await stripe.paymentIntents.create({
            amount: req.body.amount,
            currency: 'sgd',
            // Additional options can be specified here (e.g., customer, payment method types)
        });
        
        res.json({
            clientSecret: paymentIntent.client_secret,
        });
    } catch (err) {
        res.status(500).send({ error: err.message });
    }
});

// Route to confirm a payment
router.post('/confirm', async (req, res) => {
    const { idToken, orderId, paymentIntentId, postId } = req.body;

    try {
        const userId = await verifyToken(idToken); // Verify the Firebase ID token
        
        // Confirm the payment with Stripe
        const confirmedPayment = await stripe.paymentIntents.confirm(paymentIntentId);

        if (confirmedPayment.status === 'succeeded') {
            const paymentDetails = {
                UserID: userId, // From Firebase
                ProductId: postId, // Assumed to be passed in the request body
                PaymentAmount: confirmedPayment.amount, // From Stripe
                payment_intent_id: confirmedPayment.id, // From Stripe
            };

            await recordPayment(`order:${confirmedPayment.id}`, paymentDetails);

            res.json({ success: true, message: 'Payment processed and recorded successfully.' });
        } else {
            res.status(400).json({ success: false, message: 'Payment failed to process.' });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
