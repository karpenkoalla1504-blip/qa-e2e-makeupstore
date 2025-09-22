import pytest
from pages.search_page import SearchPage

pytestmark = [pytest.mark.smoke, pytest.mark.ui]

def test_search_dior_shows_dior_in_first_title(driver, config, logger):
    """
    Steps:
    1) open https://makeupstore.com/
    2) click search icon
    3) type 'dior' into #search-input and submit
    4) wait first product card visible
    5) assert first product title contains 'dior' (case-insensitive)
    """
    sp = SearchPage(driver, config["base_url"])

    logger.info("Open main page")
    sp.open()

    logger.info("Open search input")
    sp.open_search()

    logger.info("Type query 'dior' and submit")
    sp.search("dior")

    logger.info("Read first product title")
    title = sp.first_card_title()
    logger.info(f"First product title: {title!r}")

    assert "dior" in title.lower(), "Expected 'dior' in the first product title"
