# CS4067-Assgt-EventBooking-i220759-Amaarkhan-repo
# Event Booking System
#Amaar khan 22i-0759
#haider bukhari 22i-0980

A web-based event booking system that allows users to browse, book, and manage events. The project follows a microservices architecture with separate services for users, events, and bookings.

---


## 📌 Features

- **User Authentication** (Register, Login)
- **Event Management** (Create, Update, Delete)
- **Booking System** (Users can book events and manage bookings)
- **Microservices Architecture** (Independent services for scalability)
- **Messaging Queue** (RabbitMQ for inter-service communication)
- **RESTful APIs** (Standardized endpoints for frontend interaction)

---

## 🏗️ Architecture

The system consists of three main services:

### 🟢 **User Service**
- **Responsibilities**: Handles user authentication and profile management.
- **Technology Stack**:
  - Backend: Python (Flask)
  - Database: MongoDB
  - Communication: RESTful APIs, RabbitMQ

### 🔵 **Event Service**
- **Responsibilities**: Manages events (creation, retrieval, updating, deletion).
- **Technology Stack**:
  - Backend: Python (Flask)
  - Database: MongoDB
  - Communication: RESTful APIs, RabbitMQ

### 🔴 **Booking Service**
- **Responsibilities**: Handles event bookings and manages reservations.
- **Technology Stack**:
  - Backend: Node.js (Express)
  - Database: MongoDB
  - Communication: RESTful APIs, RabbitMQ

---

## 📡 API Documentation

### **User Service**
#### 🟢 Register a New User
**POST** `/api/users/register`
##### Request:
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepassword"
}

Response:

{
  "message": "User registered successfully!",
  "userId": "unique_user_id"
}

🟢 User Login

POST /api/users/login
Request:

{
  "email": "johndoe@example.com",
  "password": "securepassword"
}

Response:

{
  "token": "jwt_token_here",
  "user": {
    "id": "unique_user_id",
    "username": "johndoe",
    "email": "johndoe@example.com"
  }
}

Event Service
🔵 Create a New Event

POST /api/events
Request:

{
  "title": "Tech Conference 2025",
  "description": "Annual technology event.",
  "date": "2025-06-15",
  "location": "New York",
  "availableSeats": 100
}

Response:

{
  "message": "Event created successfully!",
  "eventId": "unique_event_id"
}

🔵 Retrieve All Events

GET /api/events
Response:

[
  {
    "id": "unique_event_id",
    "title": "Tech Conference 2025",
    "description": "Annual technology event.",
    "date": "2025-06-15",
    "location": "New York",
    "availableSeats": 100
  }
]

Booking Service
🔴 Book an Event

POST /api/bookings
Request:

{
  "userId": "unique_user_id",
  "eventId": "unique_event_id"
}

Response:

{
  "message": "Booking confirmed!",
  "bookingId": "unique_booking_id"
}

🔴 Retrieve User Bookings

GET /api/bookings/user/:userId
Response:

[
  {
    "bookingId": "unique_booking_id",
    "event": {
      "id": "unique_event_id",
      "title": "Tech Conference 2025",
      "date": "2025-06-15",
      "location": "New York"
    },
    "status": "confirmed"
  }
]



🚀 Setup Guide
Prerequisites

    Node.js (v14+)
    Python (v3.8+)
    MongoDB (v4+)
    RabbitMQ (v3+)
    npm (v6+)
    pip (latest version)

2️⃣ Setting Up Services

Each service is inside its respective folder.
🟢 User Service Setup

cd User_Service
python -m venv env
source env/bin/activate  # (On Windows: .\env\Scripts\activate)
pip install -r requirements.txt

Create .env file:

FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/user_service_db

Run the service:

flask run --port=5001

🔵 Event Service Setup

cd Event_Service
python -m venv env
source env/bin/activate
pip install -r requirements.txt

Create .env file:

FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/event_service_db

Run the service:

flask run --port=5002

🔴 Booking Service Setup

cd Booking_Service
npm install

Create .env file:

PORT=5003
MONGO_URI=mongodb://localhost:27017/booking_service_db

Run the service:

node server.js


3️⃣ Start RabbitMQ

Ensure RabbitMQ is installed and running:

rabbitmq-server
