from fastapi import FastAPI, Request, status
from routers import business, home,auth,explore
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", port=5000,reload=True)