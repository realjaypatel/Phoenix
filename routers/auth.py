from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status, Form,Response
import json
from fastapi.responses import JSONResponse, RedirectResponse

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix='/auth',
    tags=['product']
)
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb+srv://user:user@cluster0.u3fdtma.mongodb.net/Master")
db = client["your_database_name"]



SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(email: str):
    user = db["users"].find_one({"email": email})
    if user:
        return user
    else:
        return None



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
    user = await db["users"].find_one({"email": email})
    if not user:
        return templates.TemplateResponse("auth/login.html", {"request": request,"message":'Incorrect username or password'})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"data": user["email"]}, expires_delta=access_token_expires)
    response = RedirectResponse(url="/explore", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


def Validate_User(request):
    token = request.state.token
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
    
@router.get("/page1")
async def read_page1(request:Request):
    User = Validate_User(request)
    print(User)
    if User['status'] =='fail':
        return User['data']
    
    return {"message": "Welcome to Page 1!"}



@router.post("/signup")
async def signup(request:Request,name: str = Form(...),email: str = Form(...), password: str = Form(...)):
    try:
        user = await db["users"].find_one({"email": email})
        if user:
            return templates.TemplateResponse("auth/signup.html", {"request": request,"message":'email already exist !'})

        hashed_password = (password)
        user = {"email": email, "password": hashed_password,"name":name}
        res = await db["users"].insert_one(user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"data": user["email"]}, expires_delta=access_token_expires)
        response = RedirectResponse(url="/explore", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response      
        
        
    except:
        return 'Internal Server Error'



@router.get("/signout")
async def signout(request:Request):
    
    response = templates.TemplateResponse("auth/login.html", {"request": request,"message":'Signout Successful!'})
    response.delete_cookie(key="access_token")
    return response