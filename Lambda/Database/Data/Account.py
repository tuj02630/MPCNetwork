try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Account(Data):
    TABLE = "Account"
    NAME = "username"
    PASSWORD = "password"
    ID = "account_id"
    COLUMNS = [NAME, PASSWORD, ID]
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_PASSWORD = f"{TABLE}.{PASSWORD}"
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_PASSWORD, EXPLICIT_ID]

    def __init__(self, username: str, password: str, account_id: int = None):
        self.username = username
        self.password = password
        self.account_id = int(account_id) if account_id is not None else None

    def __str__(self):
        return "[Account    ]               :USERNAME: {:<12} PASSWORD: {:<12} Account_ID: {:<8}"\
            .format(self.username, self.password, self.account_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Account":
        if explicit:
            return Account(payload[Account.EXPLICIT_NAME], payload[Account.EXPLICIT_PASSWORD], payload[Account.EXPLICIT_ID])
        else:
            return Account(payload[Account.NAME], payload[Account.PASSWORD], payload[Account.ID])