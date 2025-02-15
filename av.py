import sqlite3
import tkinter as tk
from tkinter import messagebox


class MarkRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.setup_database()  # Now correctly calling the method inside the class

    def setup_database(self):
        try:
            conn = sqlite3.connect('marks.db')
            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS marks (
                student_id TEXT PRIMARY KEY,
                student_name TEXT,
                module_code TEXT,
                module_name TEXT,
                date_of_entry TEXT,
                coursework_1_mark INTEGER,
                coursework_2_mark INTEGER,
                coursework_3_mark INTEGER,
                gender TEXT
            )
            ''')

            # Check existing columns
            cursor.execute("PRAGMA table_info(marks);")
            existing_columns = [row[1] for row in cursor.fetchall()]

            # Ensure coursework_1_mark, coursework_2_mark, and coursework_3_mark exist
            missing_columns = []
            for col in ["coursework_1_mark", "coursework_2_mark", "coursework_3_mark"]:
                if col not in existing_columns:
                    missing_columns.append(col)

            # Add missing columns if needed
            for col in missing_columns:
                cursor.execute(f"ALTER TABLE marks ADD COLUMN {col} INTEGER;")
                print(f"Added missing column: {col}")

            conn.commit()
            conn.close()
            print("Database setup completed successfully.")

        except Exception as e:
            print(f"Database setup error: {e}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MarkRegistrationSystem(root)
    root.mainloop()
