from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
import requests
import pika  # ✅ Import RabbitMQ client
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EVENT_SERVICE_URL = "http://127.0.0.1:4000/events/"  # ✅ Event Service URL

# RabbitMQ settings
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "booking_queue"

# Initialize FastAPI
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# ✅ Create Database Tables
Base.metadata.create_all(bind=engine)

# ✅ Booking Model (Table)
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    num_tickets = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)  # No ForeignKey constraint

# ✅ Pydantic Schema for Request Body
class BookingCreate(BaseModel):
    event_id: str
    amount: float
    num_tickets: int

# ✅ Function to Verify JWT Token & Extract User ID
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ✅ Function to Check if Event Exists
def check_event_exists(event_id: str):
    response = requests.get(f"{EVENT_SERVICE_URL}{event_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Event not found or unavailable")
    return response.json()

# ✅ Function to Publish Message to RabbitMQ
def publish_booking_message(user_id: int, ammount: str, no_of_ticket: str):
    try:
        # Establish connection
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()

        # Declare queue
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # Create message payload
        message = json.dumps({
            "user_id": user_id,
            "ammount": ammount,
            "no_of_ticket": no_of_ticket
        })

        # Publish message
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=message
        )

        # Close connection
        connection.close()

        print(f"📤 Sent booking message: {message}")
    except Exception as e:
        print(f"❌ Error publishing to RabbitMQ: {e}")

@app.post("/bookings/")
def create_booking(
    booking: BookingCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)  # ✅ Get user ID from token
    
    # ✅ Check if event exists before booking
    event_data = check_event_exists(booking.event_id)
    
    new_booking = Booking(
        event_id=booking.event_id,
        amount=booking.amount,
        num_tickets=booking.num_tickets,
        user_id=user_id
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    # ✅ Send message to RabbitMQ
    publish_booking_message(user_id, booking.amount, booking.num_tickets)

    return {"message": "Booking successful", "booking_id": new_booking.id, "event": event_data}

# ✅ GET Endpoint to Fetch User's Bookings
@app.get("/bookings/")
def get_user_bookings(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return {"user_id": user_id, "bookings": bookings}