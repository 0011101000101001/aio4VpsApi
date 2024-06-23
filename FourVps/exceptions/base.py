from typing import Union


class FourVPSBaseException(Exception):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        self.error_message = error_message
        self.data = data
        super().__init__(self.error_message)
