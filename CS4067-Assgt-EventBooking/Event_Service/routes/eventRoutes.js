const express = require("express");
const Event = require("../models/event.js");

const router = express.Router();

// ✅ Create a New Event (Admins Only)
router.post("/", async (req, res) => {
    try {
        const { name, date, location, available_tickets, price, category, status } = req.body;

        // 🔹 Validate required fields
        if (!name || !date || !location || !available_tickets || !price || !category) {
            return res.status(400).json({ message: "All fields are required!" });
        }

        // 🔹 Ensure category is valid
        const validCategories = ["Music", "Sports", "Tech", "Theatre"];
        if (!validCategories.includes(category)) {
            return res.status(400).json({ message: "Invalid category! Choose from: Music, Sports, Tech, Theatre." });
        }

        // 🔹 Set default status to "active" if not provided
        const eventStatus = status || "active";

        const newEvent = new Event({
            name,
            date,
            location,
            available_tickets,
            price,
            category,
            status: eventStatus
        });

        await newEvent.save();

        res.status(201).json({ message: "Event created successfully!", event: newEvent });
    } catch (error) {
        console.error("Error creating event:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});

// ✅ Get All Events with Pagination, Filtering & Search
router.get("/", async (req, res) => {
    try {
        // 🔹 Pagination
        let page = parseInt(req.query.page) || 1; // Default: Page 1
        let limit = parseInt(req.query.limit) || 10; // Default: 10 events per page
        let skip = (page - 1) * limit;

        // 🔹 Filtering
        let query = {};
        if (req.query.date) query.date = req.query.date; // Filter by date
        if (req.query.location) query.location = { $regex: req.query.location, $options: "i" }; // Case-insensitive location
        if (req.query.minPrice && req.query.maxPrice) {
            query.price = { $gte: parseFloat(req.query.minPrice), $lte: parseFloat(req.query.maxPrice) }; // Price range
        }

        // 🔹 Search by Event Name
        if (req.query.search) {
            query.name = { $regex: req.query.search, $options: "i" }; // Case-insensitive search
        }

        // Fetch filtered & paginated events
        const events = await Event.find(query).skip(skip).limit(limit);
        const totalEvents = await Event.countDocuments(query);

        res.json({
            totalEvents,
            currentPage: page,
            totalPages: Math.ceil(totalEvents / limit),
            events
        });
    } catch (error) {
        console.error("Error fetching events:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
});


// ✅ Get Event by ID (Only if Tickets Are Available)
router.get("/:id", async (req, res) => {
    try {
        const event = await Event.findById(req.params.id);

        if (!event) {
            return res.status(404).json({ message: "Event not found" });
        }

        if (event.available_tickets <= 0) {
            return res.status(400).json({ message: "Event is sold out!" });
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
