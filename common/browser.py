from selenium import webdriver


class Browser():
    def __init__(self, win_height=1920, win_width=1080, headless=False, sandbox=False):
        self.driver = self.__create_driver(win_height, win_width, headless, sandbox)

    def __create_driver(self, win_height, win_width, headless, sandbox):
        options = webdriver.ChromeOptions()
        if not headless:
            options.add_argument('headless')
        if not sandbox:
            options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(win_width, win_height)
        return driver

    def get_driver(self):
        return self.driver

    def close(self):
        self.driver.close()