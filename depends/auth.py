
from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData
from fastapi import Security
from fastapi.security import APIKeyHeader
from fastapi import HTTPException
from starlette import status

api_key_header = APIKeyHeader(name="Authorization")

token='Token'

async def check_auth(api_key: str = Security(api_key_header)) -> WebAppInitData:
     try:
          data = safe_parse_webapp_init_data(token, api_key)
     except ValueError:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
     return data