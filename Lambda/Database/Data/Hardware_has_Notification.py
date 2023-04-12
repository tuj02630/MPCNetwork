

try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Hardware_has_Notification(Data):
    """Manages the notifications the user gets from the system"""
    TABLE = "Hardware_has_Notification"
    """Specifies the Hardware_has_Notification table name"""
    HARDWARE_ID = "hardware_id"
    """Specifies the hardware_id attribute column name"""
    NOTIFICATION_ID = "NOTIFICATION_ID"
    """Specifies the NOTIFICATION_ID attribute column name"""
    COLUMNS = [HARDWARE_ID, NOTIFICATION_ID]
    """Organizes the hardware id and notification id into an array"""
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    """Creates an explicit version of the hardware id variable column name"""
    EXPLICIT_NOTIFICATION_ID = f"{TABLE}.{NOTIFICATION_ID}"
    """Creates an explicit version of the notification id variable column name"""
    EXPLICIT_COLUMNS = [EXPLICIT_HARDWARE_ID, EXPLICIT_NOTIFICATION_ID]
    """Organizes the explicit version of the variables above into an array"""

    def __init__(self, hardware_id: int, notification_id: int):
        """Initializes the hardware id and notification id variables"""
        self.hardware_id = int(hardware_id)
        """hardware_id      : int<      Specify the hardware_id of the object."""
        self.notification_id = int(notification_id)
        """notification_id  : int<      Specify the notification_id of the object."""

    def __str__(self):
        """Returns a formatted string version of the variables"""
        return "[Hardware_has_Notification  ]               :NOTIFICATION_ID: {:<12} HARDWARE_ID: {:<8}" \
            .format(self.hardware_id, self.notification_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware_has_Notification":
        """
            Determines if explicit is true, if so create Account with the explicit variables column name with payload,
            if not create Hardware with the non-explicit variables column name with payload and return object

            Parameter:

                >payload    : dict<:    Payload that contains the information of hardware creation
                >explicit   : bool<:    Flag that indicates the payload key is explicit column

            Return:

                >object    : Hardware_has_Notification<: object created
        """
        if explicit:
            return Hardware_has_Notification(
                payload[Hardware_has_Notification.EXPLICIT_HARDWARE_ID],
                payload[Hardware_has_Notification.EXPLICIT_NOTIFICATION_ID])
        else:
            return Hardware_has_Notification(
                payload[Hardware_has_Notification.HARDWARE_ID],
                payload[Hardware_has_Notification.NOTIFICATION_ID])



