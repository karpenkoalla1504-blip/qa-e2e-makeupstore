from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from time import sleep  # ← ДОБАВИТЬ
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    # ТВОИ ТОЧНЫЕ ЛОКАТОРЫ (твои пути стоят первыми)
    LOGIN_ICON = (By.CSS_SELECTOR, "body > div.site-wrap > div.main-wrap > header > div.header-middle > div > div.header-right-row > div.header-office")
    LOGIN_ICON_FALLBACK = (By.CSS_SELECTOR, ".header-office")

    INPUT_EMAIL = (By.CSS_SELECTOR, "#login")
    INPUT_PASSWORD = (By.CSS_SELECTOR, "#pw")

    SUBMIT_BTN = (By.CSS_SELECTOR, "#form-auth > div > div > div:nth-child(6) > button")
    SUBMIT_BTN_FALLBACK = (By.CSS_SELECTOR, "#form-auth button[type='submit']")

    def __init__(self, driver, base_url):
        self.d = driver
        self.base = base_url.rstrip("/")

    # ======== низкоуровневые помощники ========
    def _click(self, locator, timeout=10):
        W(self.d, timeout).until(EC.element_to_be_clickable(locator)).click()

    def _type(self, locator, text, timeout=10, clear=True):
        el = W(self.d, timeout).until(EC.visibility_of_element_located(locator))
        if clear:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)

    def open(self):
        self.d.get(self.base)

    # ======== шаги логина ========
    def open_login_popup(self):
        """Кликаем по иконке, чтобы раскрылось окошко (не новый урл)."""
        try:
            self._click(self.LOGIN_ICON, timeout=8)
            return True
        except Exception:
            try:
                self._click(self.LOGIN_ICON_FALLBACK, timeout=5)
                return True
            except Exception:
                return False

    from time import sleep

    def fill_credentials_and_submit(self, email, password):
        self._type(self.INPUT_EMAIL, email, timeout=10)
        self._type(self.INPUT_PASSWORD, password, timeout=10)
        try:
            self._click(self.SUBMIT_BTN, timeout=10)
        except Exception:
            self._click(self.SUBMIT_BTN_FALLBACK, timeout=10)

        # Ждём, что форма исчезнет или появится что-то новое
        sleep(2)  # небольшой буфер после сабмита

    def go_to_user_and_check_logged_in(self, timeout=10):
        """
        Пробуем несколько раз перейти на /user/, чтобы поймать успешный логин.
        """
        user_url = urljoin(self.base + "/", "user/")
        for attempt in range(3):
            self.d.get(user_url)
            W(self.d, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")
            current = self.d.current_url
            if current.startswith(user_url):
                return True
            sleep(2)  # ждём и пробуем ещё раз
        return False

