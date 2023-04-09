try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data


class Recording(Data):
    TABLE = "Recording"
    NAME = "file_name"
    DATE = "date"
    TIMESTAMP = "timestamp"
    ID = "recording_id"
    ACCOUNT_ID = "account_id"
    HARDWARE_ID = "hardware_id"
    COLUMNS = [NAME, DATE, TIMESTAMP, ID, ACCOUNT_ID, HARDWARE_ID]
    EXPLICIT_FILE_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_DATE = f"{TABLE}.{DATE}"
    EXPLICIT_TIMESTAMP = f"{TABLE}.{TIMESTAMP}"
    EXPLICIT_ID = f"{TABLE}.{ID}"
    EXPLICIT_ACCOUNT_ID = f"{TABLE}.{ACCOUNT_ID}"
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    EXPLICIT_COLUMNS = [
        EXPLICIT_FILE_NAME, EXPLICIT_DATE, EXPLICIT_TIMESTAMP, EXPLICIT_ID, EXPLICIT_ACCOUNT_ID, EXPLICIT_HARDWARE_ID
    ]

    def __init__(self, file_name: str, date: str, timestamp: str, recording_id: int = None, account_id: int = None, hardware_id: int = None):
        self.file_name = file_name
        self.date = date
        self.timestamp = timestamp
        self.recording_id = int(recording_id) if recording_id is not None else None
        self.account_id = int(account_id) if account_id is not None else None
        self.hardware_id = int(hardware_id) if hardware_id is not None else None

    def __str__(self):
        return "[Recording    ]               :FILE_NAME: {:<12} DATE: {:<12} TIMESTAMP {:<12} RECORDING_ID: {:<8} " \
               "ACCOUNT_ID: {:<8} HARDWARE_ID: {:<8}".format(self.file_name, self.date, self.timestamp,
                                                              self.recording_id, self.account_id, self.hardware_id)

    def add_date_timestamp_from_query_para(self, queryPara: dict):
        year, month, date, hour, minute, second = (1990, 1, 1, 0, 0, 0)
        if "year" in queryPara:
            year = queryPara["year"]
        if "month" in queryPara:
            month = queryPara["month"]
        if "date" in queryPara:
            date = queryPara["date"]
        if "hour" in queryPara:
            hour = queryPara["hour"]
        if "minute" in queryPara:
            minute = queryPara["minute"]
        if "second" in queryPara:
            second = queryPara["second"]

        if "date" in queryPara:
            self.date = queryPara["date"]
        elif "year" in queryPara or "month" in queryPara or "date" in queryPara:
            self.date = f"{year}-{month}-{date}"
        else:
            self.date = "CURDATE()"

        if "timestamp" in queryPara:
            self.timestamp = queryPara["timestamp"]
        elif "year" in queryPara or "month" in queryPara or "date" in queryPara or "hour" in queryPara or "minute" in queryPara or "second" in queryPara:
            self.timestamp = f"{year}-{month}-{date} {hour}:{minute}:{second}"
        else:
            self.timestamp = "NOW()"

    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Recording":
        if explicit:
            return Recording(
                str(payload[Recording.EXPLICIT_FILE_NAME]),
                str(payload[Recording.EXPLICIT_DATE]),
                str(payload[Recording.EXPLICIT_TIMESTAMP]),
                payload[Recording.EXPLICIT_ID],
                payload[Recording.EXPLICIT_ACCOUNT_ID],
                payload[Recording.EXPLICIT_HARDWARE_ID])
        else:
            return Recording(
                str(payload[Recording.NAME]),
                str(payload[Recording.DATE]),
                str(payload[Recording.TIMESTAMP]),
                payload[Recording.ID],
                payload[Recording.ACCOUNT_ID],
                payload[Recording.HARDWARE_ID])