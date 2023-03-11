class Hardware:
    TABLE = "Hardware"
    NAME = "name"
    HARDWARE_ID = "hardware_id"
    CUSTOMER_ID = "customer_id"
    COLUMNS = [NAME, HARDWARE_ID, CUSTOMER_ID]
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_CUSTOMER_ID = f"{TABLE}.{CUSTOMER_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_HARDWARE_ID, EXPLICIT_CUSTOMER_ID]

    def __init__(self, name: str, hardware_id: int = None, customer_id: int = None):
        self.name = name
        self.hardware_id = hardware_id
        self.customer_id = customer_id
        self.data_list = [self.name, self.hardware_id, self.customer_id]

    def __str__(self):
        return "[Hardware    ]               :NAME: {:<12} HARDWARE_ID:{:<12} CUSTOMER_ID: {:<8}".format(
            self.name, str(self.hardware_id), str(self.customer_id)
        )

    @staticmethod
    def dict_to_customer(payload: dict, explicit=False) -> "Hardware":
        if explicit:
            if Hardware.EXPLICIT_CUSTOMER_ID in payload:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_HARDWARE_ID], payload[Hardware.EXPLICIT_CUSTOMER_ID])
            else:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_HARDWARE_ID])
        else:
            if Hardware.CUSTOMER_ID in payload:
                return Hardware(payload[Hardware.NAME], payload[Hardware.HARDWARE_ID], payload[Hardware.CUSTOMER_ID])
            else:
                return Hardware(payload[Hardware.NAME], payload[Hardware.HARDWARE_ID])

    @staticmethod
    def list_dict_to_customer_list(data_list: list[dict], explicit=False) -> list["Hardware"]:
        hardwares = []
        for hardware in data_list:
            hardwares.append(Hardware.dict_to_customer(hardware, explicit))
        return hardwares