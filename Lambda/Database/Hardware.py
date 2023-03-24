class Hardware:
    TABLE = "Hardware"
    NAME = "name"
    HARDWARE_ID = "hardware_id"
    ACCOUNT_ID = "account_id"
    COLUMNS = [NAME, HARDWARE_ID, ACCOUNT_ID]
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_ACCOUNT_ID = f"{TABLE}.{ACCOUNT_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_HARDWARE_ID, EXPLICIT_ACCOUNT_ID]

    def __init__(self, name: str, hardware_id: int = None, account_id: int = None):
        self.name = name
        self.hardware_id = int(hardware_id) if hardware_id is not None else None
        self.account_id = int(account_id) if account_id is not None else None
        self.data_list = [self.name, self.hardware_id, self.account_id]

    def __str__(self):
        return "[Hardware    ]               :NAME: {:<12} HARDWARE_ID:{:<12} ACCOUNT_ID: {:<8}".format(
            self.name, str(self.hardware_id), str(self.account_id)
        )

    @staticmethod
    def dict_to_hardware(payload: dict, explicit=False) -> "Hardware":
        if explicit:
            if Hardware.EXPLICIT_ACCOUNT_ID in payload:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_HARDWARE_ID], payload[Hardware.EXPLICIT_account_id])
            else:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_HARDWARE_ID])
        else:
            if Hardware.ACCOUNT_ID in payload:
                return Hardware(payload[Hardware.NAME], payload[Hardware.HARDWARE_ID], payload[Hardware.ACCOUNT_ID])
            else:
                return Hardware(payload[Hardware.NAME], payload[Hardware.HARDWARE_ID])

    @staticmethod
    def list_dict_to_hardware_list(data_list: list[dict], explicit=False) -> list["Hardware"]:
        hardwares = []
        for hardware in data_list:
            hardwares.append(Hardware.dict_to_hardware(hardware, explicit))
        return hardwares