import aiohttp
from sqlalchemy import exists, create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('postgresql://quiz_admin:1234@localhost/quiz')
Session = sessionmaker(bind=engine)


class QuizData(Base):
    __tablename__ = 'quiz_data'

    id = Column(Integer, primary_key=True)
    jservice_question_id = Column(Integer)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime)


def add_to_db(responce_json):
    '''Adding to database'''
    session = Session()
    for item in responce_json:
        quiz_data = QuizData(
            jservice_question_id=item['id'],
            question=item['question'],
            answer=item['answer'],
            created_at=item['created_at']
        )
        session.add(quiz_data)
        session.commit()
        session.close()


async def unique_checker(responce_json, url):
    '''Check question_id existance'''
    unique_responce = []
    session = Session()
    for item in responce_json:
        question_id_exists = session.query(
            exists().where(QuizData.jservice_question_id == item['id'])
        ).scalar()
        if question_id_exists:
            unique_question = await question_changer(url)
            unique_responce.append(unique_question)
        else:
            unique_responce.append(item)
    return unique_responce


async def question_changer(url):
    params = {'count': 1}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            new_response_json = await response.json()
    session = Session()
    question_id_exists = session.query(
        exists().where(
            QuizData.jservice_question_id == new_response_json[0]['id']
        )
    ).scalar()
    session.close()
    if question_id_exists:
        return await question_changer(url)
    return new_response_json[0]
