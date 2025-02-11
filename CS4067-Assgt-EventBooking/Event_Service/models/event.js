const mongoose = require("mongoose");

const EventSchema = new mongoose.Schema({
    name: {
        type: String,
        required: [true, "Event name is required"],
    },
    date: {
        type: Date,
        required: [true, "Event date is required"],
    },
    location: {
        type: String,
        required: [true, "Event location is required"],
    },
    available_tickets: {
        type: Number,
        required: [true, "Number of available tickets is required"],
        min: 0,
    },
    price: {
        type: Number,
        required: [true, "Event ticket price is required"],
    }
}, { timestamps: true });

const Event = mongoose.model("Event", EventSchema);

module.exports = Event;
