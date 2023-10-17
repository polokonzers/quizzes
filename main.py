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
    url = JSERVICE_ENPOINT
    params = {
        'count': user_quiz_request.questions_num
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as responce:
            responce_json = await responce.json()
            db_requests.add_to_db(responce_json)
            # Here we need to return to user a last question from DB
            return responce_json
