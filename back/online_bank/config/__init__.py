import os

DEBT_ARRER = "0.1"
INIT_VALUE = "15"
ACTIVE_CARD_PERIOD_IN_YEARS = 6
PERCENT_SALE = -2
PERCENT_PURCHASE = 3
OFFSET_TIMEZONE = 3
LENGTH_CONFIRM_CODE = 6
INTERVAL_CONFIRM_CODE_IN_SECONDS = 200
INTERVAL_API_TOKEN_IN_SECONDS = 18000


class BankConfig:
    def __new__(cls, *args, **kwargs):
        return

    @staticmethod
    def get_bik():
        bik = os.environ.get("BIK")
        if bik is None:
            bik = os.environ["BIK"] = '044544512'
        return bik

    @staticmethod
    def get_bin():
        bin_ = os.environ.get("BIN")
        if bin_ is None:
            bin_ = os.environ["BIN"] = '59913'
        return bin_

    @staticmethod
    def _get_counter(name: str):
        counter = os.environ.get(name)
        if counter is None:
            counter = os.environ[name] = INIT_VALUE
        return int(counter)

    @staticmethod
    def _increment_counter(name: str):
        counter = os.environ.get(name)
        if counter is None:
            os.environ[name] = INIT_VALUE
        else:
            counter = str(int(counter) + 1)
            os.environ[name] = counter

    @classmethod
    def get_card_counter(cls):
        return cls._get_counter('CARD_COUNTER')

    @classmethod
    def get_account_counter(cls):
        return cls._get_counter('ACCOUNT_COUNTER')

    @classmethod
    def get_contract_counter(cls):
        return cls._get_counter('CONTRACT_COUNTER')

    @classmethod
    def increment_card_counter(cls):
        cls._increment_counter('CARD_COUNTER')

    @classmethod
    def increment_account_counter(cls):
        return cls._increment_counter('ACCOUNT_COUNTER')

    @classmethod
    def increment_contract_counter(cls):
        return cls._increment_counter('CONTRACT_COUNTER')


allow_currency_code = {'RUB': '810', 'AUD': '036', 'AZN': '944', 'GBP': '826', 'AMD': '051', 'BYN': '933', 'BGN': '975',
                       'BRL': '986', 'HUF': '348', 'VND': '704', 'HKD': '344', 'GEL': '981', 'DKK': '208', 'AED': '784',
                       'USD': '840', 'EUR': '978', 'EGP': '818', 'INR': '356', 'IDR': '360', 'KZT': '398', 'CAD': '124',
                       'QAR': '634', 'KGS': '417', 'CNY': '156', 'MDL': '498', 'NZD': '554', 'NOK': '578', 'PLN': '985',
                       'RON': '946', 'XDR': '960', 'SGD': '702', 'TJS': '972', 'THB': '764', 'TRY': '949', 'TMT': '934',
                       'UZS': '860', 'UAH': '980', 'CZK': '203', 'SEK': '752', 'CHF': '756', 'RSD': '941', 'ZAR': '710',
                       'KRW': '410', 'JPY': '392'}

allow_currency_name = {'RUB': 'Российский рубль', 'AUD': 'Австралийский доллар', 'AZN': 'Азербайджанский манат',
                       'GBP': 'Фунт стерлингов Соединенного королевства', 'AMD': 'Армянских драмов',
                       'BYN': 'Белорусский рубль', 'BGN': 'Болгарский лев', 'BRL': 'Бразильский реал',
                       'HUF': 'Венгерских форинтов', 'VND': 'Вьетнамских донгов', 'HKD': 'Гонконгский доллар',
                       'GEL': 'Грузинский лари', 'DKK': 'Датская крона', 'AED': 'Дирхам ОАЭ', 'USD': 'Доллар США',
                       'EUR': 'Евро', 'EGP': 'Египетских фунтов', 'INR': 'Индийских рупий',
                       'IDR': 'Индонезийских рупий', 'KZT': 'Казахстанских тенге', 'CAD': 'Канадский доллар',
                       'QAR': 'Катарский риал', 'KGS': 'Киргизских сомов', 'CNY': 'Китайский юань',
                       'MDL': 'Молдавских леев', 'NZD': 'Новозеландский доллар', 'NOK': 'Норвежских крон',
                       'PLN': 'Польский злотый', 'RON': 'Румынский лей', 'XDR': 'СДР (специальные права заимствования)',
                       'SGD': 'Сингапурский доллар', 'TJS': 'Таджикских сомони', 'THB': 'Таиландских батов',
                       'TRY': 'Турецких лир', 'TMT': 'Новый туркменский манат', 'UZS': 'Узбекских сумов',
                       'UAH': 'Украинских гривен', 'CZK': 'Чешских крон', 'SEK': 'Шведских крон',
                       'CHF': 'Швейцарский франк', 'RSD': 'Сербских динаров', 'ZAR': 'Южноафриканских рэндов',
                       'KRW': 'Вон Республики Корея', 'JPY': 'Японских иен'}

allow_payment_system = {
    "MasterCard": "5",
    "Visa": "4",
    "China Union Pay": "6",
    "МИР": "2",
}

allow_payment_system_list = [("MasterCard", "MasterCard"), ("Visa", "Visa"), ("China Union Pay", "China Union Pay"),
                             ("МИР", "МИР")]

SECRET_KEY = b"d618cb0c9ad5adf872886e7ad2cec1f96ccdc57a8b95b01b0eaa092ee445e618"
