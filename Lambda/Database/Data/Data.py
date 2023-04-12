
import inspect


class Data:
    """Manages the data from the database"""
    @staticmethod
    def object_to_dict(object: object) -> dict:
        """
            Receive object of subclass of Data and converts it into dictionary

            Parameter:

                >object     : object<:    object to be converted to dictionary

            Return:

                >dict<: Object in dictionary

        """
        if object is None:
            return {}
        else:
            return object.__dict__

    @staticmethod
    def list_object_to_dict_list(list_object: list[object]) -> list[dict]:
        """
            Receive list of object of subclass of Data and converts it into list of dictionary that represents the object

            Parameter:

                >list_object    : list[object]<:    list to be converted to list of dictionary

            Return:

                >list[dict]<    : List of data created
        """
        return [Data.object_to_dict(obj) for obj in list_object]

    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Data":
        """
            Receive payload generate object from it.

            Parameter:

                >payload        : dict<:    Payload that contains the information of object creation
                >explicit       : bool<:    Flag that indicates the payload key is explicit column

            Return:

                >list[Object]<    : object generated
        """
        raise NotImplemented("Not implemented")


    @classmethod
    def list_dict_to_object_list(cls, data_list: list[dict], explicit: bool = False) -> list[dict]:
        """"
            Receive list of payload generate list of object from it.

            Parameter:

                >payload        : list[dict]<:  list of payload that contains the information of list of object creation
                >explicit       : bool<:        Flag that indicates the payload key is explicit column

            Return:

                >list[Object]<    : List of object generated
        """
        data = []
        for d in data_list:
            data.append(cls.dict_to_object(d, explicit))
        return data
