from datetime import date

class Inn:
    def __init__(self, number: str) -> None:
        self._number = number
        self._name: str = None
        self._surname: str = None
        self._patronymic: str = None
        self._birthday: date = None
        self._birth_place: Adress = None
        self.gender = None
        self._date_registration: date = None
        self._id_inspection: int = None
