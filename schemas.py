from pydantic import BaseModel
class LoginRequest(BaseModel):
    employee_id:str
    password:str
#what the api return after login
class Token(BaseModel):
    access_token:str
    token_type:str
class PasswordUpdate(BaseModel):
    new_password:str