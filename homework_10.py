from collections import UserDict

class Field:
    pass

class Name(Field):
    def __init__(self, name):
        self.value = name

class Phone(Field):
    def __init__(self, phone):
        self.value = phone

class Record:
    def __init__(self, name, phones=None):
        self.name = Name(name)
        self.phones = phones if phones is not None else []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

class AddressBook(UserDict):
    def add_record(self, name, phones=None):
        record = Record(name, phones)
        self.data[record.name.value] = record



phone_book = AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input format. Please enter name and phone number separated by a space"
        except IndexError:
            return "Invalid command. Please try again"
    return inner

@input_error
def handle_input(command):
    return command.lower()

def add_contact(name, phone):
    record = Record(name, [phone]) 
    phone_book.add_record(name, [phone]) 
    return f"Contact {name} has been added with phone number {phone}"

def change_contact(name, current_phone, new_phone):
    if name in phone_book.data:
        phone_book.data[name].edit_phone(current_phone, new_phone)
        return f"Phone number for {name} has been updated to {new_phone}"
    else:
        return "Contact not found"

def find_contact(name):
    if name in phone_book.data:
        return ', '.join([phone.value for phone in phone_book.data[name].phones])
    else:
        return "Contact not found"

def show_all_contacts():
    output = ""
    for name, record in phone_book.data.items():
        phones = ', '.join([phone.value for phone in record.phones])
        output += f"{name}: {phones}\n"
    return output


def main():
    print("Hello! This CLI phone book assistant.")
    while True:
        command = input("> ")
        command = handle_input(command)
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            try:
                _, name, phone = command.split()
                print(add_contact(name, phone))
            except ValueError:
                print("Invalid input format. Please enter name and phone number separated by a space")
        elif command.startswith("change"):
            try:
                _, name, current_phone, new_phone = command.split()
                print(change_contact(name, current_phone, new_phone))
            except ValueError:
                print("Invalid input format. Please enter name and phone number separated by a space")
            except KeyError:
                print("Contact not found")
        elif command.startswith("phone"):
            try:
                _, name = command.split()
                print(find_contact(name))
            except KeyError:
                print("Contact not found")
        elif command == "show all":
            print(show_all_contacts())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again")


if __name__ == "__main__":
    main()