from typing import NoReturn
from FourVps.exceptions.errors import UnknownError, AuthenticationError, NotAllFieldsHaveBeenTransferred, \
    TariffNotAvailable, DataCenterNotAvailable, NeedVerification, NeedToContactWithSupport, NotEnoughMoney, \
    IpPurchaseError, ServerNotFound, MaximumNumberOfIpAddresses, ServerCannotBeTurnedOn, ServerStoppedByAdministrator, \
    TryAgain, CannotChangeToThisTariffPlan, CannotChangeTheCharacteristics, FailedToGetClusterInformation, \
    ErrorAddingToScheduler, IncorrectBackupPeriod, IpError, BackupTaskNotFound

errors_dict = {' ': UnknownError,
               'Authentication error': AuthenticationError,
               'Не все поля переданы!': NotAllFieldsHaveBeenTransferred,
               'В данном дата-центре приостановлены продажи этого тарифа!': TariffNotAvailable,
               'В данном дата-центре приостановлены продажи!': DataCenterNotAvailable,
               'Для заказа в этом дц необходима верификация профиля.': NeedVerification,
               'Ошибка покупки сервера, сообщите в службу поддержки код ошибки. #BS4': NeedToContactWithSupport,
               'На вашем балансе недостаточно денежных средств. #BS4': NotEnoughMoney,
               'На вашем балансе недостаточно денежных средств!': NotEnoughMoney,
               'Ошибка покупки IP-адреса #1': IpPurchaseError,
               'Сервер не найден!': ServerNotFound,
               'У вас максимальное количество IP адресов!': MaximumNumberOfIpAddresses,
               'Не удаётся включить сервер.': ServerCannotBeTurnedOn,
               'Ошибка, данный сервер остановлен администратором.': ServerStoppedByAdministrator,
               'Данного сервера нет в базе арендованных через API! #PO4': ServerNotFound,
               'Данного сервера нет в базе!': ServerNotFound,
               'Попробуйте ещё раз!': TryAgain,
               'Данного сервера нет в базе! #CS': ServerNotFound,
               'Данного сервера нет в базе! #DS4': ServerNotFound,
               'Не удаётся переустановить ОС, сообщите в службу поддержки! #REINSTALL4': NeedToContactWithSupport,
               'Данного сервера нет в базе арендованных через API! #REINSTALL4': ServerNotFound,
               'Ошибка, нельзя сменить на этот тарифный план!': CannotChangeToThisTariffPlan,
               'Недостаточно средств для смены характеристик. Не хватает:': NotEnoughMoney,
               'Недостаточно средств для добавления в планировщик резервного копирования. Не хватает:': NotEnoughMoney,
               'Вы не можете сменить характеристики этого сервера!': CannotChangeTheCharacteristics,
               'Сервер уже имеет максимальные характеристики!': CannotChangeTheCharacteristics,
               'Не удалось получить информацию о кластере!': FailedToGetClusterInformation,
               'Ошибка добавления в планировщик копирования!': ErrorAddingToScheduler,
               'Неверный период резервного копирования!': IncorrectBackupPeriod,
               'TARIF_ID or DC_ID is empty': NotAllFieldsHaveBeenTransferred,
               'Ошибка поиска сервера в базе.': ServerNotFound,
               'Возможно этот IP-адресс не Ваш, обратитесь в службу поддержки.': IpError,
               'Ошибка удаления IP-адреса, отправляем запрос об этом в логгер. #BIP2': IpError,
               'Ошибка для вашего сервера нет доступных тарифов для смены тарифа или вы использовали конфигуратор.': TariffNotAvailable,
               'Ошибка. Не найдена задача для резервного копирования услуги.': BackupTaskNotFound,

               }


def create_exception_by_api_message(response: dict) -> NoReturn:
    message = response.get('errorMessage', ' ')

    if isinstance(message, dict):
        message = response['errorMessage']['message']

    error = errors_dict.get(message, False)

    if not error:
        print('??>>?? ', response)
        for error_text in errors_dict:
            if message.startswith(error_text):
                raise errors_dict.get(error_text)(message, response['data'])

        raise errors_dict.get(' ')()

    raise error(message, response['data'])
