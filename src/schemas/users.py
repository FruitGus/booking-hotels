from pydantic import BaseModel, ConfigDict, EmailStr



class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str = ""
    last_name: str = ""



class UserRequestLogin(BaseModel):
    email: EmailStr
    password: str



class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str = ""
    last_name: str = ""


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

