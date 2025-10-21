from fastapi import APIRouter, HTTPException
from repositories import QuizRepository, QuestionRepository
from shemas import QuizAdd, QuizBase, QuizWithQuestions, QuestionAdd, QuestionBase
from typing import List

router = APIRouter()


@router.get("/quizes", response_model=List[QuizBase])
async def get_quizes():
    quizes = await QuizRepository.get_quizes()
    return [QuizBase.model_validate(q) for q in quizes]


@router.post("/quizes", response_model=QuizBase)
async def create_quiz(quiz: QuizAdd):
    quiz_id = await QuizRepository.add_quiz(quiz)
    new_quiz = await QuizRepository.get_quiz(quiz_id)
    if not new_quiz:
        raise HTTPException(status_code=404, detail="Ошибка при создании квиза")
    return QuizBase.model_validate(new_quiz)


@router.get("/quizes/{quiz_id}", response_model=QuizBase)
async def get_quiz(quiz_id: int):
    quiz = await QuizRepository.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Квиз не найден")
    return QuizBase.model_validate(quiz)


@router.get("/quizes/{quiz_id}/questions", response_model=QuizWithQuestions)
async def get_quiz_questions(quiz_id: int):
    quiz = await QuizRepository.get_quiz(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Квиз не найден")
    return QuizWithQuestions.model_validate(quiz)


@router.post("/quizes/{quiz_id}/link")
async def link_questions_to_quiz(quiz_id: int, question_ids: List[int]):
    linked_ids = await QuizRepository.link_questions_to_quiz(quiz_id, question_ids)
    if not linked_ids:
        raise HTTPException(status_code=404, detail="Квиз или вопросы не найдены")
    return {"linked_questions": linked_ids}


@router.get("/questions", response_model=List[QuestionBase])
async def get_questions():
    questions = await QuestionRepository.get_questions()
    return [QuestionBase.model_validate(q) for q in questions]


@router.post("/questions", response_model=QuestionBase)
async def create_question(question: QuestionAdd):
    q_id = await QuestionRepository.add_question(question)
    new_q = await QuestionRepository.get_question(q_id)
    if not new_q:
        raise HTTPException(status_code=404, detail="Ошибка при создании вопроса")
    return QuestionBase.model_validate(new_q)


@router.get("/questions/{question_id}", response_model=QuestionBase)
async def get_question(question_id: int):
    q = await QuestionRepository.get_question(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return QuestionBase.model_validate(q)
