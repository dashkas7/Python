from fastapi import FastAPI, Depends
import uvicorn
from routers import default_router, users_router, quizes_router

app = FastAPI()

app.include_router(default_router)
app.include_router(users_router)
app.include_router(quizes_router)

if __name__=='__main__':
    uvicorn.run("main:app", reload=True)