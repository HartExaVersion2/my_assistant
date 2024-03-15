from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from common.browser import Browser
import time
import os

browser = Browser()
driver = browser.get_driver()



def get_homework() -> str:
    with open('homework.txt', 'r') as f:
        list_homeworks = f.readlines()
        new_homework = list_homeworks[0]
    with open('homework.txt', 'w') as f:
        f.writelines(list_homeworks[1:])
    with open('used_homework.txt', 'r') as f:
        old_homeworks = f.readlines()
    with open('used_homework.txt', 'w') as f:
        f.writelines(old_homeworks)
        f.writelines(new_homework)
    return new_homework

def authorize():
    print('авторизация')
    driver.get("https://login.dnevnik.ru/login/esia/tambovskaya")
    time.sleep(5)
    element_login = driver.find_element(By.NAME, 'login')
    element_login.send_keys(os.environ.get("DnevnikRuLogin"))
    time.sleep(1)
    element_password = driver.find_element(By.NAME, 'password')
    element_password.send_keys(os.environ.get("DnevnikRuPassword"))
    element_password.send_keys(Keys.ENTER)
    time.sleep(3)


def processing_lessons_without_marks():
    print('проверка оценок')
    try:
        card_lessons_without_marks = driver.find_element(By.CSS_SELECTOR, '[data-test-id="card-lessons-without-marks-red"]')
    except:
        card_lessons_without_marks = None
    if card_lessons_without_marks is not None:
        element = driver.find_element(By.XPATH, '//*[contains(text(), "Выставить")]')
        driver.execute_script("arguments[0].click();", element)
        element = driver.find_element(By.XPATH, '//*[contains(text(), "Проведен без оценок")]')
        driver.execute_script("arguments[0].click();", element)


def processing_problem_with_homework():
    print('проверка домашки')
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
                homework_button = row.find_element(By.CSS_SELECTOR, "div._Y65k")
                driver.execute_script("arguments[0].click();", homework_button)
                time.sleep(1)
                input = row.find_element(By.CLASS_NAME, "PHvfN")
                driver.execute_script("arguments[0].click();", input)
                time.sleep(1)
                homework = get_homework()
                input.send_keys(homework)
                input.send_keys(Keys.ENTER)
                break


print('код начал выполнение')
authorize()
processing_lessons_without_marks()
processing_problem_with_homework()
print('все функции отработали')

