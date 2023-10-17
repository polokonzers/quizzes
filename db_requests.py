from sqlalchemy import create_engine, Column, Integer, String, DateTime
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
