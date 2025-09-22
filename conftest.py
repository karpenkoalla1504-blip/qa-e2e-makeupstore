import os, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import get_logger
from dotenv import load_dotenv
import pathlib

# локально можно держать .env; на CI переменные окружения задаются в настройках
load_dotenv(override=False)

@pytest.fixture(scope="session")
def config():
    return {
        "base_url": os.getenv("BASE_URL", "https://makeupstore.com"),
        "email": os.getenv("TEST_LOGIN_EMAIL", ""),
        "password": os.getenv("TEST_LOGIN_PASSWORD", ""),
    }

@pytest.fixture
def logger():
    return get_logger("smoke")

@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--headless=new")       # сними, если хочешь видеть браузер
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    d = webdriver.Chrome(options=opts)        # Selenium Manager сам подберёт chromedriver
    yield d
    d.quit()

# делаем скриншот при падении теста
@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    yield
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        pathlib.Path("reports/screens").mkdir(parents=True, exist_ok=True)
        fname = f"reports/screens/{request.node.name}.png"
        try:
            driver.save_screenshot(fname)
        except Exception:
            pass

# чтобы знать статус фазы "call" (нужен для фикстуры выше)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
