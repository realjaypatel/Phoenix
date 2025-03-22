from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your_secret_key"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# from motor.motor_asyncio import AsyncIOMotorClient
# client = AsyncIOMotorClient("mongodb+srv://user:user@cluster0.u3fdtma.mongodb.net/Master")
# db = client["your_database_name"]
import pymongo
client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.u3fdtma.mongodb.net/Master")
db = client["your_database_name"]

def get_user(email: str):
    user = db["users"].find_one({"email": email})
    if user:
        return user
    else:
        return None
    
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def Validate_User(request):
    token = request.state.token
    # print('validate_user',token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print('payload',payload)
        email = payload['data']
        # print('email',email)
        if email is None:
            return {'status':'fail','data':credentials_exception} 
    except :
        return {'status':'fail','data':credentials_exception} 
    user = get_user(email)
    if user == None:
        return {'status':'fail','data':credentials_exception} 
    return {'status':'pass','data':user} 