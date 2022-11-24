import time  #For setting expiration limit to token
import jwt #To encode and decode jwt strings
from dotenv import load_dotenv, find_dotenv
from os import environ


env_loc = find_dotenv('.env')
load_dotenv(env_loc)

JWT_SECRET = b'-----BEGIN PRIVATE KEY-----\nMC4CAQAwBQYDK2VwBCIEIGlfZfr9xSxgimnEy28wCkcoxuZSB8pGmJMDgKust1oW\n-----END PRIVATE KEY-----\n'
#Public b'-----BEGIN PUBLIC KEY-----\nMCowBQYDK2VwAyEAOk5Q87k5Cgy9P/ixQfckkRFGCzP/jOSC/tS/h9czXcY=\n-----END PUBLIC KEY-----\n'
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
        "eat" : time.time() + 7200
    }

    token = jwt.encode(payload=payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    print(token)

    return token_response(token)


async def decode_jwt(token: str, clientHost):
    try:
        print("3")
        print(token)
        print(JWT_ALGORITHM)
        print(JWT_SECRET)
        decoded_token = await jwt.decode(jwt=token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        print("4")
        print(decoded_token)
        
        print(token)
        print(decoded_token["eat"])
        print(time.time())
        print(decoded_token["eat"] >= time.time())
        if (decoded_token["ch"] == clientHost):
        #if (True):
            return decoded_token if decoded_token["eat"] >= time.time() else None
        else:
            return None 
    except:
        print()
        print("Failed the try of decode_jwt")
        return None