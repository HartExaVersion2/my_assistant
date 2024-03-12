FROM python:3.10

# Установка необходимых пакетов
RUN apt-get update && apt-get -y install wget gnupg
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get -y install google-chrome-stable

# Установка ChromeDriver
RUN mkdir "chromedriver" \
    && cd chromedriver \
    && wget -q https://storage.googleapis.com/chrome-for-testing-public/122.0.6261.111/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && cd chromedriver-linux64 \
    && mv chromedriver /usr/bin/ \
    && chmod +x /usr/bin/chromedriver \
    && cd .. \
    && rm chromedriver-linux64.zip

# установка библиотек python
RUN pip install --upgrade pip
RUN pip install selenium

# установкак cron
RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY cronfile /etc/cron.d/crontab
COPY . /app

RUN chmod 0644 /etc/cron.d/crontab

# run crond as main process of container
CMD cron && python3 /app/checker.py