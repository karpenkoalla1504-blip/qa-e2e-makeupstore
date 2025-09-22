ID: SMK-002
Title: Login (negative) — wrong password
Type: Smoke
Priority: High

Preconditions:
- A valid user account exists.
- A correct email is known.

Steps:
1. Open https://makeupstore.com
2. Click on the login icon.
3. Enter a valid email in field #login.
4. Enter an incorrect password in field #pw.
5. Click the login button.
6. Navigate to https://makeupstore.com/user/

Expected Result:
- The system redirects to https://makeupstore.com/#auth.
- The user is not logged in.

Postconditions:
- No session is created.

Automation link:
- tests/smoke/test_login.py::test_login_negative_wrong_password
