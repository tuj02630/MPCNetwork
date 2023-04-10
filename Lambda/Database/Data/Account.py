try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Account(Data):
    """Manages the information in the user accounts"""
    TABLE = "Account"
    """Specifies the account table"""
    NAME = "username"
    """Specifies the username attribute"""
    PASSWORD = "password"
    """Specifies the password attribute"""
    EMAIL = "email"
    """Specifies the email attribute"""
    STATUS = "status"
    """Specifies the status attribute"""
    TOKEN = "token"
    """Specifies the token attribute"""
    TIMESTAMP = "timestamp"
    """Specifies the timestamp attribute"""
    ID = "account_id"
    """Specifies the id attribute"""
    COLUMNS = [NAME, PASSWORD, EMAIL, STATUS, TOKEN, TIMESTAMP, ID]
    """Organizes the name, password, email, status, token, timestamp, and id variables into an array"""
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    """Creates an explicit version of the name variable"""
    EXPLICIT_PASSWORD = f"{TABLE}.{PASSWORD}"
    """Creates an explicit version of the password variable"""
    EXPLICIT_EMAIL = f"{TABLE}.{EMAIL}"
    """Creates an explicit version of the email variable"""
    EXPLICIT_STATUS = f"{TABLE}.{STATUS}"
    """Creates an explicit version of the status variable"""
    EXPLICIT_TOKEN = f"{TABLE}.{TOKEN}"
    """Creates an explicit version of the token variable"""
    EXPLICIT_TIMESTAMP = f"{TABLE}.{TIMESTAMP}"
    """Creates an explicit version of the timestamp variable"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the id variable"""
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_PASSWORD, EXPLICIT_EMAIL, EXPLICIT_STATUS,
                        EXPLICIT_TOKEN, EXPLICIT_TIMESTAMP, EXPLICIT_ID]
    """Organizes the explicit versions of the variables above into an array"""

    def __init__(self, username: str, password: str, email: str, status: str = "N",
                 token: str = "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))", timestamp: str = "NOW()",
                 account_id: int = None):
        """initializes the username, password, email, status, token, timestamp, and account id variables"""
        self.username = username
        self.password = password
        self.email = email
        self.status = status
        self.token = token
        self.timestamp = str(timestamp)
        self.account_id = int(account_id) if account_id is not None else None

    def __str__(self):
        """returns a formatted string version of the variables"""
        return "[Account    ]               :USERNAME: {:<12} PASSWORD: {:<12} EMAIL: {:<12} STATUS: {:<2} " \
               "TOKEN: {:<20} TIMESTAMP: {:<12} Account_ID: {:<8}"\
            .format(self.username, self.password, self.email, self.status, self.token, self.timestamp, self.account_id)

    """Determines if explicit is true, if so return the explicit variables, if not return the normal versions"""
    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Account":
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

