# contacts/manager.py

from .utils import load_contacts, save_contacts


class ContactManager:
    def __init__(self):
        self.contacts = load_contacts()

    #  Add
    def add_contact(self, name, phone, email):
        self.contacts[name] = {
            "phone": phone,
            "email": email
        }
        save_contacts(self.contacts)

    #  Search by name
    def search_by_name(self, name):
        return self.contacts.get(name)

    #  Search by phone
    def search_by_phone(self, phone):
        for name, info in self.contacts.items():
            if info["phone"] == phone:
                return name, info
        return None

    # Get all
    def get_all(self):
        return self.contacts