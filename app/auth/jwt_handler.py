import time  #For setting expiration limit to token
import jwt #To encode and decode jwt strings
from dotenv import load_dotenv, find_dotenv
from os import environ


env_loc = find_dotenv('.env')
load_dotenv(env_loc)

JWT_SECRET = environ.get("API_SECRET_KEY")
JWT_ALGORITHM = environ.get("API_ENCODE_ALGORITHM")

#Returns the generated tokens
def token_response(token: str):
    return {
        "access_token": token
    }

#Function used for signing the JWT string
def signJWT(sub: str, clientHost : str):
    payload = {
        "sub" : sub,
        "ch" : clientHost,
        "iat" : time.time(),
        "eat" : time.time() + 86400
    }
    print(payload["iat"])
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return token_response(token)


def decode_jwt(token: str, clientHost: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        if (decoded_token["ch"] == clientHost):
            return decoded_token if decoded_token["eat"] >= time.time() else None
        else:
           print("Token Stoled")
           return None 
    except:
        return None