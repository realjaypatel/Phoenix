from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status,Query
import json
import database
import utils
import pandas as pd
import numpy as np
templates = Jinja2Templates(directory="templates")
import requests













router = APIRouter(
    # prefix='/',
    tags=['home']
)


@router.get('/', status_code=status.HTTP_200_OK)
async def return_home(request: Request):
    user = utils.Validate_User(request)
    print('user :',user)
    if user['status'] != 'pass':
        user = {'data':{'name':'Sign In'} }     
    data2 = requests.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
    # print('fetched data2 :',data2)
    data2 = data2.json()

               

    return templates.TemplateResponse("home.html", {"request": request,"user":user['data'],"data":data2})



