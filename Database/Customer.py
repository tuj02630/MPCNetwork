class Customer:
    TABLE = "Customer"
    USERNAME = "username"
    PASSWORD = "password"
    CUSTOMER_ID = "customer_id"
    COLUMNS = [USERNAME, PASSWORD, CUSTOMER_ID]
    EXPLICIT_USERNAME = f"{TABLE}.{USERNAME}"
    EXPLICIT_PASSWORD = f"{TABLE}.{PASSWORD}"
    EXPLICIT_CUSTOMER_ID = f"{TABLE}.{CUSTOMER_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_USERNAME, EXPLICIT_PASSWORD, EXPLICIT_CUSTOMER_ID]

    def __init__(self, username: str, password: str, customer_id: int = None):
        self.username = username
        self.password = password
        self.customer_id = customer_id
        self.data_list = [self.username, self.password, self.customer_id]

    def __str__(self):
        return "[Customer    ]               :USERNAME: {:<12} PASSWORD: {:<12} CUSTOMER_ID: {:<8}"\
            .format(self.username, self.password, self.customer_id)

    @staticmethod
    def dict_to_customer(payload: dict, explicit=False) -> "Customer":
        if explicit:
            return Customer(payload[Customer.EXPLICIT_USERNAME], payload[Customer.EXPLICIT_PASSWORD], payload[Customer.EXPLICIT_CUSTOMER_ID])
        else:
            return Customer(payload[Customer.USERNAME], payload[Customer.PASSWORD], payload[Customer.CUSTOMER_ID])

    @staticmethod
    def list_dict_to_customer_list(data_list: list[dict], explicit=False) -> list["Customer"]:
        customers = []
        for customer in data_list:
            customers.append(Customer.dict_to_customer(customer, explicit))
        return customers