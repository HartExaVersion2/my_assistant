from fastapi import FastAPI, HTTPException

app = FastAPI()

# дз в дневник ру выдано
@app.get("/event/dnevnik/homework")
async def get_events():
    return None

# оценки в дневник ру выставлены
@app.get("/event/dnevnik/marks")
async def get_events():
    return None

# "звёздочки для детей подсчитаны"
@app.get("/event/algoritmika/stars")
async def get_events():
    return None

# новое сообщение в чате алгоритмики
@app.get("/event/algoritmika/new_message")
async def get_events():
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)