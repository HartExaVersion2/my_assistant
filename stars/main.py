import os
from fill_table import FillTable
from parser import StarsParser


algo_login = os.environ.get("AlgDimLogin")
algo_password = os.environ.get("AlgDimPassword")
stars_parser = StarsParser()
stars_parser.authorize(algo_login, algo_password)
dict_stars = stars_parser.parse_stars()
work_with_table = FillTable('Stars.xlsx')
work_with_table.fill_table(dict_stars)