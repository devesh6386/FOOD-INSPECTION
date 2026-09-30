#implement rbac
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from database import users_collection
from security import SECRET_KEY, ALGORITHM
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
async def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        #decode token
        payload=jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        employee_id:str=payload.get("sub")
        if employee_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
#verify user actually exist in db
    user=await users_collection.find_one({"employee_id":employee_id})
    if user is None:
        raise credentials_exception
    return user
#rbac class
class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles
    def __call__(self,user:dict=Depends(get_current_user)):
        if user.get("role")not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return user
