from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC

class SearchPage:
    # селекторы из твоего описания
    BTN_SEARCH = (By.CSS_SELECTOR, "body > div.site-wrap > div.main-wrap > header > div.header-middle > div > div.header-left-row > div.search-button")
    INPUT_SEARCH = (By.CSS_SELECTOR, "#search-input")

    FIRST_CARD = (By.CSS_SELECTOR, "body > div.site-wrap > div.main-wrap > div > div > div.catalog > div.catalog-content > div > div.catalog-products > ul > li:nth-child(1) > div.simple-slider-list__link > div.info-product-wrapper")
    FIRST_CARD_TITLE = (By.CSS_SELECTOR, "body > div.site-wrap > div.main-wrap > div > div > div.catalog > div.catalog-content > div > div.catalog-products > ul > li:nth-child(1) > div.simple-slider-list__link > div.info-product-wrapper > a")

    # немного запасных (если вдруг поменяют разметку, тест всё равно попробует найти)
    FALLBACK_BTN_SEARCH = (By.CSS_SELECTOR, ".search-button, [data-test='open-search'], [aria-label*='Search']")
    FALLBACK_INPUT = (By.CSS_SELECTOR, "input#search-input, input[name='q'], input[type='search']")

    def __init__(self, driver, base_url: str):
        self.d = driver
        self.base = base_url.rstrip("/")

    def _click(self, locator, timeout=10):
        W(self.d, timeout).until(EC.element_to_be_clickable(locator)).click()

    def _type(self, locator, text, timeout=10, clear=True, submit=False):
        el = W(self.d, timeout).until(EC.visibility_of_element_located(locator))
        if clear:
            try:
                el.clear()
            except Exception:
                pass
        el.send_keys(text)
        if submit:
            el.submit()

    def open(self):
        self.d.get(self.base)

    def open_search(self):
        try:
            self._click(self.BTN_SEARCH, timeout=8)
        except Exception:
            self._click(self.FALLBACK_BTN_SEARCH, timeout=8)

    def search(self, query: str):
        # некоторые сайты открывают инпут только после клика на кнопку
        try:
            self._type(self.INPUT_SEARCH, query, timeout=10)
        except Exception:
            self._type(self.FALLBACK_INPUT, query, timeout=10)
        # чаще всего поиск стартует по Enter/submit
        try:
            self._type(self.INPUT_SEARCH, "\n", timeout=2, clear=False)
        except Exception:
            pass

    def first_card_title(self, timeout=12) -> str:
        # дожидаемся появления результатов
        W(self.d, timeout).until(EC.visibility_of_element_located(self.FIRST_CARD))
        title_el = W(self.d, timeout).until(EC.visibility_of_element_located(self.FIRST_CARD_TITLE))
        return title_el.text.strip()
