from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import logging
import allure


class BasePage:
    """Базовый класс страницы"""
    _logger_name = None

    def __init__(self, browser):
        """Инициализация драйвера"""
        self.driver: WebDriver = browser
        self.logger = logging.getLogger(self._logger_name)

    def _click_to_element(self, locator):
        """Клик по элементу"""
        with allure.step('Поиск и клик по элементу'):
            try:
                self.driver.implicitly_wait(3)
                WebDriverWait(self.driver, 5).until(ec.presence_of_element_located(locator))
            except NoSuchElementException:
                allure.attach(body=self.driver.get_screenshot_as_png(),
                              name="screenshot_image",
                              attachment_type=allure.attachment_type.PNG)
                raise AssertionError(e.msg)
            finally:
                self.driver.find_element(*locator).click()

    def _send_keys(self, value: str, locator: By.XPATH) -> None:
        """Отправка набора"""
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(value)

    def _selecting_by_visible_text(self, locator: By.XPATH, text: str) -> None:
        """Отображение видимого текста"""
        select = Select(self.driver.find_element(*locator))
        select.select_by_visible_text(text)

    def _get_element_text(self, locator) -> None:
        """Получить текст элемента"""
        return self.driver.find_element(locator).text

    def _wait_for_visible(self, locator: By.XPATH, time_wait=3):
        """Ожидание появления"""
        return WebDriverWait(self.driver, time_wait).until(ec.visibility_of(self.driver.find_element(*locator)))
