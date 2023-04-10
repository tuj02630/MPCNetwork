try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

"""Manages the user criteria for settings"""


class Criteria(Data):
    TABLE = "Criteria"
    """Specifies the Criteria table"""
    MAGNITUDE = "magnitude"
    """Specifies the magnitude of the camera"""
    DURATION = "duration"
    """Specifies the duration of the recording"""
    ID = "criteria_id"
    """Specifies the criteria id for which criteria in the query"""
    TYPE = "criteria_type"
    """Specifies the type of criteria in question for the question"""
    COLUMNS = [MAGNITUDE, DURATION, TYPE, ID]
    """Organizes the magnitude, duration, type, and id into an array"""
    EXPLICIT_MAGNITUDE = f"{TABLE}.{MAGNITUDE}"
    """Creates an explicit version of the the magnitude variable"""
    EXPLICIT_DURATION = f"{TABLE}.{DURATION}"
    """Creates an explicit version of the duration variable"""
    EXPLICIT_TYPE = f"{TABLE}.{TYPE}"
    """Creates an explicit version of the type variable"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the ID variable"""
    EXPLICIT_COLUMNS = [EXPLICIT_MAGNITUDE, EXPLICIT_DURATION, EXPLICIT_TYPE, EXPLICIT_ID]
    """Organizes the explicit versions of the variables above into an array"""

    def __init__(self, criteria_type: int, magnitude: int, duration: int, criteria_id: int = None):
        """Initializes the type, magnitude, duration, and criteria variables"""
        self.criteria_type = int(criteria_type)
        self.magnitude = int(magnitude)
        self.duration = int(duration)
        self.criteria_id = int(criteria_id) if criteria_id is not None else None

    def __str__(self):
        """Returns a string that's a formatted version of all the variables"""
        return "[Criteria   ]               :TYPE: {:<8} MAGNITUDE: {:<12} DURATION: {:<12} CRITERIA_ID: {:<8}" \
            .format(self.criteria_type, self.magnitude, self.duration, self.criteria_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Criteria":
        """Returns the explicit version of the variables"""
        if explicit:
            return Criteria(payload[Criteria.EXPLICIT_TYPE], payload[Criteria.EXPLICIT_MAGNITUDE],
                            payload[Criteria.EXPLICIT_DURATION], payload[Criteria.EXPLICIT_ID])
        else:
            return Criteria(payload[Criteria.TYPE], payload[Criteria.MAGNITUDE],
                            payload[Criteria.DURATION], payload[Criteria.ID])

