from pydantic import BaseModel
from typing import List

class QuizAdd(BaseModel):
    name: str

class QuizBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True



class QuestionBase(BaseModel):
    id:int
    question: str
    answer: str
    wrong1: str
    wrong2: str
    wrong3: str
    
    class Config:
        from_attributes = True


class QuestionAdd(BaseModel):
    question: str
    answer: str
    wrong1: str
    wrong2: str
    wrong3: str

class QuizWithQuestions(QuizBase):
    questions: list[QuestionBase] = []
