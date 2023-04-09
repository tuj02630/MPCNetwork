try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Criteria(Data):

    TABLE = "Criteria"
    MAGNITUDE = "magnitude"
    DURATION = "duration"
    ID = "criteria_id"
    TYPE = "criteria_type"
    COLUMNS = [MAGNITUDE, DURATION, TYPE, ID]
    EXPLICIT_MAGNITUDE = f"{TABLE}.{MAGNITUDE}"
    EXPLICIT_DURATION = f"{TABLE}.{DURATION}"
    EXPLICIT_TYPE = f"{TABLE}.{TYPE}"
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_MAGNITUDE, EXPLICIT_DURATION, EXPLICIT_TYPE, EXPLICIT_ID]

    def __init__(self, criteria_type: int, magnitude: int, duration: int, criteria_id: int=None):
        self.criteria_type = int(criteria_type)
        self.magnitude = int(magnitude)
        self.duration = int(duration)
        self.criteria_id = int(criteria_id) if criteria_id is not None else None

    def __str__(self):
        return "[Criteria   ]               :TYPE: {:<8} MAGNITUDE: {:<12} DURATION: {:<12} CRITERIA_ID: {:<8}"\
            .format(self.criteria_type, self.magnitude, self.duration, self.criteria_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Criteria":
        if explicit:
            return Criteria(payload[Criteria.EXPLICIT_TYPE], payload[Criteria.EXPLICIT_MAGNITUDE],
                            payload[Criteria.EXPLICIT_DURATION], payload[Criteria.EXPLICIT_ID])
        else:
            return Criteria(payload[Criteria.TYPE], payload[Criteria.MAGNITUDE],
                            payload[Criteria.DURATION], payload[Criteria.ID])