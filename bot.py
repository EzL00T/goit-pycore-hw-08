from addressbook import AddressBook, Record
from addressbook import Phone, Birthday

# ====== Декоратор для обробки помилок ======
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Контакт не знайдено."
        except ValueError as e:
            return f"Помилка: {e}"
        except IndexError:
            return "Недостатньо аргументів."
    return wrapper

# ====== Команди ======
@input_error
def add_contact(args, book):
    name, phone = args[0], args[1]
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return f"Контакт {name} оновлено або створено."

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return f"Телефон для {name} змінено."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    return f"{name}: {', '.join(str(p) for p in record.phones)}"

@input_error
def show_all(book):
    if not book.data:
        return "Адресна книга порожня."
    return "\n".join(str(r) for r in book.data.values())

@input_error
def add_birthday(args, book):
    name, bday = args[0], args[1]
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_birthday(bday)
    return f"День народження для {name} додано."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record or not record.birthday:
        return "Немає інформації про день народження."
    return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(_, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Немає днів народження наступного тижня."
    return "\n".join(upcoming)

# ====== Парсинг команд ======
def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]
    return command, args

# ====== Головна функція ======
def main():
    book = AddressBook()
    print("Привіт! Я ваш віртуальний помічник.")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break
        elif command == "hello":
            print("Чим можу допомогти?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Невідома команда. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
