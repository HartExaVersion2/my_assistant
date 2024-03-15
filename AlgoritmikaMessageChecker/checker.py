from common.browser import Browser
from common.logger import Log
from common.errors import UnknownError
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

logger = Log('checker', 'AlgoritmikaMessageChecker/checker.py', 'checker')

def authorize(login, password, driver):
    try:
        driver.get("https://lms.algoritmika.org/auth/v3/login#group-closest-lesson")
        driver.set_window_size(1024, 768)

        element_login = driver.find_element(By.ID, 'login')
        element_login.send_keys(login)
        element_login.send_keys(Keys.ENTER)
        time.sleep(1)
        element_password = driver.find_element(By.ID, 'password')
        element_password.send_keys(password)
        element_password.send_keys(Keys.ENTER)
        time.sleep(5)
        driver.get("https://lms.algoritmika.org/group/view/98591347#group-closest-lesson")
        time.sleep(1)
    except Exception as error:
        message = 'function {} error {}'.format(authorize.__name__, error)
        logger.error(message)
        raise UnknownError


def check_messages(driver) -> bool:
    try:
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
        browser = Browser()
        driver = browser.get_driver()
        authorize(logins[i], passwords[i], driver)
        if check_messages(driver):
            print(names[i], 'игнорщик')
        else:
            print(names[i], 'всо прочитал')
        browser.close()
    logger.info('END checker.py')
except Exception as error:
    logger.error('checker.py error {}'.format(error))

