from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class LoginPage:
    LOGIN_ICON = ".header-office"
    INPUT_EMAIL = "#login"
    INPUT_PASSWORD = "#pw"
    SUBMIT_BTN = "#form-auth > div > div > div:nth-child(6) > button"
    SUBMIT_BTN_FALLBACK = "#form-auth button[type='submit']"

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        """Открыть главную страницу"""
        self.driver.get(self.base_url)

    def _click(self, selector, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        ).click()

    def _type(self, selector, text, timeout=10):
        el = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        el.clear()
        el.send_keys(text)

    def open_login_form(self) -> bool:
        """Открыть форму логина (основной метод)"""
        try:
            self._click(self.LOGIN_ICON, timeout=10)
            return True
        except Exception:
            return False

    def open_login_popup(self) -> bool:
        """Алиас для совместимости со старыми тестами"""
        return self.open_login_form()

    def fill_credentials_and_submit(self, email, password):
        """Ввести логин/пароль и нажать кнопку"""
        self._type(self.INPUT_EMAIL, email, timeout=10)
        self._type(self.INPUT_PASSWORD, password, timeout=10)
        try:
            self._click(self.SUBMIT_BTN, timeout=10)
        except Exception:
            self._click(self.SUBMIT_BTN_FALLBACK, timeout=10)

        # Подождём чуть-чуть, чтобы форма успела обработаться
        sleep(2)

    def go_to_user_and_check_logged_in(self) -> bool:
        """Перейти на /user/ и проверить, что не редиректит обратно на /#auth"""
        self.driver.get(self.base_url + "/user/")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return "/#auth" not in self.driver.current_url
