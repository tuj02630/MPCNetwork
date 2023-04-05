try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Account(Data):
    TABLE = "Account"
    NAME = "username"
    PASSWORD = "password"
    EMAIL = "email"
    STATUS = "status"
    TOKEN = "token"
    TIMESTAMP = "timestamp"
    ID = "account_id"
    COLUMNS = [NAME, PASSWORD, EMAIL, STATUS, TOKEN, TIMESTAMP, ID]
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_PASSWORD = f"{TABLE}.{PASSWORD}"
    EXPLICIT_EMAIL = f"{TABLE}.{EMAIL}"
    EXPLICIT_STATUS = f"{TABLE}.{STATUS}"
    EXPLICIT_TOKEN = f"{TABLE}.{TOKEN}"
    EXPLICIT_TIMESTAMP = f"{TABLE}.{TIMESTAMP}"
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_PASSWORD, EXPLICIT_EMAIL, EXPLICIT_STATUS,
                        EXPLICIT_TOKEN, EXPLICIT_TIMESTAMP, EXPLICIT_ID]

    def __init__(self, username: str, password: str, email: str, status: str = "N",
                 token: str = "md5(ROUND(UNIX_TIMESTAMP(CURTIME(4)) * 1000))", timestamp: str = "NOW()",
                 account_id: int = None):
        self.username = username
        self.password = password
        self.email = email
        self.status = status
        self.token = token
        self.timestamp = str(timestamp)
        self.account_id = int(account_id) if account_id is not None else None

    def __str__(self):
        return "[Account    ]               :USERNAME: {:<12} PASSWORD: {:<12} EMAIL: {:<12} STATUS: {:<2} " \
               "TOKEN: {:<20} TIMESTAMP: {:<12} Account_ID: {:<8}"\
            .format(self.username, self.password, self.email, self.status, self.token, self.timestamp, self.account_id)

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