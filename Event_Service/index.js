const express = require("express");
const dotenv = require("dotenv");
const connectDB = require("./config/db");
const eventRoutes = require("./routes/eventRoutes");

// Load environment variables
dotenv.config();

// Connect to MongoDB
connectDB();

const app = express();

// Middleware
app.use(express.json()); // Allows JSON body parsing

// Routes
app.use("/events", eventRoutes);

// Simple Route to Check if Server is Running
app.get("/", (req, res) => {
    res.send("Event Service is Running!");
});

// Start the Server
const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on port ${PORT}`);
});
