from fastapi import APIRouter

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
def index():
    return {'data':'ok'}

@users_router.get('')
def index():
    return {'data':'user'}

@quizes_router.get('')
def index():
    return {'data':'quizes'}
