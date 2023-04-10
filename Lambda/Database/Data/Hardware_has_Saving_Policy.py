try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

"""Manages the saving policy for the hardware components"""
class Hardware_has_Saving_Policy(Data):
    TABLE = "Hardware_has_Saving_Policy"
    """Specifies the Hardware_has_Saving_Policy table name"""
    HARDWARE_ID = "hardware_id"
    """Specifies the hardware_id attribute column name of the table"""
    SAVING_POLICY_ID = "saving_policy_id"
    """Specifies the saving_policy_id attribute column name of the table"""
    COLUMNS = [HARDWARE_ID, SAVING_POLICY_ID]
    """Organizes the hardware id and saving policy id into an array"""
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    """Creates an explicit version of the hardware id variable column name"""
    EXPLICIT_SAVING_POLICY_ID = f"{TABLE}.{SAVING_POLICY_ID}"
    """Creates an explicit version of the saving policy id variable column name"""
    EXPLICIT_COLUMNS = [EXPLICIT_HARDWARE_ID, EXPLICIT_SAVING_POLICY_ID]
    """Organizes the explicit version of the variables above into an array"""

    def __init__(self, hardware_id: int, saving_policy_id: int):
        """Initializes the hardware id and saving policy id variables"""
        self.hardware_id = int(hardware_id)
        """hardware_id      : int<      Specify the hardware_id of the Hardware_has_Saving_Policy."""
        self.saving_policy_id = int(saving_policy_id)
        """saving_policy_id : int<      Specify the saving_policy_id of the Hardware_has_Saving_Policy."""

    def __str__(self):
        """Returns a formatted string version of the variables"""
        return "[Hardware_has_Saving_Policy ]               :SAVING_POLICY_ID: {:<12} HARDWARE_ID: {:<8}" \
            .format(self.hardware_id, self.saving_policy_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware_has_Saving_Policy":
        """
            Determines if explicit is true, if so create Account with the explicit variables column name with payload,
            if not create object with the non-explicit variables column name with payload and return object

            Parameter:

                >payload    : dict<:    Payload that contains the information of object creation
                >explicit   : bool<:    Flag that indicates the payload key is explicit column

            Return:

                >object    : Hardware_has_Saving_Policy<: object created
        """
        if explicit:
            return Hardware_has_Saving_Policy(
                payload[Hardware_has_Saving_Policy.EXPLICIT_HARDWARE_ID],
                payload[Hardware_has_Saving_Policy.EXPLICIT_SAVING_POLICY_ID])
        else:
            return Hardware_has_Saving_Policy(
                payload[Hardware_has_Saving_Policy.HARDWARE_ID],
                payload[Hardware_has_Saving_Policy.SAVING_POLICY_ID])
