try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Notification(Data):
    """Manages the notifications sent to the user"""
    TABLE = "Notification"
    """Specifies the notification table"""
    TYPE = "notification_type"
    """Specifies the notification type attribute column name of the table"""
    ID = "notification_id"
    """Specifies the notification_id attribute column name of the table"""
    CRITERIA_ID = "criteria_id"
    """Specifies the criteria_id attribute column name of the table"""
    COLUMNS = [TYPE, CRITERIA_ID, ID]
    """Organizes the type, criteria id, and id variables into an array"""
    EXPLICIT_TYPE = f"{TABLE}.{TYPE}"
    """Creates an explicit version of the type attribute column name of the table"""
    EXPLICIT_ID = f"{TABLE}.{ID}"
    """Creates an explicit version of the id attribute column name of the table"""
    EXPLICIT_CRITERIA_ID = f"{TABLE}.{CRITERIA_ID}"
    """Creates an explicit version of the criteria id attribute column name of the table"""
    EXPLICIT_COLUMNS = [EXPLICIT_TYPE, EXPLICIT_ID, EXPLICIT_CRITERIA_ID]
    """Organizes the explicit version of the variables above into an array"""

    def __init__(self, notification_type: int, criteria_id: int, notification_id: int = None):
        """Initializes the notification type, criteria id, and notification id"""
        self.notification_type = int(notification_type)
        """notification_type    : string<   Store the notification_type of the notification"""
        self.criteria_id = int(criteria_id)
        """criteria_id          : string<   Store the criteria_id of the notification"""
        self.notification_id = int(notification_id) if notification_id is not None else None
        """criteria_id          : string<   Store the criteria_id of the notification"""

    def __str__(self):
        """Returns a formatted string of the variables"""
        return "[Notification   ]               :NOTIFICATION_TYPE: {:<12} CRITERIA_ID: {:<12} " \
               "NOTIFICATION_ID: {:<12}" \
            .format(self.notification_type, self.criteria_id, self.notification_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Notification":
        """
            Determines if explicit is true, if so create Account with the explicit variables column name with payload,
            if not create object with the non-explicit variables column name with payload and return object

            Parameter:

                >payload    : dict<:    Payload that contains the information of object creation
                >explicit   : bool<:    Flag that indicates the payload key is explicit column

            Return:

                >object    : Notification<: object created
        """
        if explicit:
            return Notification(payload[Notification.EXPLICIT_TYPE],
                                payload[Notification.EXPLICIT_CRITERIA_ID], payload[Notification.EXPLICIT_ID])
        else:
            return Notification(payload[Notification.TYPE],
                                payload[Notification.CRITERIA_ID], payload[Notification.ID])
