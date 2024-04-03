import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
if load_dotenv():
    pass
else:
    print("env file is missing !!!!")


SECRET_KEY = os.getenv("SECRET_KEY") # configure it in .env file

def generateJwtToken(data:dict):
    jwt_token=""
    try:
        time_in_secs=60 * 60 * 24 # 1 day
        # Get the current time
        current_time = datetime.now()
        # Add one minute to the current time
        one_minute_later = current_time + timedelta(seconds=time_in_secs)
        data["exp"]=one_minute_later.timestamp()
        
        jwt_token = jwt.encode(payload=data,key=SECRET_KEY, algorithm="HS256")
        print("JWT TOKEN GENERATED will expire in {0} sec. Token : {1}".format(time_in_secs,jwt_token))
    except Exception as e:
        print("JWT CREATION Failed: ",e)
    return jwt_token

def validateJwtToken(jwt_token):
    try:
        decode_data=jwt.decode(jwt_token, SECRET_KEY, leeway=10,algorithms=["HS256"])
        if decode_data:
            return (True,"Session Authorised",decode_data)
    except jwt.ExpiredSignatureError:
        return (False,"Session has Expired",None)
    except Exception:
        return (False,"Session Unauthorised",None)
    return (False,"Session Unauthorised")

