class Recording:
    TABLE = "Recording"
    FILE_NAME = "file_name"
    DATE = "date"
    TIMESTAMP = "timestamp"
    RECORDING_ID = "recording_id"
    CUSTOMER_ID = "customer_id"
    HARDWARE_ID = "hardware_id"
    COLUMNS = [FILE_NAME, DATE, TIMESTAMP, RECORDING_ID, CUSTOMER_ID, HARDWARE_ID]
    EXPLICIT_FILE_NAME = f"{TABLE}.{FILE_NAME}"
    EXPLICIT_DATE = f"{TABLE}.{DATE}"
    EXPLICIT_TIMESTAMP = f"{TABLE}.{TIMESTAMP}"
    EXPLICIT_RECORDING_ID = f"{TABLE}.{RECORDING_ID}"
    EXPLICIT_CUSTOMER_ID = f"{TABLE}.{CUSTOMER_ID}"
    EXPLICIT_HARDWARE_ID = f"{TABLE}.{HARDWARE_ID}"
    EXPLICIT_COLUMNS = [
        EXPLICIT_FILE_NAME, EXPLICIT_DATE, EXPLICIT_TIMESTAMP, EXPLICIT_RECORDING_ID, EXPLICIT_CUSTOMER_ID, EXPLICIT_HARDWARE_ID
    ]

    def __init__(self,
                 file_name: str, date: str, timestamp: str,
                 recording_id: int = None, customer_id: int = None, hardware_id: int = None):
        self.file_name = file_name
        self.date = date
        self.timestamp = timestamp
        self.recording_id = recording_id
        self.customer_id = customer_id
        self.hardware_id = hardware_id
        self.data_list = [self.file_name, self.date, self.timestamp, self.recording_id, self.customer_id, self.hardware_id]

    def __str__(self):
        return "[Recording    ]               :FILE_NAME: {:<12} DATE: {:<12} TIMESTAMP {:<12} RECORDING_ID: {:<8} " \
               "CUSTOMER_ID: {:<8} HARDWARE_ID: {:<8}".format(self.file_name, self.date, self.timestamp,
                                                              self.recording_id, self.customer_id, self.hardware_id)

    @staticmethod
    def dict_to_customer(payload: dict, explicit=False) -> "Recording":
        if explicit:
            return Recording(
                str(payload[Recording.EXPLICIT_FILE_NAME]),
                str(payload[Recording.EXPLICIT_DATE]),
                str(payload[Recording.EXPLICIT_TIMESTAMP]),
                payload[Recording.EXPLICIT_RECORDING_ID],
                payload[Recording.EXPLICIT_CUSTOMER_ID],
                payload[Recording.EXPLICIT_HARDWARE_ID])
        else:
            return Recording(
                str(payload[Recording.FILE_NAME]),
                str(payload[Recording.DATE]),
                str(payload[Recording.TIMESTAMP]),
                payload[Recording.RECORDING_ID],
                payload[Recording.CUSTOMER_ID],
                payload[Recording.HARDWARE_ID])

    @staticmethod
    def list_dict_to_customer_list(data_list: list[dict], explicit=False) -> list["Recording"]:
        recordings = []
        for recording in data_list:
            recordings.append(Recording.dict_to_customer(recording, explicit))
        return recordings