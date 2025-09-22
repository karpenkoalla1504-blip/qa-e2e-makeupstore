ID: SMK-001
Title: Login (positive)
Type: Smoke
Priority: High
Preconditions:
  - Тестовый аккаунт существует (email/пароль заданы в секретах)
Data:
  - TEST_LOGIN_EMAIL / TEST_LOGIN_PASSWORD
Steps:
  1) Открыть https://makeupstore.com
  2) Открыть форму входа
  3) Ввести корректные email и пароль
  4) Нажать Sign in / Log in
Expected Result:
  - Пользователь авторизован: видна иконка профиля/Logout
Links:
  - Автотест: tests/smoke/test_login.py::test_login_positive
