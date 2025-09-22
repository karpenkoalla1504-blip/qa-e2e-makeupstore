ID: SMK-001
Title: Login (positive)
Type: Smoke
Priority: High

Preconditions:
- A valid user account exists.
- Credentials are stored in CI secrets or in a local .env file (TEST_LOGIN_EMAIL / TEST_LOGIN_PASSWORD).

Steps:
1. Open https://makeupstore.com
2. Click on the login icon (selector: .header-office).
3. Enter a valid email in field #login.
4. Enter a valid password in field #pw.
5. Click the login button (#form-auth > … > button).
6. Navigate to https://makeupstore.com/user/

Expected Result:
- The user remains on https://makeupstore.com/user/ (no redirect to /#auth).
- The personal account page is accessible.

Postconditions:
- The user is logged in.
- Session is active.

Automation link:
- tests/smoke/test_login.py::test_login_positive
