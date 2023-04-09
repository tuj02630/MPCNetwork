try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

"""Manages the saving policy and settings of the system"""
class Saving_Policy(Data):
    TABLE = "Saving_Policy"
    """Specifies the Saving_Policy attribute"""
    ID = "saving_policy_id"
    """Specifies the saving_policy_id attribute"""
    MAX_TIME = "max_time"
    """Specifies the max_time attribute"""
    RESOLUTION_NAME = "resolution_name"
    """Specifies the resolubtion_name attribute"""
    COLUMNS = [ID, MAX_TIME, RESOLUTION_NAME]
    """Organizes the id, max time, and resolution name attributes in an array"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the id variable"""
    EXPLICIT_MAX_TIME = f"{TABLE}.{MAX_TIME}"
    """Creates an explicit version of the max time variable"""
    EXPLICIT_RESOLUTION_NAME = f"{TABLE}.{RESOLUTION_NAME}"
    """Creates an explicit version of the resolution name variable"""
    EXPLICIT_COLUMNS = [EXPLICIT_ID, EXPLICIT_MAX_TIME, EXPLICIT_RESOLUTION_NAME]
    """Organizes the explicit versions of the variables above into an array"""

    """Initializes the max time, resulution name, and saving policy id variables"""
    def __init__(self, max_time: int, resolution_name: str, saving_policy_id: int = None):
        self.max_time = int(max_time)
        self.resolution_name = resolution_name
        self.saving_policy_id = int(saving_policy_id) if saving_policy_id is not None else None

    """Returns a formatted string of the variables"""
    def __str__(self):
        return "[Saving_Policy  ]               :Max_Time: {:<12} Resolution_Name: {:<12} Saving_Policy_ID: {:<8}"\
            .format(self.max_time, self.resolution_name, self.saving_policy_id)

    """Determines if explicit is true, if so then return the explicit variables, if not return the normal ones"""
    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Saving_Policy":
        if explicit:
            return Saving_Policy(payload[Saving_Policy.EXPLICIT_MAX_TIME], payload[Saving_Policy.EXPLICIT_RESOLUTION_NAME], payload[Saving_Policy.EXPLICIT_ID])
        else:
            return Saving_Policy(payload[Saving_Policy.MAX_TIME], payload[Saving_Policy.RESOLUTION_NAME], payload[Saving_Policy.ID])