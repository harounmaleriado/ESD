const functions = require('firebase-functions');
const admin = require('firebase-admin');
const stripe = require('stripe')('sk_test_51OrzrBC0QgRlIqeyFHKWaaAJAPPGyIwH4r5SLQtBmTTkfz2xLiwtHEnD1EbB1M9CQ3xwlQ3MyjxoL0FsjH8wgHQI009q2nEPLJ');

admin.initializeApp();

exports.syncProductsWithStripe = functions.firestore.document('products/{productId}')
    .onWrite(async (change, context) => {
        const productData = change.after.exists ? change.after.data() : null;
        const productId = context.params.productId;

        if (productData) {
            try {
                let stripePrice;

                // Check if product has a price defined
                if (productData.price) {
                    // Check if the product has a corresponding price in Stripe
                    if (productData.stripePriceId) {
                        // Retrieve the existing price from Stripe
                        stripePrice = await stripe.prices.retrieve(productData.stripePriceId);
                    } else {
                        // Create a new price in Stripe
                        stripePrice = await stripe.prices.create({
                            product: productData.stripeProductId, // The ID of the corresponding product in Stripe
                            unit_amount: productData.price * 100, // Price in cents (Stripe expects price in the smallest currency unit)
                            currency: 'usd', // Change this according to your currency
                        });

                        // Update Firestore with the created Stripe price ID
                        await admin.firestore().doc(`products/${productId}`).update({
                            stripePriceId: stripePrice.id
                        });
                    }
                }

                // Check if product exists in Stripe
                const stripeProduct = await stripe.products.retrieve(productData.stripeProductId);

                // If product exists, update it
                await stripe.products.update(stripeProduct.id, {
                    name: productData.name,
                    description: productData.description,
                    // Update other fields as needed
                });
            } catch (error) {
                console.error("Error syncing product with Stripe:", error);
            }
        } else {
            // Handle product deletion
            // You may want to delete the corresponding product and price in Stripe as well
        }
    });
