from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from common.browser import Browser
from common.errors import InitError, UnknownError
from config import BROWSER, URLS
import time
import math


class StarsParser():

    def __init__(self, logger):
        try:
            self.browser = Browser(BROWSER.WINDOW_HEIGHT, BROWSER.WINDOW_WIDTH, BROWSER.HEADLESS, BROWSER.SANDBOX)
            self.driver = self.browser.get_driver()
            self.logger = logger
        except Exception as error:
            message = 'class StarsParser error {}'.format(error)
            raise InitError(message)

    def authorize(self, login, password):
        try:
            self.driver.get(URLS.AUTH)
            element_login = self.driver.find_element(By.ID, 'login')
            element_login.send_keys(login)
            element_login.send_keys(Keys.ENTER)
            time.sleep(1)
            element_password = self.driver.find_element(By.ID, 'password')
            element_password.send_keys(password)
            element_password.send_keys(Keys.ENTER)
            time.sleep(5)
        except Exception as error:
            message = 'function {} error {}'.format(self.authorize.__name__, error)
            self.logger.error(message)
            raise UnknownError

    def __check_missed_tasks(self, missed_tasks: list):
        try:
            for task in missed_tasks:
                icon_bonus = task.find('i', {'class': 'alg-icon icon-bonus is-small'})
                if icon_bonus is None:
                    icon_bonus = task.find('i', {'class': 'alg-icon icon-bonus is-small is-white'})
                icon_locked = task.find('i', {'class': 'alg-icon icon-closed is-small'})
                if (icon_bonus is None) and (icon_locked is None):
                    return missed_tasks
            return []
        except Exception as error:
            message = 'function {} error {}'.format(self.__check_missed_tasks.__name__, error)
            self.logger.error(message)
            raise UnknownError

    def __sort_locked_tasks(self, tasks: list):
        try:
            total_task = []
            for task in tasks:
                blocked_task = task.find('i', {'class', 'alg-icon icon-closed is-small'})
                if blocked_task is None:
                    total_task.append(task)
            if total_task or not tasks:
                return True
            else:
                return False
        except Exception as error:
            message = 'function {} error {}'.format(self.__sort_locked_tasks.__name__, error)
            self.logger.error(message)
            raise UnknownError

    def __check_complex_tasks(self, completed_tasks: list):
        try:
            bonus_tasks = []
            for task in completed_tasks:
                icon_bonus = task.find('i', {'class': 'alg-icon icon-bonus is-small is-white'})
                if icon_bonus is not None:
                    bonus_tasks.append(task)
            return bonus_tasks
        except Exception as error:
            message = 'function {} error {}'.format(self.__check_complex_tasks.__name__, error)
            self.logger.error(message)
            raise UnknownError

    def parse_stars(self) -> dict:
        try:
            self.driver.get(URLS.CLOSEST_LESSON)
            time.sleep(1)
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            blocks_with_students = soup.find_all('tr', {'class': 'lessons-table__tr'})
            total_result = {}
            for block in blocks_with_students:
                count_stars = 0
                name = block.find('div', {'class', 'lessons-table__meta-name'}).text.split(" ")[0].replace('\n', '')
                all_task_progress = block.find_all('div', {'class': 'lessons-table__task-progress'})
                all_task_progress = all_task_progress[:-1]
                for task_progress in all_task_progress:
                    failed_basic_task = task_progress.find_all('a',
                                                               {'class': 'lessons-table__level lessons-table__level--red'})
                    failed_basic_task = self.__check_missed_tasks(failed_basic_task)
                    missed_basic_task = task_progress.find_all('span', {'class': 'lessons-table__level'})
                    missed_basic_task = self.__check_missed_tasks(missed_basic_task)
                    completed_complex_task = task_progress.find_all('a', {
                        'class': 'lessons-table__level lessons-table__level--green'}) + task_progress.find_all('a', {
                        'class': 'lessons-table__level lessons-table__level--green at-home'})
                    completed_complex_task = self.__check_complex_tasks(completed_complex_task)
                    not_locked_tasks = self.__sort_locked_tasks(task_progress.find_all('span', {'class': 'lessons-table__level'}))

                    if len(failed_basic_task) == 0 and len(missed_basic_task) == 0 and not_locked_tasks:
                        count_stars += 1
                    if len(completed_complex_task) != 0:
                        count_stars += math.ceil(len(completed_complex_task) / 2)

                total_result[name] = count_stars
            return total_result
        except Exception as error:
            message = 'function {} error {}'.format(self.parse_stars.__name__, error)
            self.logger.error(message)
            raise UnknownError