from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('postgresql://quiz_admin:1234@localhost/quiz')
Session = sessionmaker(bind=engine)


class QuizData(Base):
    __tablename__ = 'quiz_data'

    quiz_id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime)
