from fastapi import FastAPI, HTTPException
from common.datamodel import WorkReports

app = FastAPI()

# дз в дневник ру выдано
@app.post("/event/dnevnik/homework")
async def get_events(response):
    response_data = response.json()
    response_model = WorkReports.parse_obj(response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    # сообщение в бота

# оценки в дневник ру выставлены
@app.post("/event/dnevnik/marks")
async def get_events(response):
    response_data = response.json()
    response_model = WorkReports.parse_obj(response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    # сообщение в бота

# "звёздочки для детей подсчитаны"
@app.post("/event/algoritmika/stars")
async def get_events(response):
    response_data = response.json()
    response_model = WorkReports.parse_obj(response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    # сообщение в бота

# новое сообщение в чате алгоритмики
@app.post("/event/algoritmika/new_message")
async def get_events(response):
    response_data = response.json()
    response_model = WorkReports.parse_obj(response_data)
    if response_model.error == 0:
        message = response_model.text
    else:
        message = 'Ошибка сервиса: \n' + response_model.text
    # сообщение в бота

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)