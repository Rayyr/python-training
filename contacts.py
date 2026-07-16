# contact_book.py

import sys

# Contact book: dict of dicts
contacts = {}


# Add Contact
def add_contact(name, phone, email):
    contacts[name] = {
        "phone": phone,
        "email": email
    }
    print(f"Added {name}")


# Search by Name
def search_by_name(name):
    contact = contacts.get(name)   # safe access
    if contact:
        print(f"\n{name}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact['email']}")
    else:
        print("Contact not found")


# Search by Phone
def search_by_phone(phone):
    for name, info in contacts.items():  # iterate dict
        if info["phone"] == phone:
            print(f"\n{name}")
            print(f"Phone: {info['phone']}")
            print(f"Email: {info['email']}")
            return
    print("Contact not found")


# Show All Contacts
def show_all():
    if not contacts:
        print("No contacts available")
        return

    print("\nContact List:")
    print("=" * 30)
    for name, info in contacts.items():
        print(f"{name} → {info}")
    print("=" * 30)


# CLI Menu
def main():
    while True:
        print("\nContact Book")
        print("1. Add Contact")
        print("2. Search by Name")
        print("3. Search by Phone")
        print("4. Show All")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            add_contact(name, phone, email)

        elif choice == "2":
            name = input("Enter name: ")
            search_by_name(name)

        elif choice == "3":
            phone = input("Enter phone: ")
            search_by_phone(phone)

        elif choice == "4":
            show_all()

        elif choice == "5":
            print("Goodbye!")
            sys.exit()

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()