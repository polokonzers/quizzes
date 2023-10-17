import aiohttp
from fastapi import FastAPI
from pydantic import BaseModel
import db_requests

JSERVICE_ENPOINT = "https://jservice.io/api/random/"


class UserQuizRequest(BaseModel):
    # Typization of request body
    questions_num: int


app = FastAPI()


@app.post("/")
async def root(user_quiz_request: UserQuizRequest):
    '''Handling user workflow'''
    url = JSERVICE_ENPOINT
    params = {
        'count': user_quiz_request.questions_num
    }
    responce_json = await jservice_request(url, params)
    db_requests.add_to_db(responce_json)
    previous_question = db_requests.pull_question(responce_json)
    print(responce_json)
    return previous_question


async def jservice_request(url, params):
    '''Request to jservice with changing not unique questions'''
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as responce:
            responce_json = await responce.json()
            validated_responce = await db_requests.unique_checker(
                responce_json,
                url
            )
            return validated_responce
