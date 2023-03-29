try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Hardware(Data):
    TABLE = "Hardware"
    NAME = "name"
    ID = "hardware_id"
    ACCOUNT_ID = "account_id"
    RESOLUTION_NAME = "max_resolution"
    COLUMNS = [NAME, ID, ACCOUNT_ID, RESOLUTION_NAME]
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_HARDWARE_ID = EXPLICIT_ID
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_ACCOUNT_ID = f"{TABLE}.{ACCOUNT_ID}"
    EXPLICIT_RESOLUTION_NAME = f"{TABLE}.{RESOLUTION_NAME}"
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_ID, EXPLICIT_ACCOUNT_ID, EXPLICIT_RESOLUTION_NAME]

    def __init__(self, name: str, max_resolution: str, hardware_id: int = None, account_id: int = None):
        self.name = name
        self.max_resolution = max_resolution
        self.hardware_id = int(hardware_id) if hardware_id is not None else None
        self.account_id = int(account_id) if account_id is not None else None

    def __str__(self):
        return "[Hardware    ]               :NAME: {:<12} MAX_RESOLUTION: {:<12} HARDWARE_ID:{:<12} ACCOUNT_ID: {:<8}".format(
            self.name, self.max_resolution, str(self.hardware_id), str(self.account_id)
        )

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware":
        if explicit:
            if Hardware.EXPLICIT_ACCOUNT_ID in payload:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_RESOLUTION_NAME],
                                payload[Hardware.EXPLICIT_ID], payload[Hardware.EXPLICIT_ACCOUNT_ID])
            else:
                return Hardware(payload[Hardware.EXPLICIT_NAME], payload[Hardware.EXPLICIT_RESOLUTION_NAME],
                                payload[Hardware.EXPLICIT_ID])
        else:
            if Hardware.ACCOUNT_ID in payload:
                return Hardware(payload[Hardware.NAME], payload[Hardware.RESOLUTION_NAME],
                                payload[Hardware.ID], payload[Hardware.ACCOUNT_ID])
            else:
                return Hardware(payload[Hardware.NAME], payload[Hardware.RESOLUTION_NAME],
                                payload[Hardware.ID])
