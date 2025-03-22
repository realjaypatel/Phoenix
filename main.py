from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from routers import business, home,auth,explore
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()
@app.middleware("http")
async def extract_token_from_cookie(request: Request, call_next):
    token = request.cookies.get("access_token")
    # print('token :', token)
    if token:
        request.state.token = token
    else:
        request.state.token = None
    response = await call_next(request)
    return response
app.mount("/static", StaticFiles(directory="static"), name="static")




@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(home.router)
app.include_router(business.router)
app.include_router(auth.router)
app.include_router(explore.router)
app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error/404.html", {"request": request}, status_code=404)

app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error/500.html", {"request": request}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=5000,reload=True)