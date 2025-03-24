from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status, Form,Response
import json
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import Depends, FastAPI, HTTPException, status
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import database
templates = Jinja2Templates(directory="templates")
from utils import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix='/auth',
    tags=['product']
)
db = database.db





def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.get('/login', status_code=status.HTTP_200_OK)
async def return_home(request: Request):
    # print('got a req')
    return templates.TemplateResponse("auth/login.html", {"request": request,"message":''})

@router.get('/signup', status_code=status.HTTP_200_OK)
async def return_home(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request,"message":''})

@router.post("/token")
async def login_for_access_token(request:Request,email: str = Form(...), password: str = Form(...)):
    try:
        user =  db["users"].find_one({"email": email})
        if not user:
            return templates.TemplateResponse("auth/login.html", {"request": request,"message":'Incorrect username or password'})

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"data": user["email"]}, expires_delta=access_token_expires)
        response = RedirectResponse(url="/explore", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    except:
        return 'Internal Server Error (Auth)'


@router.post("/signup")
async def signup(request:Request,name: str = Form(...),email: str = Form(...), password: str = Form(...)):

    try:
        user =  db["users"].find_one({"email": email})
        if user:
            return templates.TemplateResponse("auth/signup.html", {"request": request,"message":'email already exist !'})

        hashed_password = (password)
        user = {"email": email, "password": hashed_password,"name":name}
        res = db["users"].insert_one(user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"data": user["email"]}, expires_delta=access_token_expires)
        response = RedirectResponse(url="/explore", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response      
        
        
    except:
        return 'Internal Server Error (Auth)'

@router.get("/signout")
async def signout(request:Request):
    
    response = templates.TemplateResponse("auth/login.html", {"request": request,"message":'Signout Successful!'})
    response.delete_cookie(key="access_token")
    return response