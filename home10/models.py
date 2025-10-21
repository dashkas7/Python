from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


quiz_question = Table(
    "quiz_question",
    Base.metadata,
    Column("quiz_id", Integer, ForeignKey("quiz.id"), primary_key=True),
    Column("question_id", Integer, ForeignKey("question.id"), primary_key=True),
)

class QuizOrm(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


    questions = relationship(
        "QuestionOrm",
        secondary=quiz_question,
        back_populates="quizzes",
        lazy="selectin" 
    )


class QuestionOrm(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    question = Column(String(250), nullable=False)
    answer   = Column(String(100), nullable=False)
    wrong1   = Column(String(100), nullable=False)
    wrong2   = Column(String(100), nullable=False)
    wrong3   = Column(String(100), nullable=False)
    
    
    quizzes = relationship(
        "QuizOrm",
        secondary=quiz_question,
        back_populates="questions"
    )
