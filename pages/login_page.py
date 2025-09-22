from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    BTN_LOGIN_CANDIDATES = [
        (By.CSS_SELECTOR, "a[href*='login']"),
        (By.CSS_SELECTOR, "button[href*='login']"),
        (By.CSS_SELECTOR, ".login-button"),
        (By.LINK_TEXT, "Login"),
        (By.PARTIAL_LINK_TEXT, "Log in"),
        (By.CSS_SELECTOR, "[data-test='login']"),
        (By.CSS_SELECTOR, ".header-login, .header .login"),
    ]
    INPUT_EMAIL_CANDIDATES = [
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[name='email']"),
        (By.CSS_SELECTOR, "#email"),
    ]
    INPUT_PASSWORD_CANDIDATES = [
        (By.CSS_SELECTOR, "input[type='password']"),
        (By.CSS_SELECTOR, "input[name='password']"),
        (By.CSS_SELECTOR, "#password"),
    ]
    BTN_SUBMIT_CANDIDATES = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.CSS_SELECTOR, ".btn.login, .button.login, .auth-submit"),
        (By.XPATH, "//button[contains(., 'Sign in') or contains(., 'Log in')]"),
    ]
    LOGGED_IN_MARKERS = [
        (By.CSS_SELECTOR, ".header-profile, .user-avatar, [data-test='profile']"),
        (By.XPATH, "//*[contains(., 'Logout') or contains(., 'Sign out')]"),
    ]
    ERROR_MARKERS = [
        (By.CSS_SELECTOR, ".error, .error-message, .form-error, [data-test='login-error']"),
        (By.XPATH, "//*[contains(., 'invalid') or contains(., 'Incorrect') or contains(., 'wrong')]"),
    ]

    def __init__(self, driver, base_url):
        self.d = driver
        self.base = base_url

    def open(self):
        self.d.get(self.base)

    def _click_first_available(self, candidates, timeout=10):
        for loc in candidates:
            try:
                W(self.d, timeout).until(EC.element_to_be_clickable(loc)).click()
                return True
            except Exception:
                continue
        return False

    def _type_first_available(self, candidates, text, timeout=10, clear=True):
        for loc in candidates:
            try:
                el = W(self.d, timeout).until(EC.visibility_of_element_located(loc))
                if clear: el.clear()
                el.send_keys(text)
                return True
            except Exception:
                continue
        return False

    def open_login_form(self):
        return self._click_first_available(self.BTN_LOGIN_CANDIDATES)

    def submit(self):
        return self._click_first_available(self.BTN_SUBMIT_CANDIDATES)

    def login(self, email, password):
        self._type_first_available(self.INPUT_EMAIL_CANDIDATES, email)
        self._type_first_available(self.INPUT_PASSWORD_CANDIDATES, password)
        self.submit()

    def is_logged_in(self, timeout=10):
        for loc in self.LOGGED_IN_MARKERS:
            try:
                W(self.d, timeout).until(EC.presence_of_element_located(loc))
                return True
            except Exception:
                continue
        return False

    def has_error(self, timeout=5):
        for loc in self.ERROR_MARKERS:
            try:
                W(self.d, timeout).until(EC.presence_of_element_located(loc))
                return True
            except Exception:
                continue
        return False
