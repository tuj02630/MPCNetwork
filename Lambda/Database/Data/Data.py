import inspect

class Data:
    @staticmethod
    def object_to_dict(object: object) -> dict:
        if object is None:
            return {}
        else:
            return object.__dict__

    @staticmethod
    def list_object_to_dict_list(list_object: list[object]) -> list:
        return [Data.object_to_dict(obj) for obj in list_object]

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Data":
        raise NotImplemented("Not implemented")

    @classmethod
    def list_dict_to_object_list(cls, data_list: list[dict], explicit=False) -> list[dict]:
        data = []
        for d in data_list:
            data.append(cls.dict_to_object(d, explicit))
        return data