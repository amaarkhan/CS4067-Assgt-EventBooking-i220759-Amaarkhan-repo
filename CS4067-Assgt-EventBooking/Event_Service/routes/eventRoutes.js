const express = require("express");
const Event = require("../models/event.js");


const router = express.Router();

// ✅ Create a New Event
router.post("/", async (req, res) => {
    try {
        const { name, date, location, available_tickets, price } = req.body;

        // Validate required fields
        if (!name || !date || !location || !available_tickets || !price) {
            return res.status(400).json({ message: "All fields are required!" });
        }

        const newEvent = new Event({ name, date, location, available_tickets, price });
        await newEvent.save();

        res.status(201).json({ message: "Event created successfully!", event: newEvent });
    } catch (error) {
        console.error("Error creating event:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

// ✅ Get All Events
router.get("/", async (req, res) => {
    try {
        const events = await Event.find();
        res.json(events);
    } catch (error) {
        console.error("Error fetching events:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

// ✅ Get Event by ID
router.get("/:id", async (req, res) => {
    try {
        const event = await Event.findById(req.params.id);
        if (!event) {
            return res.status(404).json({ message: "Event not found" });
        }
        res.json(event);
    } catch (error) {
        console.error("Error fetching event:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

// ✅ Update Event
router.put("/:id", async (req, res) => {
    try {
        const updatedEvent = await Event.findByIdAndUpdate(req.params.id, req.body, { new: true });
        if (!updatedEvent) {
            return res.status(404).json({ message: "Event not found" });
        }
        res.json({ message: "Event updated successfully!", event: updatedEvent });
    } catch (error) {
        console.error("Error updating event:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

// ✅ Delete Event
router.delete("/:id", async (req, res) => {
    try {
        const deletedEvent = await Event.findByIdAndDelete(req.params.id);
        if (!deletedEvent) {
            return res.status(404).json({ message: "Event not found" });
        }
        res.json({ message: "Event deleted successfully!" });
    } catch (error) {
        console.error("Error deleting event:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

module.exports = router;
