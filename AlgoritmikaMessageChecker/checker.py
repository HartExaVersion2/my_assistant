from common.browser import Browser
from common.logger import Log
from common.errors import UnknownError
from common.datamodel import WorkReports
from config import BROWSER, URLS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import requests

logger = Log('checker', 'AlgoritmikaMessageChecker/checker.py', 'checker')


def __send_report(error_code, text):
    try:
        report = WorkReports(error=error_code, text=text)
        json_data = report.json_data.dict()
        requests.post(URLS.CORE_API, json=json_data)
    except Exception as error:
        message = 'function {} error {}'.format(__send_report.__name__, error)
        logger.error(message)
        raise UnknownError


def authorize(login, password, driver):
    try:
        driver.get(URLS.AUTH)
        driver.set_window_size(1024, 768)

        element_login = driver.find_element(By.ID, 'login')
        element_login.send_keys(login)
        element_login.send_keys(Keys.ENTER)
        time.sleep(1)
        element_password = driver.find_element(By.ID, 'password')
        element_password.send_keys(password)
        element_password.send_keys(Keys.ENTER)
        time.sleep(5)
    except Exception as error:
        message = 'function {} error {}'.format(authorize.__name__, error)
        logger.error(message)
        raise UnknownError


def check_messages(driver) -> bool:
    try:
        driver.get(URLS.CLOSEST_LESSON)
        time.sleep(1)
        counter = driver.find_element(By.CSS_SELECTOR, "div.algo-journal-counter")
        if counter.text != '' and int(counter.text) > 0:
            return True
        else:
            return False
    except Exception as error:
        message = 'function {} error {}'.format(check_messages.__name__, error)
        logger.error(message)
        raise UnknownError

try:
    logger.info('START checker.py')
    names = ['КаринОчка', 'Прилепский']
    logins = [os.environ.get("AlgKarenLogin"), os.environ.get("AlgDimLogin")]
    passwords = [os.environ.get("AlgKarenPassword"), os.environ.get("AlgDimPassword")]
    for i in range(len(logins)):
        browser = Browser(BROWSER.WINDOW_HEIGHT, BROWSER.WINDOW_WIDTH, BROWSER.HEADLESS, BROWSER.SANDBOX)
        driver = browser.get_driver()
        authorize(logins[i], passwords[i], driver)
        if check_messages(driver):
            __send_report(error_code=0, text='{}. У вас новое сообщение на платформе!'.format(names[i]))
        browser.close()
    logger.info('END checker.py')
    report = WorkReports(error=0, text='У вас новое сообщение на платформе!')
except Exception as error:
    __send_report(error_code=1, text='В приложении checker произошла ошибка!')
    logger.error('checker.py error {}'.format(error))

