try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

"""Manages the saving policy for the hardware components"""
class Hardware_has_Saving_Policy(Data):
    TABLE = "Hardware_has_Saving_Policy"
    """Specifies the Hardware_has_Saving_Policy table"""
    HARDWARE_ID = "hardware_id"
    """Specifies the hardware_id attribute of the table"""
    SAVING_POLICY_ID = "saving_policy_id"
    """Specifies the saving_policy_id attribute of the table"""
    COLUMNS = [HARDWARE_ID, SAVING_POLICY_ID]
    """Organizes the hardware id and saving policy id into an array"""
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    """Creates an explicit version of the hardware id variable"""
    EXPLICIT_SAVING_POLICY_ID = f"{TABLE}.{SAVING_POLICY_ID}"
    """Creates an explicit version of the saving policy id variable"""
    EXPLICIT_COLUMNS = [EXPLICIT_HARDWARE_ID, EXPLICIT_SAVING_POLICY_ID]
    """Organizes the explicit version of the variables above into an array"""

    """Initializes the hardware id and saving policy id variables"""
    def __init__(self, hardware_id: int, saving_policy_id: int):
        self.hardware_id = int(hardware_id)
        self.saving_policy_id = int(saving_policy_id)

    """Returns a formatted string version of the variables"""
    def __str__(self):
        return "[Hardware_has_Saving_Policy ]               :SAVING_POLICY_ID: {:<12} HARDWARE_ID: {:<8}" \
            .format(self.hardware_id, self.saving_policy_id)

    """Determines if the explicit variable is true, if so then return the explicit variables, if not return the normal version"""
    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware_has_Saving_Policy":
        if explicit:
            return Hardware_has_Saving_Policy(
                payload[Hardware_has_Saving_Policy.EXPLICIT_HARDWARE_ID],
                payload[Hardware_has_Saving_Policy.EXPLICIT_SAVING_POLICY_ID])
        else:
            return Hardware_has_Saving_Policy(
                payload[Hardware_has_Saving_Policy.HARDWARE_ID],
                payload[Hardware_has_Saving_Policy.SAVING_POLICY_ID])