try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Account(Data):
    """Manages the information in the user accounts"""
    TABLE = "Account"
    """Specifies the account table column name"""
    NAME = "username"
    """Specifies the username attribute column name"""
    PASSWORD = "password"
    """Specifies the password attribute column name"""
    EMAIL = "email"
    """Specifies the email attribute column name"""
    STATUS = "status"
    """Specifies the status attribute column name"""
    TOKEN = "token"
    """Specifies the token attribute column name"""
    TIMESTAMP = "timestamp"
    """Specifies the timestamp attribute column name"""
    ID = "account_id"
    """Specifies the id attribute column name"""
    COLUMNS = [NAME, PASSWORD, EMAIL, STATUS, TOKEN, TIMESTAMP, ID]
    """Organizes the name, password, email, status, token, timestamp, and id variables into an array"""
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    """Creates an explicit version of the name variable column name"""
    EXPLICIT_PASSWORD = f"{TABLE}.{PASSWORD}"
    """Creates an explicit version of the password variable column name"""
    EXPLICIT_EMAIL = f"{TABLE}.{EMAIL}"
    """Creates an explicit version of the email variable column name"""
    EXPLICIT_STATUS = f"{TABLE}.{STATUS}"
    """Creates an explicit version of the status variable column name"""
    EXPLICIT_TOKEN = f"{TABLE}.{TOKEN}"
    """Creates an explicit version of the token variable column name"""
    EXPLICIT_TIMESTAMP = f"{TABLE}.{TIMESTAMP}"
    """Creates an explicit version of the timestamp variable column name"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the id variable column name"""
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_PASSWORD, EXPLICIT_EMAIL, EXPLICIT_STATUS,
                        EXPLICIT_TOKEN, EXPLICIT_TIMESTAMP, EXPLICIT_ID]
    """Organizes the explicit versions of the variable column names above into an array"""

    def __init__(self, username: str, password: str, email: str, status: str = "N",
                 token: str = "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))", timestamp: str = "NOW()",
                 account_id: int = None):
        """
            initializes the username, password, email, status, token, timestamp, and account id variables

            Parameters:

                >username       : string<   Specify the username of the account.
                >password       : string<   Specify the password of the account.
                >email          : string<   Specify the email of the account.
                >status         : string<   Specify the status of the account (Optional).
                >token          : string<   Specify the token of the account (Optional).
                >timestamp      : string<   Specify the timestamp of the account (Optional).
                >account_id     : int<      Specify the account_id of the account (Optional).
        """
        self.username = username
        """username       : string<   Store the username of the account"""
        self.password = password
        """password       : string<   Store the password of the account"""
        self.email = email
        """email          : string<   Specify the email of the account"""
        self.status = status
        """status         : string<   Specify the status of the account (Optional)."""
        self.token = token
        """token          : string<   Specify the token of the account (Optional)."""
        self.timestamp = str(timestamp)
        """timestamp      : string<   Specify the timestamp of the account (Optional)."""
        self.account_id = int(account_id) if account_id is not None else None
        """account_id     : int<      Specify the account_id of the account (Optional)."""

    def __str__(self):
        """returns a formatted string version of the variables"""
        return "[Account    ]               :USERNAME: {:<12} PASSWORD: {:<12} EMAIL: {:<12} STATUS: {:<2} " \
               "TOKEN: {:<20} TIMESTAMP: {:<12} Account_ID: {:<8}"\
            .format(self.username, self.password, self.email, self.status, self.token, self.timestamp, self.account_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Account":
        """
            Determines if explicit is true, if so create Account with the explicit variables column name with payload,
            if not create Account with the non-explicit variables column name with payload and return object

            Parameter:

                >payload    : dict<:    Payload that contains the information of account creation
                >explicit   : bool<:    Flag that indicates the payload key is explicit column

            Return:

                >account    : Account<: Account created
        """
        if explicit:
            return Account(payload[Account.EXPLICIT_NAME], payload[Account.EXPLICIT_PASSWORD],
                           payload[Account.EXPLICIT_EMAIL], payload[Account.EXPLICIT_STATUS],
                           payload[Account.EXPLICIT_TOKEN], payload[Account.EXPLICIT_TIMESTAMP],
                           payload[Account.EXPLICIT_ID])
        else:
            return Account(payload[Account.NAME], payload[Account.PASSWORD],
                           payload[Account.EMAIL], payload[Account.STATUS],
                           payload[Account.TOKEN], payload[Account.TIMESTAMP],
                           payload[Account.ID])

