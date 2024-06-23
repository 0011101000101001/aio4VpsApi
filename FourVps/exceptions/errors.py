from typing import Union
from FourVps.exceptions.base import FourVPSBaseException


class UnknownError(Exception):
    def __init__(self):
        super().__init__('Unknown error!')


class AuthenticationError(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class NotAllFieldsHaveBeenTransferred(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class TariffNotAvailable(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class DataCenterNotAvailable(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class NeedVerification(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class NeedToContactWithSupport(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class NotEnoughMoney(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class IpPurchaseError(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class ServerNotFound(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class MaximumNumberOfIpAddresses(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class ServerCannotBeTurnedOn(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class ServerStoppedByAdministrator(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class TryAgain(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class CannotChangeToThisTariffPlan(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class CannotChangeTheCharacteristics(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class FailedToGetClusterInformation(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class ErrorAddingToScheduler(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class IncorrectBackupPeriod(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class IpError(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)


class BackupTaskNotFound(FourVPSBaseException):
    def __init__(self, error_message: str, data: Union[False, dict, list]):
        super().__init__(error_message, data)
