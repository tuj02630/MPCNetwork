import inspect

"""Manages the data from the database"""
class Data:
    @staticmethod
    def object_to_dict(object: object) -> dict:
        if object is None:
            return {}
        else:
            return object.__dict__

    """Returns a list of objects"""
    @staticmethod
    def list_object_to_dict_list(list_object: list[object]) -> list[dict]:
        return [Data.object_to_dict(obj) for obj in list_object]

    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Data":
        raise NotImplemented("Not implemented")

    """Loops through the new data and appends it to the existing data"""
    @classmethod
    def list_dict_to_object_list(cls, data_list: list[dict], explicit: bool = False) -> list[dict]:
        data = []
        for d in data_list:
            data.append(cls.dict_to_object(d, explicit))
        return data

    # @classmethod
    # def __getitem__(cls, item):
    #     return cls.__dict__[item]