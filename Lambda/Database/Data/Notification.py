try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

"""Manages the the notifications sent to the user"""
class Notification(Data):
    TABLE = "Notification"
    """Specifies the notification table"""
    TYPE = "notification_type"
    """Specifies the notification type attribute"""
    ID = "notification_id"
    """Specifies the notification_id attribute"""
    CRITERIA_ID = "criteria_id"
    """Specifies the criteria_id attribute"""
    COLUMNS = [TYPE, CRITERIA_ID, ID]
    """Organizes the type, criteria id, and id variables into an array"""
    EXPLICIT_TYPE = f"{TABLE}.{TYPE}"
    """Creates an explicit version of the type attribute"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the id attribute"""
    EXPLICIT_CRITERIA_ID = f"{TABLE}.{CRITERIA_ID}"
    """Creates an explicit version of the criteria id attribute"""
    EXPLICIT_COLUMNS = [EXPLICIT_TYPE, EXPLICIT_ID, EXPLICIT_CRITERIA_ID]
    """Organizes the explicit version of the variables above into an array"""

    """Initializes the notification type, criteria id, and notification id"""
    def __init__(self, notification_type: int, criteria_id: int, notification_id: int = None):
        self.notification_type = int(notification_type)
        self.criteria_id = int(criteria_id)
        self.notification_id = int(notification_id) if notification_id is not None else None

    """Returns a formatted string of the variables"""
    def __str__(self):
        return "[Notification   ]               :NOTIFICATION_TYPE: {:<12} CRITERIA_ID: {:<12} " \
               "NOTIFICATION_ID: {:<12}" \
            .format(self.notification_type, self.criteria_id, self.notification_id)

    """Determines if explicit is true, if so then return the explicit variables, if not then return the normal ones"""
    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Notification":
        if explicit:
            return Notification(payload[Notification.EXPLICIT_TYPE],
                                payload[Notification.EXPLICIT_CRITERIA_ID], payload[Notification.EXPLICIT_ID])
        else:
            return Notification(payload[Notification.TYPE],
                                payload[Notification.CRITERIA_ID], payload[Notification.ID])
