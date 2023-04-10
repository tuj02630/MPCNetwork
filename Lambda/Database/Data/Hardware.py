try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

class Hardware(Data):
    """Manages the hardware components of the system"""
    TABLE = "Hardware"
    """Specifies the hardware table"""
    NAME = "name"
    """Specifies the name attribute"""
    ID = "hardware_id"
    """Specifies the hardware_id attribute"""
    ACCOUNT_ID = "account_id"
    """Specifies the account_id attribute"""
    RESOLUTION_NAME = "max_resolution"
    """Specifies the max_resolution attribute"""
    COLUMNS = [NAME, ID, ACCOUNT_ID, RESOLUTION_NAME]
    """organizes the name, id, account id, and resolution name into an array"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the id variable"""
    EXPLICIT_HARDWARE_ID = EXPLICIT_ID
    """Creates an explicit version of the hardware id variable"""
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    """Creates an explicit version of the name attribute"""
    EXPLICIT_ACCOUNT_ID = f"{TABLE}.{ACCOUNT_ID}"
    """Creates an explicit version of the account id variable"""
    EXPLICIT_RESOLUTION_NAME = f"{TABLE}.{RESOLUTION_NAME}"
    """Creates an explicit version of the resolution name variable"""
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_ID, EXPLICIT_ACCOUNT_ID, EXPLICIT_RESOLUTION_NAME]
    """Organizes the explicit versions of the variables above into an array"""

    def __init__(self, name: str, max_resolution: str, hardware_id: int = None, account_id: int = None):
        """Initializes the name, max resolution, hardware id, and account id variables"""
        self.name = name
        self.max_resolution = max_resolution
        self.hardware_id = int(hardware_id) if hardware_id is not None else None
        self.account_id = int(account_id) if account_id is not None else None

    def __str__(self):
        """Returns a formatted string of the variables"""
        return "[Hardware    ]               :NAME: {:<12} MAX_RESOLUTION: {:<12} HARDWARE_ID:{:<12} ACCOUNT_ID: {:<8}".format(
            self.name, self.max_resolution, str(self.hardware_id), str(self.account_id)
        )
    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware":
        """Determines if explicit is true, if so return the explicit variables, if not return the normal version"""
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

