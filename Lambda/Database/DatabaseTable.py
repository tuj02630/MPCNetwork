"""Class that manages customers and their information"""
class DatabaseTable:
    @staticmethod
    def dict_to_customer(payload: dict, explicit=False) -> "DatabaseTable":
        return
    @staticmethod
    def list_dict_to_customer_list(data_list: list[dict], explicit=False) -> list["DatabaseTable"]:
        recordings = []
        for recording in data_list:
            recordings.append(DatabaseTable.dict_to_customer(recording, explicit))
        return recordings