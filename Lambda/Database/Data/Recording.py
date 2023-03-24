class Recording:
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

    def __init__(self,
                 file_name: str, date: str, timestamp: str,
                 recording_id: int = None, account_id: int = None, hardware_id: int = None):
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

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Recording":
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

    @staticmethod
    def list_dict_to_object_list(data_list: list[dict], explicit=False) -> list["Recording"]:
        recordings = []
        for recording in data_list:
            recordings.append(Recording.dict_to_object(recording, explicit))
        return recordings