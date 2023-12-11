from datetime import date

class Passport:
    def __init__(self, series: int, number: int) -> None:
        self._series = series
        self._number = number
        self._name: str = None
        self._surname: str = None
        self._patronymic: str = None
        self._birthday: date = None
        self._birth_place: Adress = None
        self._place_residense: Adress = None
        self.gender = None
        self._date_registration: date = None
        self._id_inspection: int = None
        self._name_inspection: str = None