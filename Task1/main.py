from collections import UserDict
import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Клас для зберігання імені контакту
    pass

class Phone(Field):
    # Клас для зберігання номера телефону з валідацією
    def __init__(self, value):
        # Перевіряємо правильність номера перед збереженням
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value):
        # Перевіряємо, що номер складається з 10 цифр
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError(
                "Введіть коректний номер телефону, він повинен містити 10 цифр"
            )

class Birthday(Field):
    def __init__(self, value):
        try:
            # Перетворюємо рядок на об'єкт datetime і перевіряємо формат
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    # Клас для зберігання контакту з іменем, телефонами та днем народження
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        # Додаємо телефон до списку
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Видаляємо телефон зі списку
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        # Замінюємо старий номер на новий
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def add_birthday(self, birthday):
        # Додаємо день народження
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        # Рахуємо дні до наступного дня народження, якщо він встановлений
        if self.birthday:
            today = datetime.today().date()
            next_birthday = self.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = self.birthday.value.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None

    def __str__(self):
        # Повертає інформацію про контакт у вигляді рядка
        phones = "; ".join(p.value for p in self.phones)
        birthday = str(self.birthday) if self.birthday else "Not set"
        return (
            f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"
        )

class AddressBook(UserDict):
    # Клас для зберігання адресної книги
    def add_record(self, record):
        # Додаємо новий контакт до адресної книги за ім'ям контакту
        self.data[record.name.value] = record

    def find(self, name):
        # Шукаємо контакт за ім'ям
        return self.data.get(name, None)

    def delete(self, name):
        # Видаляємо контакт за ім'ям
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        # Визначаємо поточну дату
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        first_day_of_next_week = next_week - timedelta(days=next_week.weekday())

        # Створюємо список привітань
        upcoming_birthdays = []

        # Перебираємо всі записи в адресній книзі
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year).date()  # Приводимо до типу date
                if birthday_this_year < today:
                    birthday_this_year = record.birthday.value.replace(year=today.year + 1).date()  # Приводимо до типу date

                if today <= birthday_this_year <= next_week:
                    if birthday_this_year.weekday() <= 4:
                        upcoming_birthdays.append({
                            "name": record.name.value,
                            "congratulation_date": birthday_this_year.strftime("%Y.%m.%d"),
                        })
                    elif birthday_this_year.weekday() in {5, 6}:
                        upcoming_birthdays.append({
                            "name": record.name.value,
                         "congratulation_date": first_day_of_next_week.strftime("%Y.%m.%d"),
                        })

        # Повертаємо список привітань
        return sorted(upcoming_birthdays, key=lambda x: x["congratulation_date"])