import os, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.logger import get_logger
from dotenv import load_dotenv
import pathlib

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
    headless = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")

    # --- важные флаги для CI ---
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--lang=en-US")
    # можно переопределить UA через ENV USER_AGENT, иначе используем дефолтный «человеческий»
    ua = os.getenv("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/118.0.0.0 Safari/537.36")
    opts.add_argument(f"--user-agent={ua}")

    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()

# скрин/HTML при падении
@pytest.fixture(autouse=True)
def screenshot_on_failure(request, driver):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        pathlib.Path("reports/screens").mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(f"reports/screens/{request.node.name}_{ts}.png")
        try:
            with open(f"reports/screens/{request.node.name}_{ts}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except Exception:
            pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
