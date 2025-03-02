from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import os
from dotenv import load_dotenv
import logging
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

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


@app.post("/users/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        # ✅ Check if the user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # ✅ Hash the password
        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username, email=user.email, password=hashed_password)

        # ✅ Store user in the database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        print("✅ User Registered:", db_user.email)  # Debugging log
        return {"message": "User registered successfully"}
    
    except HTTPException as e:
        raise e  # ✅ Properly return the "User already exists" error
    
    except Exception as e:
        db.rollback()
        print("❌ Error Registering User:", str(e))  # Debugging log
        raise HTTPException(status_code=500, detail="Registration failed")


@app.post("/users/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        logging.warning(f"Invalid login attempt: {user.email}")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_data = {"sub": db_user.email, "id": db_user.id}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    logging.info(f"User logged in: {user.email}")
    return {"access_token": token, "token_type": "bearer"}



# Function to Verify JWT Token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")



@app.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"id": user.id, "username": user.username, "email": user.email}


# start command uvicorn main:app --host 0.0.0.0 --port 8000 --reload
