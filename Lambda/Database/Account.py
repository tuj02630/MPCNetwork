class Account:
    TABLE = "Account"
    USERNAME = "username"
    PASSWORD = "password"
    ACCOUNT_ID = "Account_id"
    COLUMNS = [USERNAME, PASSWORD, ACCOUNT_ID]
    EXPLICIT_USERNAME = f"{TABLE}.{USERNAME}"
    EXPLICIT_PASSWORD = f"{TABLE}.{PASSWORD}"
    EXPLICIT_ACCOUNT_ID = f"{TABLE}.{ACCOUNT_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_USERNAME, EXPLICIT_PASSWORD, EXPLICIT_ACCOUNT_ID]

    def __init__(self, username: str, password: str, account_id: int = None):
        self.username = username
        self.password = password
        self.Account_id = account_id
        self.data_list = [self.username, self.password, self.Account_id]

    def __str__(self):
        return "[Account    ]               :USERNAME: {:<12} PASSWORD: {:<12} Account_ID: {:<8}"\
            .format(self.username, self.password, self.Account_id)

    @staticmethod
    def dict_to_account(payload: dict, explicit=False) -> "Account":
        if explicit:
            return Account(payload[Account.EXPLICIT_USERNAME], payload[Account.EXPLICIT_PASSWORD], payload[Account.EXPLICIT_ACCOUNT_ID])
        else:
            return Account(payload[Account.USERNAME], payload[Account.PASSWORD], payload[Account.ACCOUNT_ID])

    @staticmethod
    def list_dict_to_account_list(data_list: list[dict], explicit=False) -> list["Account"]:
        accounts = []
        for account in data_list:
            accounts.append(Account.dict_to_account(account, explicit))
        return accounts