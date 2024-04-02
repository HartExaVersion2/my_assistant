from fastapi import FastAPI, HTTPException
from common.datamodel import WorkReports
from Bot.assistant_bot import send_message_to_user
from pydantic import parse_obj_as

app = FastAPI()

# дз в дневник ру выдано
@app.post("/event/dnevnik/homework")
async def get_events(request: WorkReports):
    response_data = request.dict()
    response_model = parse_obj_as(WorkReports, response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    send_message_to_user(message)

# оценки в дневник ру выставлены
@app.post("/event/dnevnik/marks")
async def get_events(request: WorkReports):
    response_data = request.dict()
    response_model = parse_obj_as(WorkReports, response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    send_message_to_user(message)

# "звёздочки для детей подсчитаны"
@app.post("/event/algoritmika/stars")
async def get_events(request: WorkReports):
    response_data = request.dict()
    response_model = parse_obj_as(WorkReports, response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    send_message_to_user(message)

# новое сообщение в чате алгоритмики
@app.post("/event/algoritmika/new_message")
async def get_events(request: WorkReports):
    response_data = request.dict()
    response_model = parse_obj_as(WorkReports, response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    send_message_to_user(message)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)