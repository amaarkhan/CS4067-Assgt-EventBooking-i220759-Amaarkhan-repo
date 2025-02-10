from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Initialize FastAPI
app = FastAPI()

# Set up logging
logging.basicConfig(filename="user_service.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create Database Tables
Base.metadata.create_all(bind=engine)

# User Model (Table)
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Pydantic Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Register User
@app.post("/users/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logging.info(f"User registered: {user.email}")
        return {"message": "User registered successfully"}
    except:
        db.rollback()
        logging.error(f"User registration failed: {user.email}")
        raise HTTPException(status_code=400, detail="User already exists")

# Login User & Return JWT Token
@app.post("/users/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        logging.warning(f"Invalid login attempt: {user.email}")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_data = {"sub": db_user.email}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    logging.info(f"User logged in: {user.email}")
    return {"access_token": token, "token_type": "bearer"}

# Get User Profile (Requires Authentication)
@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        logging.warning(f"User not found: ID {id}")
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}
