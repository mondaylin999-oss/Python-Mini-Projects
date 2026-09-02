import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Path locking for database file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "vault.db")


class DatabaseManager:
    """Handles SQL operations (SQLite syntax is almost identical to Postgres!)."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_entry(self, website, username, password):
        self.cursor.execute(
            "INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
            (website, username, password)
        )
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT id, website, username, password FROM vault")
        return self.cursor.fetchall()

    def delete_entry(self, entry_id):
        self.cursor.execute("DELETE FROM vault WHERE id = ?", (entry_id,))
        self.conn.commit()


class PasswordVaultApp:
    """Handles the graphical user interface using Tkinter."""

    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Secure Password Vault")
        self.root.geometry("550x450")
        self.root.resizable(False, False)

        self.db = DatabaseManager()

        # --- TOP INPUT FRAME ---
        input_frame = tk.LabelFrame(root, text=" Add New Credential ", padx=10, pady=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        # Website Field
        tk.Label(input_frame, text="Website/Service:").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_website = tk.Entry(input_frame, width=25)
        self.entry_website.grid(row=0, column=1, pady=2)

        # Username Field
        tk.Label(input_frame, text="Username/Email:").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_user = tk.Entry(input_frame, width=25)
        self.entry_user.grid(row=1, column=1, pady=2)

        # Password Field
        tk.Label(input_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_pass = tk.Entry(input_frame, width=25, show="*")
        self.entry_pass.grid(row=2, column=1, pady=2)

        # Add Button
        btn_add = tk.Button(input_frame, text="➕ Save Entry", bg="#4CAF50", fg="white", command=self.save_credential)
        btn_add.grid(row=3, columnspan=2, pady=8)

        # --- BOTTOM DATA DISPLAY (TREEVIEW TABLE) ---
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("ID", "Website", "Username", "Password")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        # Define table column headers
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=30, anchor="center")
        self.tree.heading("Website", text="Website")
        self.tree.column("Website", width=140)
        self.tree.heading("Username", text="Username")
        self.tree.column("Username", width=160)
        self.tree.heading("Password", text="Password")
        self.tree.column("Password", width=140)

        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar for table
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Delete Action Button
        btn_delete = tk.Button(root, text="🗑️ Delete Selected Entry", bg="#f44336", fg="white", command=self.delete_credential)
        btn_delete.pack(pady=10)

        # Initial load of data from database into table
        self.load_data()

    def save_credential(self):
        """Action handler when user clicks 'Save Entry'."""
        site = self.entry_website.get().strip()
        user = self.entry_user.get().strip()
        pwd = self.entry_pass.get().strip()

        if not site or not user or not pwd:
            messagebox.showwarning("Missing Fields", "Please fill in all inputs before saving.")
            return

        self.db.add_entry(site, user, pwd)
        
        # Clear fields after saving
        self.entry_website.delete(0, tk.END)
        self.entry_user.delete(0, tk.END)
        self.entry_pass.delete(0, tk.END)

        messagebox.showinfo("Success", f"Credentials for '{site}' stored safely!")
        self.load_data()

    def load_data(self):
        """Clears the table view and reloads rows from database."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.fetch_all()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def delete_credential(self):
        """Deletes selected item in table from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a row in the table to delete.")
            return

        item_values = self.tree.item(selected_item)["values"]
        entry_id = item_values[0]
        site_name = item_values[1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete credentials for '{site_name}'?"):
            self.db.delete_entry(entry_id)
            self.load_data()


def main():
    root = tk.Tk()
    app = PasswordVaultApp(root)
    root.mainloop() # Launches the GUI application loop


if __name__ == "__main__":
    main()