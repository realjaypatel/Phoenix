from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
import json
import database
import requests as rs
templates = Jinja2Templates(directory="templates")
import ast
import utils
router = APIRouter(
    prefix='/business',
    tags=['business']
)

data = {
    
}





@router.get('/{startup_id}', status_code=status.HTTP_200_OK)
async def return_home(startup_id,request: Request):
    user = utils.Validate_User(request)
    if user['status'] != 'pass':
        user = {'data':{'name':'Sign In'} }  
    print(startup_id)
    data = rs.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
    data = data.json()
    for json in data:
        # print(json['Id'], str(startup_id),type(json['Id']),str(json['Id']) == startup_id)
        if str(json['Id']) == str(startup_id):
            json['other_img'] =ast.literal_eval(json['other_img'])
            # print(json)
            return templates.TemplateResponse("business.html", {"request": request,"user":user['data'],"data":json})


    return 'not found'