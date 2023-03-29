try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Hardware_has_Notification(Data):
    TABLE = "Hardware_has_Notification"
    HARDWARE_ID = "hardware_id"
    NOTIFICATION_ID = "NOTIFICATION_ID"
    COLUMNS = [HARDWARE_ID, NOTIFICATION_ID]
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    EXPLICIT_NOTIFICATION_ID = f"{TABLE}.{NOTIFICATION_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_HARDWARE_ID, EXPLICIT_NOTIFICATION_ID]

    def __init__(self, hardware_id: int, notification_id: int):
        self.hardware_id = int(hardware_id)
        self.notification_id = int(notification_id)

    def __str__(self):
        return "[Hardware_has_Notification  ]               :NOTIFICATION_ID: {:<12} HARDWARE_ID: {:<8}" \
            .format(self.hardware_id, self.notification_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Hardware_has_Notification":
        if explicit:
            return Hardware_has_Notification(
                payload[Hardware_has_Notification.EXPLICIT_HARDWARE_ID],
                payload[Hardware_has_Notification.EXPLICIT_NOTIFICATION_ID])
        else:
            return Hardware_has_Notification(
                payload[Hardware_has_Notification.HARDWARE_ID],
                payload[Hardware_has_Notification.NOTIFICATION_ID])