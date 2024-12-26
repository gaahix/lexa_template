from aiogram.utils.web_app import WebAppInitData
from fastapi import FastAPI, HTTPException, Depends
from fastapi import Request
from depends.auth import check_auth
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    # Если делать через мидварь, то тут нужен депенд, чтобы в docs была плашка авторизации, на все методы в роуте
    dependencies=[Depends(check_auth)]
)

# Можно добавлять стейт через мидлварь
class UserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        token = request.headers.get("Authorization")
        if not token:
            raise HTTPException(status_code=401, detail="Unauthorized")
        request.state.user = await check_auth(token)
        response = await call_next(request)
        return response


app.add_middleware(UserMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Тут через мидлварь получаю значение
@app.get("/")
async def root(request: Request):
    user:WebAppInitData = getattr(request.state, "user", None)
    return user.model_dump_json()

# Тут через депенд
@app.get("/depends")
async def depends(user:WebAppInitData = Depends(check_auth)):
    return user.model_dump_json()
