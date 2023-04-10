try:
    from Database.Data.Data import Data
except:
    from Lambda.Database.Data.Data import Data

"""Manages the resolution of the video"""
class Resolution(Data):
    TABLE = "Resolution"
    """Specifies the Resolution table"""
    NAME = "resolution_name"
    """Specifies the resolution_name attribute of the table"""
    WIDTH = "width"
    """Specifies the width attribute which represents the width of the video screen"""
    HEIGHT = "height"
    """Specifies the height attribute which represents the height of the video screen"""
    COLUMNS = [NAME, WIDTH, HEIGHT]
    """Organizes the name, width, and height variables into an array"""
    EXPLICIT_NAME = f"{TABLE}.{NAME}"
    """Creates an explicit version of the name attribute"""
    EXPLICIT_WIDTH = f"{TABLE}.{WIDTH}"
    """Creates an explicit version of the width attribute"""
    EXPLICIT_HEIGHT = f"{TABLE}.{HEIGHT}"
    """Creates an explicit version of the height attribute"""
    EXPLICIT_COLUMNS = [EXPLICIT_NAME, EXPLICIT_WIDTH, EXPLICIT_HEIGHT]
    """Organizes the explicit version of the variables above into an array"""

    def __init__(self, resolution_name: str, width: int, height: int):
        """Initializes the resolution name, width, and height variables"""
        self.resolution_name = resolution_name
        self.width = int(width)
        self.height = int(height)

    def __str__(self):
        """Returns a formatted string version of the variables"""
        return "[Resolution    ]               :Resolution_Name: {:<12} Width: {:<12} Height: {:<8}"\
            .format(self.resolution_name, self.width, self.height)

    @staticmethod
    def dict_to_object(payload: dict, explicit: bool = False) -> "Resolution":
        """Determines if explicit is true, if true then return the explicit variables, if not then return the normal ones"""
        if explicit:
            return Resolution(payload[Resolution.EXPLICIT_NAME], payload[Resolution.EXPLICIT_WIDTH], payload[Resolution.EXPLICIT_HEIGHT])
        else:
            return Resolution(payload[Resolution.NAME], payload[Resolution.WIDTH], payload[Resolution.HEIGHT])

