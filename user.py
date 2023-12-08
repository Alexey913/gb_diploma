from datetime import date

class User:
    def __init__(self, login: str, email: str, password: str) -> None:
        self._email = email
        self._password = password
        self._login = email.split('@')[0]
        self._name: str = None
        self._surname: str = None
        self._patronymic: str = None
        self._gender: str = None
        self._bithday: date = None
        self._birth_place: Adress = None
        self._place_residence: Adress = None
        self._passport: Passport = None
        self._foreign_pass: Passport = None
        self._inn: Inn = None
        self._snils: Snils = None
        self._driver_license: DriverLicense  = None
        self._property = []
        self._education = []
        self._planning = []
        self._contacts: list[User] = None
        self._spouse: User = None
        self._children: list[User] = None
        self._gps_tracking = None