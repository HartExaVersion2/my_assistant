import os
from fill_table import FillTable
from parser import StarsParser
from common.logger import Log
from common.errors import UnknownError, InitError

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
    logger.info('END function main stars parser')
except InitError as error:
    message = 'Init Error {}'.format(error)
    logger.error(message)
except UnknownError as error:
    logger.error(error)
except Exception as error:
    message = 'error in main function. Error {}'.format(error)
    logger.error(message)