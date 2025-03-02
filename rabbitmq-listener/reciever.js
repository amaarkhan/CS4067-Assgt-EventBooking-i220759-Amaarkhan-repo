const amqp = require("amqplib");
const axios = require("axios");

const RABBITMQ_URL = "amqp://localhost"; // Change if RabbitMQ is on a different server
const QUEUE_NAME = "booking_queue"; // Name of the queue
const USER_SERVICE_URL = "http://127.0.0.1:8001/users"; // FastAPI User Service

async function fetchUserDetails(userId) {
    try {
        const response = await axios.get(`${USER_SERVICE_URL}/${userId}`);
        return response.data; // Returns { id, username, email }
    } catch (error) {
        console.error(`❌ Failed to fetch user details for ID ${userId}:`, error.response?.data || error.message);
        return null;
    }
}

async function startConsumer() {
    try {
        // Connect to RabbitMQ
        const connection = await amqp.connect(RABBITMQ_URL);
        const channel = await connection.createChannel();

        // Ensure the queue exists
        await channel.assertQueue(QUEUE_NAME, { durable: true });

        console.log(`🚀 Waiting for messages in queue: ${QUEUE_NAME}...`);

        // Consume messages
        channel.consume(QUEUE_NAME, async (msg) => {
            if (msg !== null) {
                const message = JSON.parse(msg.content.toString());
                console.log(`✅ Booking confirmed for user`, message);

                // Fetch user details using user_id
                const user = await fetchUserDetails(message.user_id);

                if (user) {
                    console.log(`📧 Email for user ${message.user_id}: ${user.email}`);
                } else {
                    console.log(`⚠️ User details not found for user_id: ${message.user_id}`);
                }

                // Acknowledge the message
                channel.ack(msg);
            }
        });
    } catch (error) {
        console.error("❌ Error connecting to RabbitMQ:", error);
    }
}

startConsumer();
