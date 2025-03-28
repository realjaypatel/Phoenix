from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status

import database

db = database.db
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_user(email: str):
    user = db["users"].find_one({"email": email})
    if user:
        return user
    else:
        return None
    
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