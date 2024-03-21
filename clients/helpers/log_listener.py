import logging
from selenium.webdriver.support.events import AbstractEventListener

logging.basicConfig(level=logging.INFO, filename='report.log')
logger = logging.getLogger('Browser actions')


class Listener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        logger.info(f"Перехожу в {url}")

    def after_navigate_to(self, url, driver):
        logger.info(f"На {url}")

    def before_navigate_back(self, driver):
        logger.info(f"Перехожу обратно")

    def after_navigate_back(self, driver):
        logger.info(f"Возвращение")

    def before_find(self, by, value, driver):
        logger.info(f"Ищу '{value}' с '{by}'")

    def after_find(self, by, value, driver):
        logger.info(f"Нашел '{value}' с '{by}'")

    def before_execute_script(self, script, driver):
        logger.info(f"Вставляю '{script}'")

    def after_execute_script(self, script, driver):
        logger.info(f"Выполнил '{script}'")

    def before_quit(self, driver):
        logger.info(f"Разрываю с {driver}")

    def after_quit(self, driver):
        logger.info(f"ВЫКЛ")

    def on_exception(self, exception, driver):
        logger.error(f'Получил ошибку: {exception}')
        driver.save_screenshot(f'{exception}.png')
