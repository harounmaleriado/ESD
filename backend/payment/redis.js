const redis = require('redis');

// Create a Redis client
const client = redis.createClient({
    url: 'redis://127.0.0.1:6379' // Replace with your Redis instance URL
});

client.on('connect', () => console.log('Connected to Redis!'));
client.on('error', (err) => console.log('Redis Client Error', err));

// Connect to Redis
client.connect();

async function recordPayment(orderId, paymentDetails) {
    try {
        await client.hSet(`orders:${orderId}`, paymentDetails);
        console.log(`Order ${orderId} payment details recorded successfully.`);
    } catch (error) {
        console.error('Failed to record payment details:', error);
    }
}
module.exports = { recordPayment };

