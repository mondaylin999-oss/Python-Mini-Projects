import os
import sqlite3

# --- PATH LOCKING ---
# Forces contacts.db to be created inside the script's exact folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "contacts.db")


class ContactDatabase:
    """Handles all SQL database connections and table queries."""

    def __init__(self):
        # Create or connect to the SQLite database file
        self.conn = sqlite3.connect(DB_FILE)
        # The cursor is the tool used to execute SQL commands and fetch results
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Creates the 'contacts' table if it doesn't already exist."""
        query = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
        """
        self.cursor.execute(query)
        self.conn.commit()  # Save changes to disk

    def add_contact(self, name, phone, email):
        """Inserts a new row into the table using parameterized queries (prevents SQL Injection)."""
        query = "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)"
        self.cursor.execute(query, (name, phone, email))
        self.conn.commit()
        print(f"✅ Contact '{name}' added successfully!")

    def view_contacts(self):
        """Retrieves and prints all contacts stored in the database."""
        query = "SELECT * FROM contacts"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()  # Returns a list of tuples

        if not rows:
            print("\n📭 No contacts found in the database.")
            return

        print("\n" + "=" * 50)
        print(f"%-5s %-20s %-15s %-20s" % ("ID", "Name", "Phone", "Email"))
        print("-" * 50)
        for row in rows:
            contact_id, name, phone, email = row
            print(f"%-5d %-20s %-15s %-20s" % (contact_id, name, phone, email))
        print("=" * 50)

    def search_contact(self, search_term):
        """Searches for contacts matching a name pattern."""
        query = "SELECT * FROM contacts WHERE name LIKE ?"
        self.cursor.execute(query, (f"%{search_term}%",))
        rows = self.cursor.fetchall()

        if not rows:
            print(f"\n🔍 No contacts matching '{search_term}'.")
            return

        print(f"\n🔍 SEARCH RESULTS FOR '{search_term}':")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | Email: {row[3]}")

    def delete_contact(self, contact_id):
        """Deletes a contact by their unique Primary Key (ID)."""
        query = "DELETE FROM contacts WHERE id = ?"
        self.cursor.execute(query, (contact_id,))
        self.conn.commit()
        
        if self.cursor.rowcount > 0:
            print(f"🗑️ Contact ID #{contact_id} deleted successfully.")
        else:
            print(f"❌ No contact found with ID #{contact_id}.")

    def close(self):
        """Closes the database connection safely."""
        self.conn.close()


def main():
    db = ContactDatabase()

    while True:
        print("\n=== 📞 SQLITE CONTACT MANAGER ===")
        print("1. View All Contacts")
        print("2. Add New Contact")
        print("3. Search Contact by Name")
        print("4. Delete Contact by ID")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            db.view_contacts()
        elif choice == "2":
            name = input("Enter Name: ").strip()
            phone = input("Enter Phone Number: ").strip()
            email = input("Enter Email (optional): ").strip() or "N/A"
            if name and phone:
                db.add_contact(name, phone, email)
            else:
                print("❌ Name and Phone are required fields!")
        elif choice == "3":
            search_term = input("Enter name to search: ").strip()
            if search_term:
                db.search_contact(search_term)
        elif choice == "4":
            try:
                contact_id = int(input("Enter Contact ID to delete: "))
                db.delete_contact(contact_id)
            except ValueError:
                print("❌ Please enter a valid numerical ID.")
        elif choice == "5":
            db.close()
            print("Database connection closed. See you tomorrow!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()