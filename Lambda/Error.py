class Error:
    UNKNOWN_ACCOUNT = "Account Does Not Exist"
    PASSWORD_MISMATCH = "Password Mismatch"
    PASSWORD_WEAK = "Weak Password (8 characters / 1 upper / 1 lower / 1 number at least)"

    TOKEN_MISMATCH = "Token Mismatch"

    NAME_NOT_FOUND = "Name Not Found"
    NAME_DUPLICATE = "Name Has Already been Taken"

    INVALID_EMAIL_FORMAT = "Invalid Email Format"
    EMAIL_DUPLICATE = "Email Has Already Been Taken"

    LOGIN_FAILED = "Username or password is incorrect"

    INCORRECT_CODE = "Incorrect Code"

    TIMESTAMP_ERROR = "Action too fast"
