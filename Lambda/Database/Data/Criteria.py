try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Criteria(Data):
    """Manages the user criteria for settings"""
    TABLE = "Criteria"
    """Specifies the Criteria table name"""
    MAGNITUDE = "magnitude"
    """Specifies the magnitude of the camera column name"""
    DURATION = "duration"
    """Specifies the duration of the recording column name"""
    ID = "criteria_id"
    """Specifies the criteria id for which criteria in the query column name"""
    TYPE = "criteria_type"
    """Specifies the type of criteria in question for the question column name"""
    COLUMNS = [MAGNITUDE, DURATION, TYPE, ID]
    """Organizes the magnitude, duration, type, and id into an array"""
    EXPLICIT_MAGNITUDE = f"{TABLE}.{MAGNITUDE}"
    """Creates an explicit version of the the magnitude variable column name"""
    EXPLICIT_DURATION = f"{TABLE}.{DURATION}"
    """Creates an explicit version of the duration variable column name"""
    EXPLICIT_TYPE = f"{TABLE}.{TYPE}"
    """Creates an explicit version of the type variable column name"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the ID variable column name"""
    EXPLICIT_COLUMNS = [EXPLICIT_MAGNITUDE, EXPLICIT_DURATION, EXPLICIT_TYPE, EXPLICIT_ID]
    """Organizes the explicit versions of the variables above into an array"""

    def __init__(self, criteria_type: int, magnitude: int, duration: int, criteria_id: int = None):
        """Initializes the type, magnitude, duration, and criteria variables"""
        self.criteria_type = int(criteria_type)
        """criteria_type  : string<   Store the criteria_type of the criteria"""
        self.magnitude = int(magnitude)
        """magnitude      : string<   Store the magnitude of the criteria"""
        self.duration = int(duration)
        """duration       : string<   Store the duration of the criteria"""
        self.criteria_id = int(criteria_id) if criteria_id is not None else None
        """criteria_id    : string<   Store the criteria_id of the criteria"""

    def __str__(self):
        """Returns a string that's a formatted version of all the variables"""
        return "[Criteria   ]               :TYPE: {:<8} MAGNITUDE: {:<12} DURATION: {:<12} CRITERIA_ID: {:<8}" \
            .format(self.criteria_type, self.magnitude, self.duration, self.criteria_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Criteria":
        """
            Determines if explicit is true, if so create Account with the explicit variables column name with payload,
            if not create Account with the non-explicit variables column name with payload and return object

            Parameter:

                >payload    : dict<:    Payload that contains the information of criteria creation
                >explicit   : bool<:    Flag that indicates the payload key is explicit column

            Return:

                >criteria    : Criteria<: Criteria created
        """
        if explicit:
            return Criteria(payload[Criteria.EXPLICIT_TYPE], payload[Criteria.EXPLICIT_MAGNITUDE],
                            payload[Criteria.EXPLICIT_DURATION], payload[Criteria.EXPLICIT_ID])
        else:
            return Criteria(payload[Criteria.TYPE], payload[Criteria.MAGNITUDE],
                            payload[Criteria.DURATION], payload[Criteria.ID])

