from fastapi import APIRouter, Depends
from database import UserRepository as ur 
from models import UserFilter
from shemas import *

default_router = APIRouter()

users_router = APIRouter(
    prefix="/users",
    tags=["Квизы"]
)
quizes_router = APIRouter(
    prefix="/quizes",
    tags=["Квизы"]
)

@default_router.get('/', tags=['API V1'])
async def index():
    return {'data':'ok'}



@users_router.get('')
async def users_get() -> list[User]: #dict[str:list[User] | str]
    users = await ur.get_users()
    # return {'data': users}
    return users

@users_router.get('/{id}')
async def user_get(id:int) -> User: #возвр одного польз-ля
    user = await ur.get_user(id)
    if user:
        return {'data': user}
    raise HTTPException(status_code=404, detail="User not found")
 # или return {'err':"User not found, ..."} # но тогда get_user(id) -> User | dict[str,str] 


@users_router.post('')
async def add_user(user:UserAdd=Depends()) -> dict[str,UserId]:
    id = await ur.add_user(user)
    return{'id': id}





@quizes_router.get('')
async def index():
    return {'data':'quizes'}
