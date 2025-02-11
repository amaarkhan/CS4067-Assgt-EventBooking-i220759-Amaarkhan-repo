const mongoose = require("mongoose");

const EventSchema = new mongoose.Schema({
    name: { type: String, required: true },
    date: { type: Date, required: true },
    location: { type: String, required: true },
    available_tickets: { type: Number, required: true, min: 0 },
    price: { type: Number, required: true },
    category: { type: String, enum: ["Music", "Sports", "Tech", "Theatre"], required: true }, // 🔹 New category field
    status: { type: String, enum: ["active", "inactive"], default: "active" } // 🔹 Soft delete
}, { timestamps: true });

const Event = mongoose.model("Event", EventSchema);

module.exports = Event;
