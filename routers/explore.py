from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status,Query
import json
import database
import requests as rs
templates = Jinja2Templates(directory="templates")
import ast
import requests as rq
import utils
router = APIRouter(
    prefix='/explore',
    tags=['business']
)







# @router.get('/{search_name}', status_code=status.HTTP_200_OK)
# async def return_home(search_name,request: Request):
    
#     user = utils.Validate_User(request)
#     if user['status'] != 'pass':
#         user = {'data':{'name':'Sign In'} }   
#     data = rq.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
#     data = data.json()
#     if not search_name:        
#         return templates.TemplateResponse("explore.html", {"request": request,"user":user['data'],"data":data})
#     else:
#         search_result = []
#         for value in data:
#             if search_name.lower() in value['Title'].lower():
#                 search_result.append(value)
#         # return templates.TemplateResponse("explore.html", {"request": request,"data":search_result})
#         return templates.TemplateResponse("explore.html", {"request": request,"user":user['data'],"data":search_result})

    


@router.get('/{search_name}', status_code=status.HTTP_200_OK)
async def return_home(search_name,request: Request,p: int = Query(1, alias="p")):
    page_size = 20
    skip = (p - 1) * page_size
    limit = page_size

    user = utils.Validate_User(request)
    if user['status'] != 'pass':
        user = {'data':{'name':'Sign In'} }   
    data = rq.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
    data = data.json()
    search_result = []
    for value in data:
        if search_name.lower() in value['Title'].lower():
            search_result.append(value)
    search_result = search_result[skip:skip+limit]
    return templates.TemplateResponse("explore.html", {"request": request,"user":user['data'],"data":search_result})
    
    

@router.get('/categories/{category}', status_code=status.HTTP_200_OK)
async def return_home(request: Request,category,p: int = Query(1, alias="p")):
    page_size = 20
    skip = (p - 1) * page_size
    limit = page_size
    user = utils.Validate_User(request)
    if user['status'] != 'pass':
        user = {'data':{'name':'Sign In'} }   
    data = rq.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
    data = data.json()
    if not category:
        return templates.TemplateResponse("explore.html", {"request": request,"data":data})
    else:
        search_result = []
        for value in data:
            if category.lower() in value['Category'].lower():
                search_result.append(value)

        search_result = search_result[skip:skip+limit]
        return templates.TemplateResponse("explore.html", {"request": request,"user":user['data'],"data":search_result})

@router.get('/', status_code=status.HTTP_200_OK)
async def return_home(request: Request,p: int = Query(1, alias="p")):
    page_size = 20
    skip = (p - 1) * page_size
    limit = page_size
    
    user = utils.Validate_User(request)
    if user['status'] != 'pass':
        user = {'data':{'name':'Sign In'} }   
    data = rq.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
    data = data.json()       
    data = data[skip:skip+limit]
    return templates.TemplateResponse("explore.html", {"request": request,"user":user['data'],"data":data})
    






