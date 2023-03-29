try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Hardware_has_Saving_Policy(Data):
    TABLE = "Hardware_has_Saving_Policy"
    HARDWARE_ID = "hardware_id"
    SAVING_POLICY_ID = "saving_policy_id"
    COLUMNS = [HARDWARE_ID, SAVING_POLICY_ID]
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    EXPLICIT_SAVING_POLICY_ID = f"{TABLE}.{SAVING_POLICY_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_HARDWARE_ID, EXPLICIT_SAVING_POLICY_ID]

    def __init__(self, hardware_id: int, saving_policy_id: int):
        self.hardware_id = int(hardware_id)
        self.saving_policy_id = int(saving_policy_id)

    def __str__(self):
        return "[Hardware_has_Saving_Policy ]               :SAVING_POLICY_ID: {:<12} HARDWARE_ID: {:<8}" \
            .format(self.hardware_id, self.saving_policy_id)

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