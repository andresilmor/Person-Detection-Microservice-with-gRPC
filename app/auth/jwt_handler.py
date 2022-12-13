import time  #For setting expiration limit to token
import jwt #To encode and decode jwt strings
from dotenv import load_dotenv, find_dotenv
from os import environ


env_loc = find_dotenv('.env')
load_dotenv(env_loc)

JWT_SECRET = environ.get("API_SECRET_KEY").replace("||", "\n")
#Public b'-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAOk5Q87k5Cgy9P/ixQfckkRFGCzP/jOSC/tS/h9czXcY=\n-----END PUBLIC KEY-----\n'
JWT_ALGORITHM = environ.get("API_ENCODE_ALGORITHM")

#Returns the generated tokens
def token_response(token: str):
    return {
        "access_token": token
    }

#Function used for signing the JWT string
def signJWT(sub: str):
    payload = {
        "sub" : sub,
        "iat" : time.time(),
        "eat" : time.time() + 7200
    }

    token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token_response(token)


async def decode_jwt(token: str):
    try:
        print(token)
        decoded_token =  jwt.decode(jwt=token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token if decoded_token["eat"] >= time.time() else None
    
    except:
        print("Failed the try of decode_jwt")
        return None