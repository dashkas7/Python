from sqlalchemy import select
from database import new_session, engine, Base
from models import QuizOrm, QuestionOrm
from shemas import QuizAdd, QuestionAdd


class DataRepository:
    @classmethod
    async def create_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def delete_table(cls):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @classmethod
    async def add_test_data(cls):
        async with new_session() as session:
            try:
                quizzes = [
                    QuizOrm(name="Quiz 1"),
                    QuizOrm(name="Quiz 2"),
                ]

                questions = [
                    QuestionOrm(
                        question="Сколько будет 2+2*2?", answer="6",
                        wrong1="8", wrong2="2", wrong3="4"
                    ),
                    QuestionOrm(
                        question="Столица Франции?", answer="Париж",
                        wrong1="Лондон", wrong2="Берлин", wrong3="Рим"
                    )
                ]

                quizzes[0].questions.append(questions[0])
                quizzes[1].questions.append(questions[1])

                session.add_all(quizzes + questions)
                await session.commit()
            except Exception as e:
                print("Ошибка при добавлении тестовых данных:", e)
                raise


class QuizRepository:
    @classmethod
    async def add_quiz(cls, quiz: QuizAdd) -> int:
        async with new_session() as session:
            try:
                obj = QuizOrm(name=quiz.name)  # только поле name
                session.add(obj)
                await session.flush()
                await session.commit()
                return obj.id
            except Exception as e:
                print("Ошибка при создании квиза:", e)
                raise

    @classmethod
    async def get_quizes(cls, limit: int = 10, offset: int = 0) -> list[QuizOrm]:
        async with new_session() as session:
            res = await session.execute(select(QuizOrm).limit(limit).offset(offset))
            return res.scalars().all()

    @classmethod
    async def get_quiz(cls, id: int) -> QuizOrm | None:
        async with new_session() as session:
            res = await session.execute(select(QuizOrm).where(QuizOrm.id == id))
            return res.scalars().first()

    @classmethod
    async def link_questions_to_quiz(cls, quiz_id: int, question_ids: list[int]) -> list[int]:
        async with new_session() as session:
            quiz = await session.get(QuizOrm, quiz_id)
            if not quiz:
                return []

            res = await session.execute(select(QuestionOrm).where(QuestionOrm.id.in_(question_ids)))
            questions = res.scalars().all()

            for q in questions:
                if q not in quiz.questions:
                    quiz.questions.append(q)

            await session.commit()
            return [q.id for q in questions]


class QuestionRepository:
    @classmethod
    async def add_question(cls, question: QuestionAdd) -> int:
        async with new_session() as session:
            try:
                obj = QuestionOrm(**question.model_dump())
                session.add(obj)
                await session.flush()
                await session.commit()
                return obj.id
            except Exception as e:
                print("Ошибка при создании вопроса:", e)
                raise

    @classmethod
    async def get_questions(cls, limit: int = 10, offset: int = 0) -> list[QuestionOrm]:
        async with new_session() as session:
            res = await session.execute(select(QuestionOrm).limit(limit).offset(offset))
            return res.scalars().all()

    @classmethod
    async def get_question(cls, id: int) -> QuestionOrm | None:
        async with new_session() as session:
            res = await session.execute(select(QuestionOrm).where(QuestionOrm.id == id))
            return res.scalars().first()
