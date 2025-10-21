from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name:str
    age: int | None = None
    
@app.get('/',tags=['inDex get'] )
def home(f:str='123', q:str=None):
    return{'status':'success', "data":'data1', 'f':f, 'q':q}

@app.post('/',tags=['inDex post'] )
def home(user: User = Depends()):
    print(user)
    return{"status":"success post", "data": {'id':1, 'user':f'{user.name} {user.age}'}}



if __name__=='__main__':
    uvicorn.run("main:app", reload=True)

