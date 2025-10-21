from pydentic import BaseModel, ConfigDict

# USER

class UserAdd (BaseModel):
    name: str
    age:int
    phone: str|None =   None
    
    
class User (UserAdd):
    id:int
    
    model_config = ConfigDict(from_attributes=True)
 

class userID(BaseModel):
    id:int

