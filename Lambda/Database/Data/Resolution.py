class Resolution:
    TABLE = "Resolution"
    NAME = "resolution_name"
    WIDTH = "width"
    HEIGHT = "height"
    COLUMNS = [NAME, WIDTH, HEIGHT]
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    EXPLICIT_WIDTH = f"{TABLE}.{WIDTH}"
    EXPLICIT_HEIGHT = f"{TABLE}.{HEIGHT}"
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_WIDTH, EXPLICIT_HEIGHT]

    def __init__(self, resolution_name: str, width: int, height: int):
        self.resolution_name = resolution_name
        self.width = int(width)
        self.height = int(height)

    def __str__(self):
        return "[Resolution    ]               :Resolution_Name: {:<12} Width: {:<12} Height: {:<8}"\
            .format(self.resolution_name, self.width, self.height)

    @staticmethod
    def dict_to_object(payload: dict, explicit=False) -> "Resolution":
        if explicit:
            return Resolution(payload[Resolution.EXPLICIT_NAME], payload[Resolution.EXPLICIT_WIDTH], payload[Resolution.EXPLICIT_HEIGHT])
        else:
            return Resolution(payload[Resolution.NAME], payload[Resolution.WIDTH], payload[Resolution.HEIGHT])

    @staticmethod
    def list_dict_to_object_list(data_list: list[dict], explicit=False) -> list["Resolution"]:
        resolutions = []
        for resolution in data_list:
            resolutions.append(Resolution.dict_to_object(resolution, explicit))
        return resolutions
