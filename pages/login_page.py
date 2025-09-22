from time import sleep
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    # --- Точные локаторы (из твоего описания) ---
    LOGIN_ICON = (By.CSS_SELECTOR,
                  "body > div.site-wrap > div.main-wrap > header > div.header-middle > div > div.header-right-row > div.header-office")
    LOGIN_ICON_FALLBACK = (By.CSS_SELECTOR, ".header-office")

    INPUT_EMAIL = (By.CSS_SELECTOR, "#login")
    INPUT_PASSWORD = (By.CSS_SELECTOR, "#pw")

    SUBMIT_BTN = (By.CSS_SELECTOR, "#form-auth > div > div > div:nth-child(6) > button")
    SUBMIT_BTN_FALLBACK = (By.CSS_SELECTOR, "#form-auth button[type='submit']")

    COOKIE_ACCEPT = (By.CSS_SELECTOR, "[data-testid='cookie-accept'], .cookie-accept, .cc-allow, .cookie-accept-button")

    def __init__(self, driver, base_url: str):
        self.d = driver
        self.base = base_url.rstrip("/")

    # ---------- helpers ----------
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

    def _is_any_visible(self, locators, timeout=10):
        for loc in (locators if isinstance(locators, (list, tuple)) else [locators]):
            try:
                W(self.d, timeout).until(EC.visibility_of_element_located(loc))
                return True
            except Exception:
                continue
        return False

    def _wait_dom_idle(self, timeout=12):
        W(self.d, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")

    # ---------- base actions ----------
    def open(self):
        self.d.get(self.base)
        self.try_accept_cookies()

    def try_accept_cookies(self):
        try:
            W(self.d, 3).until(EC.element_to_be_clickable(self.COOKIE_ACCEPT)).click()
        except Exception:
            pass

    # ---------- auth flow ----------
    def open_login_popup(self) -> bool:
        """Открываем попап логина и ждём поля."""
        try:
            self._click(self.LOGIN_ICON, timeout=8)
        except Exception:
            try:
                self._click(self.LOGIN_ICON_FALLBACK, timeout=5)
            except Exception:
                return False
        return self._is_any_visible([self.INPUT_EMAIL, self.INPUT_PASSWORD], timeout=8)

    def fill_credentials_and_submit(self, email: str, password: str):
        """Вводим креды и сабмитим. Ждём закрытие/инвиз формы и стабилизацию DOM."""
        self._type(self.INPUT_EMAIL, email, timeout=12)
        self._type(self.INPUT_PASSWORD, password, timeout=12)
        try:
            self._click(self.SUBMIT_BTN, timeout=12)
        except Exception:
            self._click(self.SUBMIT_BTN_FALLBACK, timeout=12)

        # В CI форма может оставаться на экране пару секунд — ждём исчезновения хотя бы одного поля
        try:
            W(self.d, 8).until(EC.invisibility_of_element_located(self.INPUT_PASSWORD))
        except Exception:
            # если форма не закрылась — просто чуть подождём
            sleep(1.5)

        self._wait_dom_idle(timeout=12)
        sleep(1.0)  # маленький буфер, чтобы сервер успел выставить сессию

    def go_to_user_and_check_logged_in(self, timeout=10) -> bool:
        """
        Делаем несколько попыток открыть /user/, давая времени сессии установиться.
        Успех: остались на /user/. Провал: после 8 попыток всё ещё редиректит.
        """
        user_url = urljoin(self.base + "/", "user/")
        for _ in range(8):
            self.d.get(user_url)
            self._wait_dom_idle(timeout=timeout)
            current = self.d.current_url
            if current.startswith(user_url):
                return True
            # если редиректит на /#auth — чуть подождём и попробуем ещё
            sleep(2.0)
        return False

    def login_flow(self, email: str, password: str) -> bool:
        self.open()
        assert self.open_login_popup(), "Не нашли/не открылся попап логина"
        self.fill_credentials_and_submit(email, password)
        return self.go_to_user_and_check_logged_in()
