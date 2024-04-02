import os
from fill_table import FillTable
from parser import StarsParser
from common.logger import Log
from common.errors import UnknownError, InitError
from common.datamodel import WorkReports
from config import URLS
import requests

def __send_report(error_code, text):
    try:
        report = WorkReports(error=error_code, text=text)
        json_data = report.dict()
        requests.post(URLS.CORE_API, json=json_data)
    except Exception as error:
        message = 'function {} error {}'.format(__send_report.__name__, error)
        logger.error(message)
        raise UnknownError

logger = Log('star_parser', 'stars/main.py', 'main')
try:
    logger.info('START function main stars parser')
    algo_login = os.environ.get("AlgDimLogin")
    algo_password = os.environ.get("AlgDimPassword")
    stars_parser = StarsParser(logger)
    stars_parser.authorize(algo_login, algo_password)
    dict_stars = stars_parser.parse_stars()
    work_with_table = FillTable('Stars.xlsx', logger)
    work_with_table.fill_table(dict_stars)
    __send_report(0, 'Звёзды подсчитаны')
    logger.info('END function main stars parser')
except InitError as error:
    message = 'Init Error {}'.format(error)
    logger.error(message)
    __send_report(0, 'В приложении starts произошла ошибка')
except UnknownError as error:
    logger.error(error)
    __send_report(0, 'В приложении starts произошла ошибка')
except Exception as error:
    message = 'error in main function. Error {}'.format(error)
    logger.error(message)
    __send_report(0, 'В приложении starts произошла ошибка')