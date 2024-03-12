from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import math
import os

driver = webdriver.Chrome()

driver.get("https://lms.algoritmika.org/auth/v3/login#group-closest-lesson")
driver.set_window_size(1024, 768)

element_login = driver.find_element(By.ID, 'login')
element_login.send_keys(os.environ.get("AlgDimLogin"))
element_login.send_keys(Keys.ENTER)
time.sleep(1)
element_password = driver.find_element(By.ID, 'password')
element_password.send_keys(os.environ.get("AlgDimPassword"))
element_password.send_keys(Keys.ENTER)
time.sleep(5)
driver.get("https://lms.algoritmika.org/group/view/98591347#group-closest-lesson")
time.sleep(1)


def check_missed_tasks(missed_tasks: list):
    for task in missed_tasks:
        icon_bonus = task.find('i', {'class': 'alg-icon icon-bonus is-small'})
        if icon_bonus is None:
            icon_bonus = task.find('i', {'class': 'alg-icon icon-bonus is-small is-white'})
        icon_locked = task.find('i', {'class': 'alg-icon icon-closed is-small'})
        if (icon_bonus is None) and (icon_locked is None):
            return missed_tasks
    return []


def sort_locked_tasks(tasks: list):
    total_task = []
    for task in tasks:
        blocked_task = task.find('i', {'class', 'alg-icon icon-closed is-small'})
        if blocked_task is None:
            total_task.append(task)
    if total_task or not tasks:
        return True
    else:
        return False


def check_complex_tasks(completed_tasks: list):
    bonus_tasks = []
    for task in completed_tasks:
        icon_bonus = task.find('i', {'class': 'alg-icon icon-bonus is-small is-white'})
        if icon_bonus is not None:
            bonus_tasks.append(task)
    return bonus_tasks


page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
blocks_with_students = soup.find_all('tr', {'class': 'lessons-table__tr'})
total_result = {}
for block in blocks_with_students:
    count_stars = 0
    name = block.find('div', {'class', 'lessons-table__meta-name'}).text.split(" ")[0].replace('\n', '')
    all_task_progress = block.find_all('div', {'class': 'lessons-table__task-progress'})
    all_task_progress = all_task_progress[:-1]
    for task_progress in all_task_progress:
        failed_basic_task = task_progress.find_all('a', {'class': 'lessons-table__level lessons-table__level--red'})
        failed_basic_task = check_missed_tasks(failed_basic_task)
        missed_basic_task = task_progress.find_all('span', {'class': 'lessons-table__level'})
        missed_basic_task = check_missed_tasks(missed_basic_task)
        completed_complex_task = task_progress.find_all('a', {'class': 'lessons-table__level lessons-table__level--green'}) + task_progress.find_all('a', {'class': 'lessons-table__level lessons-table__level--green at-home'})
        completed_complex_task = check_complex_tasks(completed_complex_task)
        not_locked_tasks = sort_locked_tasks(task_progress.find_all('span', {'class': 'lessons-table__level'}))

        if len(failed_basic_task) == 0 and len(missed_basic_task) == 0 and not_locked_tasks:
            count_stars += 1
        if len(completed_complex_task) != 0:
            count_stars += math.ceil(len(completed_complex_task)/2)

    total_result[name] = count_stars

print(total_result)


# import pandas as pd
#
# # Загружаем ваш файл в переменную `file` / вместо 'example' укажите название свого файла из текущей директории
# file = 'Stars.xlsx'
#
# # Загружаем spreadsheet в объект pandas
# xl = pd.ExcelFile(file)
# # Загрузить лист в DataFrame по его имени: df1
# df1 = xl.parse('Лист1')
#
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', None)
# print(df1)
# # # Указать writer библиотеки
# # writer = pd.ExcelWriter('Stars.xlsx', engine='xlsxwriter')
#
# # # Записать ваш DataFrame в файл
# # yourData.to_excel(writer, 'Sheet1')
# #
# # # Сохраним результат
# # writer.save()
