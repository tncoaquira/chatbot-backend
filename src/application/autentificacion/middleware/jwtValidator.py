from datetime import datetime, timezone
import jwt
from src.config.chatbot import Config
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

logger = logging.getLogger(__name__)
def decodeJwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        exp_datetime = datetime.fromtimestamp(decoded_token["exp"], tz=timezone.utc)
        return decoded_token if exp_datetime >= datetime.now(timezone.utc) else None
    except Exception as e:
        logger.error(f"Error al decodificar el token: {e} ")
        return None
    
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        print(jwtoken,"_______________")
        isTokenValid: bool = False

        try:
            payload = decodeJwt(jwtoken)
        except :
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid