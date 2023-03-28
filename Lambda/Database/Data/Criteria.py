class Criteria:
    TABLE = "Criteria"
    MAGNITUDE = "magnitude"
    DURATION = "duration"
    TYPE = "criteria_type"
    COLUMNS = [MAGNITUDE, DURATION, TYPE]
    EXPLICIT_MAGNITUDE = f"{TABLE}.{MAGNITUDE}"
    EXPLICIT_DURATION = f"{TABLE}.{DURATION}"
    EXPLICIT_TYPE = f"{TABLE}.{TYPE}"
    EXPLICIT_COLUMNS = [EXPLICIT_MAGNITUDE, EXPLICIT_DURATION, EXPLICIT_TYPE]

    def __init__(self, criteria_type: int, magnitude: int, duration: int):
        self.criteria_type = int(criteria_type)
        self.magnitude = int(magnitude)
        self.duration = int(duration)

    def __str__(self):
        return "[Criteria   ]               :TYPE: {:<8} MAGNITUDE: {:<12} DURATION: {:<12}"\
            .format(self.criteria_type, self.magnitude, self.duration)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Criteria":
        if explicit:
            return Criteria(payload[Criteria.EXPLICIT_TYPE], payload[Criteria.EXPLICIT_MAGNITUDE], payload[Criteria.EXPLICIT_DURATION])
        else:
            return Criteria(payload[Criteria.TYPE], payload[Criteria.MAGNITUDE], payload[Criteria.DURATION])

    @staticmethod
    def list_dict_to_object_list(data_list: list[dict], explicit=False) -> list["Criteria"]:
        criteria = []
        for c in data_list:
            criteria.append(Criteria.dict_to_object(c, explicit))
        return criteria