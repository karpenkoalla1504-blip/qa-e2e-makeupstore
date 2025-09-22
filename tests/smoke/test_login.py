import pytest
from pages.login_page import LoginPage

pytestmark = [pytest.mark.smoke, pytest.mark.ui]

def test_login_positive(driver, config, logger):
    """SMK-001: Позитивный логин — корректные креды из ENV."""
    assert config["email"] and config["password"], "Нужно задать TEST_LOGIN_EMAIL/TEST_LOGIN_PASSWORD"
    lp = LoginPage(driver, config["base_url"])

    logger.info("Открываем сайт")
    lp.open()

    logger.info("Открываем форму логина")
    assert lp.open_login_form(), "Не нашли кнопку входа — проверь BTN_LOGIN_CANDIDATES"

    logger.info("Логинимся корректными данными")
    lp.login(config["email"], config["password"])

    logger.info("Проверяем, что вошли")
    assert lp.is_logged_in(), "Должна появиться иконка профиля/Logout"

def test_login_negative_wrong_password(driver, config, logger):
    """SMK-002: Негатив — неверный пароль."""
    assert config["email"], "Нужно задать TEST_LOGIN_EMAIL"
    bad_pass = "wrong_" + (config["password"] or "password123")
    lp = LoginPage(driver, config["base_url"])

    logger.info("Открываем сайт")
    lp.open()

    logger.info("Открываем форму логина")
    assert lp.open_login_form(), "Не нашли кнопку входа — проверь BTN_LOGIN_CANDIDATES"

    logger.info("Пробуем войти с неверным паролем")
    lp.login(config["email"], bad_pass)

    logger.info("Проверяем, что вход не выполнен и показана ошибка")
    assert not lp.is_logged_in(), "Не должны войти с неверным паролем"
    assert lp.has_error(), "Ожидали сообщение об ошибке на форме логина"
