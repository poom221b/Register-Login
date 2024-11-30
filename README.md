Registration and Login Program
This program allows users to register and log in using a username and password stored in an Excel file (users.xlsx). Passwords are hashed for security.

Features
User Registration: Allows users to register with a username and a password. The password must be at least 8 characters long and contain both letters and numbers.
Login: Allows users to log in by verifying their username and password.
Data Storage: User information is stored in an Excel file with usernames and hashed passwords.

Test Cases
Test Case 1: User Registration
Action: Register with a unique username and a valid password.
Expected: User is registered successfully.
Test Case 2: Duplicate Username Registration
Action: Register with an existing username.
Expected: "Username already exists!"
Test Case 3: Invalid Password Registration
Action: Register with a password that doesn't meet the criteria.
Expected: "Invalid password!"
Test Case 4: Successful Login
Action: Login with a registered username and correct password.
Expected: "Login successful!"
Test Case 5: Invalid Login
Action: Login with an incorrect username or password.
Expected: "Invalid username or password!"
Test Case 6: Exit Program
Action: Select "Exit".
Expected: Program exits with "Goodbye!"
