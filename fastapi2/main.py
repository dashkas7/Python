from fastapi import FastAPI, Depends
import uvicorn

from contextlib import asynccontextmanager
from routers import default_router, users_router, quizes_router
from database import DataRepository as dr

@asynccontextmanager # реагирует на  методы __aenter__() и __aexit__()
async def lifespan(app: FastAPI):
    await dr.create_table()
    await dr.add_test_data()
    print("------Bases build-------------")
    
    yield
    await dr.delete_table()
    print("-------------Bases drooped------------")

app = FastAPI(lifespan=lifespan)

app.include_router(default_router)
app.include_router(users_router)
app.include_router(quizes_router)

if __name__=='__main__':
    uvicorn.run("main:app", reload=True)