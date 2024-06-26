from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BROWSER, URLS
from common.browser import Browser
from common.logger import Log
from common.errors import UnknownError
from common.datamodel import WorkReports
import shutil
import requests
import time
import os

logger = Log('dnevnik_ru_writer', 'DnevnikRu/dnevnik_ru_writer.py', 'dnevnik_ru_writer')


def __send_report(error_code, text):
    try:
        report = WorkReports(error=error_code, text=text)
        json_data = report.dict()
        requests.post(URLS.CORE_API, json=json_data)
    except Exception as error:
        message = 'function {} error {}'.format(__send_report.__name__, error)
        logger.error(message)
        raise UnknownError


def __is_file_empty(file_path):
    return os.stat(file_path).st_size == 0

def __copy_file(source_file, destination_file):
    shutil.copyfile(source_file, destination_file)

def __clear_file(file_path):
    with open(file_path, 'w') as file:
        pass

def get_homework() -> str:
    try:
        if __is_file_empty('homework.txt'):
            __copy_file('used_homework.txt', 'homework.txt')
            __clear_file('used_homework.txt')
        with open('homework.txt', 'r') as f:
            list_homeworks = f.readlines()
            new_homework = list_homeworks[0].replace('\n', '')
        with open('homework.txt', 'w') as f:
            f.writelines(list_homeworks[1:])
        with open('used_homework.txt', 'r') as f:
            old_homeworks = f.readlines()
        with open('used_homework.txt', 'w') as f:
            f.writelines(old_homeworks)
            f.writelines(new_homework)
        return new_homework
    except Exception as error:
        message = 'function {} error {}'.format(get_homework.__name__, error)
        logger.error(message)
        raise UnknownError

def authorize():
    try:
        driver.get(URLS.AUTH)
        time.sleep(5)
        element_login = driver.find_element(By.NAME, 'login')
        element_login.send_keys(os.environ.get("DnevnikRuLogin"))
        time.sleep(1)
        element_password = driver.find_element(By.NAME, 'password')
        element_password.send_keys(os.environ.get("DnevnikRuPassword"))
        element_password.send_keys(Keys.ENTER)
        time.sleep(3)
    except Exception as error:
        message = 'function {} error {}'.format(authorize.__name__, error)
        logger.error(message)
        raise UnknownError


def processing_lessons_without_marks():
    try:
        try:
            card_lessons_without_marks = driver.find_element(By.CSS_SELECTOR, '[data-test-id="card-lessons-without-marks-red"]')
        except:
            card_lessons_without_marks = None
        if card_lessons_without_marks is not None:
            element = driver.find_element(By.XPATH, '//*[contains(text(), "Выставить")]')
            driver.execute_script("arguments[0].click();", element)
            element = driver.find_element(By.XPATH, '//*[contains(text(), "Проведен без оценок")]')
            driver.execute_script("arguments[0].click();", element)
    except Exception as error:
        message = 'function {} error {}'.format(processing_lessons_without_marks.__name__, error)
        logger.error(message)
        raise UnknownError


def processing_problem_with_homework():
    try:
        try:
            card_problem_with_homework = driver.find_element(By.CSS_SELECTOR, '[data-test-id="card-problems-with-homeworks-red"]')
        except:
            card_problem_with_homework = None
        if card_problem_with_homework is not None:
            element = driver.find_element(By.XPATH, '//*[contains(text(), "Выдать")]')
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
            element = driver.find_element(By.XPATH, '//*[contains(text(), "Выдать ДЗ")]')
            driver.execute_script("arguments[0].click();", element)
            time.sleep(1)
            main_window = driver.current_window_handle
            time.sleep(1)
            all_windows = driver.window_handles
            time.sleep(1)
            journal = [window for window in all_windows if window != main_window][0]
            driver.switch_to.window(journal)
            time.sleep(1)
            rows = driver.find_elements(By.CSS_SELECTOR, "tr.eYrEI")
            for row in rows:
                if "Вы не выдали ДЗ!" in row.text:
                    homework = get_homework()
                    homework_button = row.find_element(By.CSS_SELECTOR, "div._Y65k")
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", homework_button)
                    time.sleep(1)
                    input = row.find_element(By.CLASS_NAME, "PHvfN")
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", input)
                    input.send_keys(homework)
                    input.send_keys(Keys.ENTER)
                    break
    except Exception as error:
        message = 'function {} error {}'.format(processing_problem_with_homework.__name__, error)
        logger.error(message)
        raise UnknownError

try:
    logger.info('START dnevnik ru writer')
    browser = Browser(BROWSER.WINDOW_HEIGHT, BROWSER.WINDOW_WIDTH, BROWSER.HEADLESS, BROWSER.SANDBOX)
    driver = browser.get_driver()
    authorize()
    processing_lessons_without_marks()
    processing_problem_with_homework()
    __send_report(0, 'dnevnik ru writer завершил заполнение дневника')
    logger.info('END dnevnik ru writer')
except Exception as error:
    __send_report(1, 'В dnevnik ru writer произошла ошибка')
    message = 'ДневникуРу пизда. Поднимай меня. error {}'.format(error)
    logger.error(message)