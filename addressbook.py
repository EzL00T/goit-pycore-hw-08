from collections import UserDict
from datetime import datetime, timedelta

# ====== Базове поле ======
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# ====== Ім'я контакту ======
class Name(Field):
    pass

# ====== Номер телефону ======
class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону має містити 10 цифр")
        super().__init__(value)

# ====== День народження ======
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Неправильний формат дати. Використовуйте DD.MM.YYYY")

# ====== Запис контакту ======
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = ", ".join(str(p) for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "немає"
        return f"{self.name.value} | Телефони: {phones} | День народження: {birthday}"

# ====== Адресна книга ======
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming = []
        today = datetime.today().date()
        next_week = today + timedelta(days=7)

        for record in self.data.values():
            if not record.birthday:
                continue
            birthday = record.birthday.value.replace(year=today.year)
            if today <= birthday <= next_week:
                upcoming.append(f"{record.name.value}: {birthday.strftime('%d.%m.%Y')}")
        return upcoming
