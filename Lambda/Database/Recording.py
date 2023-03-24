class Recording:
    TABLE = "Recording"
    FILE_NAME = "file_name"
    DATE = "date"
    TIMESTAMP = "timestamp"
    RECORDING_ID = "recording_id"
    ACCOUNT_ID = "account_id"
    HARDWARE_ID = "hardware_id"
    COLUMNS = [FILE_NAME, DATE, TIMESTAMP, RECORDING_ID, ACCOUNT_ID, HARDWARE_ID]
    EXPLICIT_FILE_NAME = f"{TABLE}.{FILE_NAME}"
    EXPLICIT_DATE = f"{TABLE}.{DATE}"
    EXPLICIT_TIMESTAMP = f"{TABLE}.{TIMESTAMP}"
    EXPLICIT_RECORDING_ID = f"{TABLE}.{RECORDING_ID}"
    EXPLICIT_ACCOUNT_ID = f"{TABLE}.{ACCOUNT_ID}"
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    EXPLICIT_COLUMNS = [
        EXPLICIT_FILE_NAME, EXPLICIT_DATE, EXPLICIT_TIMESTAMP, EXPLICIT_RECORDING_ID, EXPLICIT_ACCOUNT_ID, EXPLICIT_HARDWARE_ID
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
        self.data_list = [self.file_name, self.date, self.timestamp, self.recording_id, self.account_id, self.hardware_id]

    def __str__(self):
        return "[Recording    ]               :FILE_NAME: {:<12} DATE: {:<12} TIMESTAMP {:<12} RECORDING_ID: {:<8} " \
               "ACCOUNT_ID: {:<8} HARDWARE_ID: {:<8}".format(self.file_name, self.date, self.timestamp,
                                                              self.recording_id, self.account_id, self.hardware_id)

    @staticmethod
    def dict_to_recording(payload: dict, explicit=False) -> "Recording":
        if explicit:
            return Recording(
                str(payload[Recording.EXPLICIT_FILE_NAME]),
                str(payload[Recording.EXPLICIT_DATE]),
                str(payload[Recording.EXPLICIT_TIMESTAMP]),
                payload[Recording.EXPLICIT_RECORDING_ID],
                payload[Recording.EXPLICIT_ACCOUNT_ID],
                payload[Recording.EXPLICIT_HARDWARE_ID])
        else:
            return Recording(
                str(payload[Recording.FILE_NAME]),
                str(payload[Recording.DATE]),
                str(payload[Recording.TIMESTAMP]),
                payload[Recording.RECORDING_ID],
                payload[Recording.ACCOUNT_ID],
                payload[Recording.HARDWARE_ID])

    @staticmethod
    def list_dict_to_recording_list(data_list: list[dict], explicit=False) -> list["Recording"]:
        recordings = []
        for recording in data_list:
            recordings.append(Recording.dict_to_recording(recording, explicit))
        return recordings