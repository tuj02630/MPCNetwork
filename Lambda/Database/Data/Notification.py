try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Notification(Data):
    TABLE = "Notification"
    TYPE = "notification_type"
    ID = "notification_id"
    CRITERIA_ID = "criteria_id"
    COLUMNS = [TYPE, CRITERIA_ID, ID]
    EXPLICIT_TYPE = f"{TABLE}.{TYPE}"
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_CRITERIA_ID = f"{TABLE}.{CRITERIA_ID}"
    EXPLICIT_COLUMNS = [EXPLICIT_TYPE, EXPLICIT_ID, EXPLICIT_CRITERIA_ID]

    def __init__(self, notification_type: int, criteria_id: int, notification_id: int = None):
        self.notification_type = int(notification_type)
        self.criteria_id = int(criteria_id)
        self.notification_id = int(notification_id) if notification_id is not None else None

    def __str__(self):
        return "[Notification   ]               :NOTIFICATION_TYPE: {:<12} CRITERIA_ID: {:<12} " \
               "NOTIFICATION_ID: {:<12}" \
            .format(self.notification_type, self.criteria_id, self.notification_id)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Notification":
        if explicit:
            return Notification(payload[Notification.EXPLICIT_TYPE],
                                payload[Notification.EXPLICIT_CRITERIA_ID], payload[Notification.EXPLICIT_ID])
        else:
            return Notification(payload[Notification.TYPE],
                                payload[Notification.CRITERIA_ID], payload[Notification.ID])
