class Saving_Policy:
    TABLE = "Saving_Policy"
    ID = "saving_policy_id"
    MAX_TIME = "max_time"
    RESOLUTION_NAME = "resolution_name"
    COLUMNS = [ID, MAX_TIME, RESOLUTION_NAME]
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_MAX_TIME = f"{TABLE}.{MAX_TIME}"
    EXPLICIT_RESOLUTION_NAME = f"{TABLE}.{RESOLUTION_NAME}"
    EXPLICIT_COLUMNS = [EXPLICIT_ID, EXPLICIT_MAX_TIME, EXPLICIT_RESOLUTION_NAME]

    def __init__(self, max_time: int, resolution_name: str, saving_policy_id: int = None):
        self.max_time = int(max_time)
        self.resolution_name = resolution_name
        self.saving_policy_id = int(saving_policy_id) if saving_policy_id is not None else None

    def __str__(self):
        return "[Saving_Policy  ]               :Max_Time: {:<12} Resolution_Name: {:<12} Saving_Policy_ID: {:<8}"\
            .format(self.max_time, self.resolution_name, self.saving_policy_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Saving_Policy":
        if explicit:
            return Saving_Policy(payload[Saving_Policy.EXPLICIT_MAX_TIME], payload[Saving_Policy.EXPLICIT_RESOLUTION_NAME], payload[Saving_Policy.EXPLICIT_ID])
        else:
            return Saving_Policy(payload[Saving_Policy.MAX_TIME], payload[Saving_Policy.RESOLUTION_NAME], payload[Saving_Policy.ID])

    @staticmethod
    def list_dict_to_object_list(data_list: list[dict], explicit=False) -> list["Saving_Policy"]:
        policies = []
        for policy in data_list:
            policies.append(Saving_Policy.dict_to_object(policy, explicit))
        return policies