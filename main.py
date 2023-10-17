import aiohttp
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
Base = declarative_base()

JSERVICE_ENPOINT = "https://jservice.io/api/random/"


class UserQuizRequest(BaseModel):
    # Typization of request body
    questions_num: int


class QuizData(Base):
    __tablename__ = 'quiz_data'

    quiz_id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime)


app = FastAPI()
engine = create_engine('postgresql://quiz_admin:1234@localhost/quiz')
Session = sessionmaker(bind=engine)


@app.post("/")
async def root(user_quiz_request: UserQuizRequest):
    url = JSERVICE_ENPOINT
    params = {
        'count': user_quiz_request.questions_num
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as responce:
            responce_json = await responce.json()
            session = Session()
            for item in responce_json:
                quiz_data = QuizData(
                    quiz_id=item['id'],
                    question=item['question'],
                    answer=item['answer'],
                    created_at=item['created_at']
                )
                session.add(quiz_data)
            session.commit()
            session.close()
            # Here we need to return to user a last question from DB
            return responce_json
