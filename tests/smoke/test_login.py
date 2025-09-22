import pytest
from pages.login_page import LoginPage

pytestmark = [pytest.mark.smoke, pytest.mark.ui]

def test_login_positive(driver, config, logger):
    """
    Позитив: кликаем иконку логина, вводим #login/#pw, сабмитим.
    Успешность = можем остаться на https://makeupstore.com/user/ (без редиректа на /#auth).
    """
    email = config["email"]; password = config["password"]
    assert email and password, "Заполни TEST_LOGIN_EMAIL/TEST_LOGIN_PASSWORD в .env"
    lp = LoginPage(driver, config["base_url"])

    logger.info("Открываем главную")
    lp.open()

    logger.info("Открываем попап логина по иконке .header-office")
    assert lp.open_login_popup(), "Иконка логина не найдена (проверь селектор LOGIN_ICON)"

    logger.info("Вводим логин/пароль и жмём кнопку")
    lp.fill_credentials_and_submit(email, password)

    logger.info("Проверяем, что /user/ доступен без редиректа на /#auth")
    assert lp.go_to_user_and_check_logged_in(), "Ожидали авторизацию (остаться на /user/)"

def test_login_negative_wrong_password(driver, config, logger):
    """
    Негатив: неверный пароль. Ожидаем редирект на /#auth при попытке зайти на /user/.
    """
    email = config["email"]
    assert email, "Для негатива нужен хотя бы корректный email (TEST_LOGIN_EMAIL)"
    bad_pass = "WRONG_" + (config["password"] or "pass123")
    lp = LoginPage(driver, config["base_url"])

    logger.info("Открываем главную и попап логина")
    lp.open()
    assert lp.open_login_popup(), "Иконка логина не найдена"

    logger.info("Вводим неверный пароль и сабмитим")
    lp.fill_credentials_and_submit(email, bad_pass)

    logger.info("Проверяем, что на /user/ нас НЕ пускает (редирект на /#auth)")
    assert not lp.go_to_user_and_check_logged_in(), "Не должны попасть на /user/ с неверным паролем"
