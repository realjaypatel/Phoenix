from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status, Form,Response
import json
from fastapi.responses import JSONResponse

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
    print('got a req')
    return templates.TemplateResponse("auth/login.html", {"request": request})

@router.get('/signup', status_code=status.HTTP_200_OK)
async def return_home(request: Request):
    return templates.TemplateResponse("auth/signup.html", {"request": request})

# @router.post("/token", response_model=Token)
# async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await db["users"].find_one({"email": form_data.username})
#     if not user or not verify_password(form_data.password, user["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token({"data": user["email"]}, expires_delta=access_token_expires)
#     response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
#     response.set_cookie(key="access_token", value=access_token, httponly=True)
#     return response


@router.post("/token")
async def login_for_access_token(email: str = Form(...), password: str = Form(...)):
    print('got a token req')
    user = await db["users"].find_one({"email": email})
    print('founded user:',user )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"data": user["email"]}, expires_delta=access_token_expires)
    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
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
        print('payload',payload)
        email = payload['data']
        print('email',email)
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
async def signup(name: str = Form(...),email: str = Form(...), password: str = Form(...)):
    # hashed_password = (password)
    # user = {"email": email, "password": hashed_password}
    # res = await db["users"].insert_one(user)
    # return JSONResponse(status_code=201, content={"id": str(res.inserted_id), "email": email})
    # print('got a token req')
    try:
        user = await db["users"].find_one({"email": email})
        if user:
            return 'email already exist'
        hashed_password = (password)
        user = {"email": email, "password": hashed_password,"name":name}
        res = await db["users"].insert_one(user)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token({"data": user["email"]}, expires_delta=access_token_expires)
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response      
        
        
    except:
        return 'Internal Server Error'



@router.get("/signout")
async def signout():
    response = JSONResponse(content={"message": "Successfully signed out"})
    response.delete_cookie(key="access_token")
    return response

# SECRET_KEY = "your_secret_key"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(BaseModel):
#     email: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt



# @router.post("/signup")
# async def signup(email: str = Form(...), password: str = Form(...)):
#     print('got a req /signup',email,password)
#     hashed_password = get_password_hash(password)
#     user = {"email": email, "password": hashed_password}
#     res = await db["users"].insert_one(user)
#     return JSONResponse(status_code=201, content={"id": str(res.inserted_id), "email": email})

# @router.post("/token", response_model=Token)
# async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await db["users"].find_one({"email": form_data.username})
#     if not user or not verify_password(form_data.password, user["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user["email"]}, expires_delta=access_token_expires
#     )
#     response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/users/me")
# async def read_users_me(token: str = Depends(oauth2_scheme)):
    
#     print('/me',token)
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except jwt.PyJWTError:
#         raise credentials_exception
#     user = await db["users"].find_one({"email": email})
#     if user is None:
#         raise credentials_exception
#     return user


# # @app.get("/users/me")
# # async def read_users_me(token: str = Depends(oauth2_scheme)):
# #     credentials_exception = HTTPException(
# #         status_code=status.HTTP_401_UNAUTHORIZED,
# #         detail="Could not validate credentials",
# #         headers={"WWW-Authenticate": "Bearer"},
# #     )
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         email: str = payload.get("sub")
# #         if email is None:
# #             raise credentials_exception
# #     except jwt.PyJWTError:
# #         raise credentials_exception
# #     user = await db["users"].find_one({"email": email})
# #     if user is None:
# #         raise credentials_exception
# #     return user