

try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

"""Manages the notifications the user gets from the system"""
class Hardware_has_Notification(Data):
    TABLE = "Hardware_has_Notification"
    """Specifies the Hardware_has_Notification table"""
    HARDWARE_ID = "hardware_id"
    """Specifies the hardware_id attribute"""
    NOTIFICATION_ID = "NOTIFICATION_ID"
    """Specifies the NOTIFICATION_ID attribute"""
    COLUMNS = [HARDWARE_ID, NOTIFICATION_ID]
    """Organizes the hardware id and notification id into an array"""
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    """Creates an explicit version of the hardware id variable"""
    EXPLICIT_NOTIFICATION_ID = f"{TABLE}.{NOTIFICATION_ID}"
    """Creates an explicit version of the notification id variable"""
    EXPLICIT_COLUMNS = [EXPLICIT_HARDWARE_ID, EXPLICIT_NOTIFICATION_ID]
    """Organizes the explicit version of the variables above into an array"""

    def __init__(self, hardware_id: int, notification_id: int):
        """Initializes the hardware id and notification id variables"""
        self.hardware_id = int(hardware_id)
        self.notification_id = int(notification_id)

    def __str__(self):
        """Returns a formatted string version of the variables"""
        return "[Hardware_has_Notification  ]               :NOTIFICATION_ID: {:<12} HARDWARE_ID: {:<8}" \
            .format(self.hardware_id, self.notification_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware_has_Notification":
        """If explicit is true, then return the explicit versio of the variables, if not, return the other version"""
        if explicit:
            return Hardware_has_Notification(
                payload[Hardware_has_Notification.EXPLICIT_HARDWARE_ID],
                payload[Hardware_has_Notification.EXPLICIT_NOTIFICATION_ID])
        else:
            return Hardware_has_Notification(
                payload[Hardware_has_Notification.HARDWARE_ID],
                payload[Hardware_has_Notification.NOTIFICATION_ID])



