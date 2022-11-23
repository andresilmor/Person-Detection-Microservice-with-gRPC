from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,  HTTPAuthorizationCredentials
from .jwt_handler import decode_jwt

from strawberry.types import Info

class jwtBearer(HTTPBearer):
    
    def __init__(self, auto_Error : bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_Error)

    async def __call__(self, request : Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.schema == "Bearer":
                raise HTTPException(status_code = 403, detail= "Invalid or Expired Token")
            return credentials.credentials
        else: 
            raise HTTPException(status_code = 403, detail= "Invalid or Expired Token")

    async def verify_jwt(self, info : Info):
        isTokenValid : bool = False
        print(info.context['request'].client.host)
        print(info.context['request'].headers['Authorization'])
        payload = await decode_jwt(info.context['request'].headers['Authorization'])
        print("Payload: " + str(payload))
        if payload:
            isTokenValid = True
        return isTokenValid
        
async def authorizationRequired(info : Info, func):
    print("1")
  
    print(jwtBearer().verify_jwt(info=info))
    if jwtBearer().verify_jwt(info=info):
        return await func()
    else:
        return None
  