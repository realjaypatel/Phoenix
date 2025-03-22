from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status,Query
import json
import database
import utils
import pandas as pd
import numpy as np
templates = Jinja2Templates(directory="templates")














router = APIRouter(
    # prefix='/',
    tags=['home']
)


@router.get('/', status_code=status.HTTP_200_OK)
async def return_home(request: Request):
    user = utils.Validate_User(request)
    print("user",user)
    # if 'name' not in user.keys():
    #     user['name'] = 'Unknown Name'
    if user['status'] != 'pass':
        user = {
            
            'data':{
            
            'name':'Sign In'
        } 
        } 
               

    return templates.TemplateResponse("home.html", {"request": request,"user":user['data']})

@router.get('/api', status_code=status.HTTP_200_OK)
async def return_home2(request: Request):
    user = utils.Validate_User(request)
    print("user",user)
    # if 'name' not in user.keys():
    #     user['name'] = 'Unknown Name'
    if user['status'] != 'pass':
        user = {
            
            'data':{
            
            'name':'Sign In'
        } 
        } 
               

    return templates.TemplateResponse("product.html", {"request": request,"user":user['data']})



