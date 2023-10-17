## Quizzes
Веб-сервис, создающий загадки.
Реализован на FastAPI+ SQLAlchemy + PostgreSQL.
Запускается в docker-compose.
Сохранность данных обеспечивается с помощью volume'а.

### Инструкция по запуску:
1. В директории с docker-compose.yml выполнить `docker-compose up -d`
2. Найти контейнер с `quizzes-db` с помощью команды `docker container ls`
3. Открыть терминал контейнера базы данных: `docker exec -it <container_id_or_name> bash`
4. Войти в бд: `psql -U quiz_admin -d quiz`
5. Создать таблицу:
`CREATE TABLE quiz_data (
    id SERIAL PRIMARY KEY,
    jservice_question_id INTEGER,
    question TEXT,
    answer TEXT,
    created_at TIMESTAMP
);`

### Пример запроса с локальной машины:
POST http://localhost/
Request body (JSON format):
{
"questions_num":  1
}
### Пример ответа:
{
    "question": "\"Opening Night\",\"Where Did We Go Right?\"",
    "created_at": "2022-12-30T20:05:58.219000",
    "id": 4,
    "jservice_question_id": 128464,
    "answer": "<i>The Producers</i>"
}
**Обратите внимание: ответ на первый запрос придет пустым!**