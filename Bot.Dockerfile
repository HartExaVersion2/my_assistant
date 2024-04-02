FROM python:3.10

# установка библиотек python
RUN pip install --upgrade pip
RUN pip install pydantic
RUN pip install requests
RUN pip install fastapi
RUN pip install telebot
RUN pip install uvicorn


WORKDIR /app
RUN mkdir "common"
RUN mkdir "Bot"

COPY Core .
COPY Bot ./Bot
COPY common ./common
COPY test.py .

# run crond as main process of container
CMD python3 /app/core_api.py