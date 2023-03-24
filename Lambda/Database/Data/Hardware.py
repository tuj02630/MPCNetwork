class Hardware:
    TABLE = "Hardware"
    NAME = "name"
    ID = "hardware_id"
    ACCOUNT_ID = "account_id"
    COLUMNS = [NAME, ID, ACCOUNT_ID]
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_ACCOUNT_ID = f"{TABLE}.{ACCOUNT_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_ID, EXPLICIT_ACCOUNT_ID]

    def __init__(self, name: str, hardware_id: int = None, account_id: int = None):
        self.name = name
        self.hardware_id = int(hardware_id) if hardware_id is not None else None
        self.account_id = int(account_id) if account_id is not None else None

    def __str__(self):
        return "[Hardware    ]               :NAME: {:<12} HARDWARE_ID:{:<12} ACCOUNT_ID: {:<8}".format(
            self.name, str(self.hardware_id), str(self.account_id)
        )

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware":
        if explicit:
            if Hardware.EXPLICIT_ACCOUNT_ID in payload:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_ID], payload[Hardware.EXPLICIT_ACCOUNT_ID])
            else:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_ID])
        else:
            if Hardware.ACCOUNT_ID in payload:
                return Hardware(payload[Hardware.NAME], payload[Hardware.ID], payload[Hardware.ACCOUNT_ID])
            else:
                return Hardware(payload[Hardware.NAME], payload[Hardware.ID])

    @staticmethod
    def list_dict_to_object_list(data_list: list[dict], explicit=False) -> list["Hardware"]:
        hardwares = []
        for hardware in data_list:
            hardwares.append(Hardware.dict_to_object(hardware, explicit))
        return hardwares