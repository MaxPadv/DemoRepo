import pytest
import logging
import sys

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver

from clients.helpers.log_listener import Listener


def pytest_addoption(parser):
    """Опции запуска"""
    parser.addoption('--url',
                     action='store',
                     default='https://demo.expay.cash/top-up',
                     help='Основная ссылка')
    parser.addoption('--browser_name',
                     action='store',
                     default='firefox',
                     help='Выбор браузера: firefox, chrome')
    parser.addoption('--timeout',
                     action='store',
                     default=40,
                     help='Timeout ожидания WebDriver')
    parser.addoption('--file',
                     action='store',
                     default=None,
                     help='Логи')


@pytest.fixture()
def browser(request, my_logger) -> None:
    """Инициализация браузера"""
    browser = request.config.getoption("--browser_name")
    if browser == 'chrome':
        my_logger.info('\nЗапуск Chrome для теста...')
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        options.add_argument('--ignore-certificate-errors')
        browser = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        my_logger.info('\nЗапуск Firefox для теста...')
        options = webdriver.FirefoxOptions()
        # options.add_argument("-headless")
        browser = EventFiringWebDriver(webdriver.Firefox(options=options), Listener())
    yield browser
    my_logger.info('\nClose browser...')
    browser.quit()


@pytest.fixture()
def my_logger(request) -> logging.getLogger():
    """Кастомный логгер"""
    filename = request.config.getoption('--file')
    logging.basicConfig(level=logging.INFO, filename=filename)
    logger = logging.getLogger('Web Driver')
    if filename is None:
        stdout_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_handler)
    else:
        file_handler = logging.FileHandler(filename)
        logger.addHandler(file_handler)

    return logger


@pytest.fixture()
def get_url(request, browser) -> str:
    """Установка базового линка"""
    url = request.config.getoption("--url")
    timeout = request.config.getoption('--timeout')
    open_link = browser.get(url)
    browser.implicitly_wait(timeout)
    return open_link
