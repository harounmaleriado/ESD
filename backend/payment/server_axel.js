const express = require("express");
const cors = require("cors");
const { createClient } = require("redis");

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json()); // for parsing application/json

const client = createClient({
  password: "Ws4LewIBWvtmsdIEdxQlQg1b0aDbTBqZ",
  socket: {
    host: "redis-10539.c295.ap-southeast-1-1.ec2.cloud.redislabs.com",
    port: 10539,
  },
});

client.on("error", (err) => console.log("Redis Client Error", err));

app.post("/post-data", async (req, res) => {
  try {
    await client.connect();

    // Destructure the four variables from the request body
    const { ListingId, Email, PaymentAmount, payment_intent_id } = req.body;

    // Assuming you want to use ListingId as a unique key for a Redis hash
    const redisKey = `listing:${ListingId}`;

    // Save the data to Redis using a hash data structure
    await client.hSet(redisKey, {
      Email: Email,
      PaymentAmount: PaymentAmount,
      payment_intent_id: payment_intent_id,
    });

    await client.disconnect();
    res.status(200).json({ message: "Payment data saved to Redis" });
  } catch (error) {
    console.error("Error saving data to Redis:", error);
    res
      .status(500)
      .json({ message: "Error saving data to Redis", error: error.message });
  }
});

app.listen(port, () =>
  console.log(`Server listening at http://localhost:${port}`)
);
