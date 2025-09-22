ID: SMK-002
Title: Login (negative) — wrong password
Type: Smoke
Priority: High
Preconditions:
  - Аккаунт существует
Data:
  - TEST_LOGIN_EMAIL
  - Пароль: заведомо неверный
Steps:
  1) Открыть https://makeupstore.com
  2) Открыть форму входа
  3) Ввести корректный email и неверный пароль
  4) Нажать Sign in / Log in
Expected Result:
  - Авторизация не выполнена
  - Есть сообщение об ошибке, нет признаков логина
Links:
  - Автотест: tests/smoke/test_login.py::test_login_negative_wrong_password
