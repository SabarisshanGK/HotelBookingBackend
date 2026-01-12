# Imports
import jwt
from enums.UserRoleEnum import UserRole
from datetime import timedelta , datetime , timezone
from dotenv import load_dotenv
import os
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from fastapi import Depends , HTTPException , status

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

security = HTTPBearer()

def create_jwt_access_token(user_email: str , user_role: UserRole , expiry_delta: timedelta):
    payload = {
        "user_email": user_email,
        "user_role": user_role,
        "issuer": "Hotel booking website"
    }
    iAt = datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + expiry_delta
    payload.update(
        {
            "issueadAt": int(iAt.timestamp()),
            "expire": int(expire.timestamp())
        }
    )
    return jwt.encode(payload , SECRET_KEY , algorithm=ALGORITHM)


# Verifying token from authorization header
async def verify_token(credentials: HTTPAuthorizationCredentials =Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED , detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Token Expired")