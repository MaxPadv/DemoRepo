from selenium.webdriver.common.by import By
from Web.Pages.BasePage import BasePage


class MainPage(BasePage):
    """Главная страница"""
    # Текстовая нагрузка
    REPLENISH = (By.XPATH, "//*[text()='Пополнить']")
    BALANCE = (By.XPATH, "//*[text()='Ваш баланс']")
    ADD_BALANCE = (By.XPATH, "//*[text()='Пополнение баланса']")
    SCENARIO = (By.XPATH, "//*[text()='Выберите сценарий']")
    VALID_ADD = (By.XPATH, "//*[text()='Успешное пополнение']")
    APPEAL = (By.XPATH, "//*[text()='Апелляция']")
    SCENARIOS = (By.XPATH, "//*[text()='Отмена']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
