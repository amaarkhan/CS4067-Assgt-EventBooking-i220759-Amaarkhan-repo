from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Initialize FastAPI
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# ✅ Create Database Tables
Base.metadata.create_all(bind=engine)


# ✅ Booking Model (Table)
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    num_tickets = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)  # No ForeignKey constraint


# ✅ Pydantic Schema for Request Body
class BookingCreate(BaseModel):
    event_id: int
    amount: float
    num_tickets: int


# ✅ Function to Verify JWT Token & Extract User ID
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")  # Extract `id` from JWT
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ✅ POST Endpoint to Create a Booking
@app.post("/bookings/")
def create_booking(
    booking: BookingCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)  # ✅ Get user ID from token

    new_booking = Booking(
        event_id=booking.event_id,
        amount=booking.amount,
        num_tickets=booking.num_tickets,
        user_id=user_id
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {"message": "Booking successful", "booking_id": new_booking.id}


# ✅ GET Endpoint to Fetch User's Bookings
@app.get("/bookings/")
def get_user_bookings(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()

    return {"user_id": user_id, "bookings": bookings}

