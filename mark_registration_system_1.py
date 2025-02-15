import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MarkRegistrationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Mark Registration System")
        self.root.geometry("1650x870")
        self.tree = ttk.Treeview(root)

        # Initialize database
        self.setup_database()
        self.update_table_mark('marks', 'obervation', 'varchar(255)')
        self.update_table_mark('program_info', 'admission_year', 'INTGER')

        # Variables
        self.marks_updated = False
        self.marks_viewed = False

        self.num_students = tk.IntVar()
        self.num_modules = tk.IntVar()

        self.module_code = tk.StringVar()
        self.module_name = tk.StringVar()
        self.coursework_1_mark = tk.IntVar()
        self.coursework_2_mark = tk.IntVar()
        self.coursework_3_mark = tk.IntVar()
        self.student_id = tk.StringVar()
        self.student_name = tk.StringVar()
        self.gender = tk.StringVar()
        self.date_of_entry = tk.StringVar()

        self.current_page = tk.Frame(self.root)
        self.current_page.pack()
        self.setup_navigation()
        self.show_home()

    def setup_database(self):
        conn = sqlite3.connect('marks.db')
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS program_info (
            id INTEGER PRIMARY KEY,
            num_students INTEGER,
            num_modules INTEGER
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY,
            module_code TEXT,
            module_name TEXT,
            coursework_1_mark INTEGER,
            coursework_2_mark INTEGER,
            coursework_3_mark INTEGER,
            student_id TEXT,
            student_name TEXT,
            gender TEXT,
            date_of_entry TEXT
        )
        ''')

        conn.commit()
        conn.close()
    def update_table_mark(self, table, my_column, column_type):
        try:
                conn = sqlite3.connect('marks.db')
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [info[1] for info in cursor.fetchall()]
                if my_column not in columns:
                    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {my_column} {column_type}")
                    conn.commit()
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}") 



    def setup_navigation(self):
        nav_frame = tk.Frame(self.root, bg="#0288d1")
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        nav_buttons = [
            ("Home", self.show_home),
            ("Input Marks", self.show_input_marks),
            ("View Marks", self.show_view_marks),
            ("Update Marks", self.show_update_marks),
            ("Visualisation", self.show_visualisation)
        ]

        for text, command in nav_buttons:
            btn = tk.Button(nav_frame, text=text, bg="#95B3D7", fg="#4682B4",
                            font=("Arial", 25, "bold"), command=command)
            btn.pack(side=tk.LEFT, padx=50, pady=20)

    def clear_content(self):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = tk.Frame(self.root)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_home(self):
        self.clear_content()

        tk.Label(self.current_page, text="Welcome to the Mark Registration System",
                 font=("Arial", 20), pady=30).pack()

        tk.Label(self.current_page, text="Number of Students:",
                 font=("Arial", 15)).pack(pady=10)
        tk.Entry(self.current_page, textvariable=self.num_students).pack(pady=10)

        tk.Label(self.current_page, text="Number of Modules:",
                 font=("Arial", 15)).pack(pady=10)
        tk.Entry(self.current_page, textvariable=self.num_modules).pack(pady=10)

        tk.Button(self.current_page, text="Save Records", command=self.save_records,
                  bg="#00bcd4", fg="black").pack(pady=40)

    def save_records(self):
        if not self.num_students.get() or not self.num_modules.get():
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            conn = sqlite3.connect('marks.db')
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO program_info (num_students, num_modules)
            VALUES (?, ?)
            ''', (self.num_students.get(), self.num_modules.get()))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Records saved successfully!")
            self.show_input_marks()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_input_marks(self):
        self.clear_content()

        tk.Label(self.current_page, text="Mark Entry Form",
                 font=("Arial", 20), pady=1).pack()

        self.create_form_entry("Module Code", self.module_code)
        self.create_form_entry("Module Name", self.module_name)
        self.create_form_entry("Coursework 1 Mark", self.coursework_1_mark)
        self.create_form_entry("Coursework 2 Mark", self.coursework_2_mark)
        self.create_form_entry("Coursework 3 Mark", self.coursework_3_mark)
        self.create_form_entry("Student ID", self.student_id)
        self.create_form_entry("Student Name", self.student_name)
        self.create_form_entry("Date of Entry", self.date_of_entry)

        tk.Label(self.current_page, text="Gender", font=("Arial", 12)).pack(pady=5)
        tk.Radiobutton(self.current_page, text="Male", variable=self.gender,
                       value="Male").pack()
        tk.Radiobutton(self.current_page, text="Female", variable=self.gender,
                       value="Female").pack()

        button_frame = tk.Frame(self.current_page)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Submit Marks", command=self.submit_marks,
                  bg="#00bcd4", fg="black").pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Reset", command=self.reset_form,
                  bg="#f44336", fg="black").pack(side=tk.LEFT, padx=10)

        # Next button (Initially Disabled)
        self.next_button = tk.Button(button_frame, text="Next", command=self.next_action,
                                     bg="#4CAF50", fg="white", state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=10)

    def create_form_entry(self, label_text, variable):
        tk.Label(self.current_page, text=label_text, font=("Arial", 12)).pack(pady=5)
        tk.Entry(self.current_page, textvariable=variable).pack(pady=5)

    def reset_form(self):
        self.module_code.set("")
        self.module_name.set("")
        self.coursework_1_mark.set(0)
        self.coursework_2_mark.set(0)
        self.coursework_3_mark.set(0)
        self.student_id.set("")
        self.student_name.set("")
        self.gender.set("")
        self.date_of_entry.set("")

    def submit_marks(self):
        if not all([self.module_code.get(), self.module_name.get(),
                    self.coursework_1_mark.get(), self.coursework_2_mark.get(),
                    self.coursework_3_mark.get(), self.student_id.get(),
                    self.student_name.get(), self.gender.get(),
                    self.date_of_entry.get()]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            # Debug statement to check coursework_1_mark value
            print(f"Coursework 1 Mark: {self.coursework_1_mark.get()}")

            conn = sqlite3.connect('marks.db')
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO marks (
                module_code, module_name, coursework_1_mark, coursework_2_mark,
                coursework_3_mark, student_id, student_name, gender, date_of_entry
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.module_code.get(), self.module_name.get(),
                self.coursework_1_mark.get(), self.coursework_2_mark.get(),
                self.coursework_3_mark.get(), self.student_id.get(),
                self.student_name.get(), self.gender.get(),
                self.date_of_entry.get()
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Marks submitted successfully!")

            # Enable the Next button
            self.next_button.config(state=tk.NORMAL)

            self.reset_form()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def next_action(self):
        self.show_view_marks()
        # You can add navigation logic here

    def show_view_marks(self):
        self.clear_content()
        self.marks_viewed = False  # Reset the viewed flag when entering the page

        tk.Label(self.current_page, text="View Marks", font=("Arial", 20), pady=10).pack()

        # Search feature
        tk.Label(self.current_page, text="Module Code:", font=("Arial", 12)).pack(pady=5)
        self.search_code = tk.Entry(self.current_page)
        self.search_code.pack(pady=5)

        # Frame for buttons (View & Next)
        button_frame = tk.Frame(self.current_page)
        button_frame.pack(pady=10)

        # View Button
        tk.Button(button_frame, text="View", command=self.search_marks, bg="#00bcd4", fg="black").pack(side=tk.LEFT,
                                                                                                       padx=10)

        # Next Button (Initially Disabled)
        self.next_button = tk.Button(button_frame, text="Next", command=self.next_page3,
                                     bg="#4CAF50", fg="white", state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=10)

        # Table for displaying marks
        self.tree = ttk.Treeview(self.current_page, columns=("Student ID", "Student Name", "Coursework 1 Mark",
                                                             "Coursework 2 Mark", "Coursework 3 Mark", "Total"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def search_marks(self):
        search_term = self.search_code.get().strip().lower()  # Trim spaces and convert to lowercase

        if not search_term:
            messagebox.showerror("Error", "Please enter a Module Code to search!")
            return

        try:
            conn = sqlite3.connect('marks.db')
            cursor = conn.cursor()

            cursor.execute('''
            SELECT student_id, student_name, coursework_1_mark, coursework_2_mark,
                   coursework_3_mark
            FROM marks
            WHERE LOWER(module_code) = ?
            ''', (search_term,))  # Search by module_code, not student_name

            results = cursor.fetchall()
            conn.close()

            for item in self.tree.get_children():
                self.tree.delete(item)

            if results:
                for row in results:
                    total = sum(row[2:5])  # Sum of coursework marks
                    self.tree.insert("", tk.END, values=(*row, total))
                self.marks_viewed = True
                self.next_button.config(state=tk.NORMAL)  # Enable "Next" button
                messagebox.showinfo("Success", "Records found and displayed!")
            else:
                self.marks_viewed = False
                self.next_button.config(state=tk.DISABLED)  # Keep "Next" disabled
                messagebox.showinfo("No Results", "No matching records found.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search database: {e}")

    def next_page3(self):
        if not self.marks_viewed:
            messagebox.showerror("Error", "You must view the marks before proceeding!")
            return
        self.show_update_marks()

    def show_update_marks(self):
        self.clear_content()
        self.marks_updated = False

        tk.Label(self.current_page, text="Modify Marks",
                 font=("Arial", 20), pady=30).pack()

        self.create_form_entries("Module Code", self.module_code)
        self.create_form_entries("Student ID", self.student_id)
        self.create_form_entries("Date of Entry", self.date_of_entry)
        self.create_form_entries("Coursework 1 Mark", self.coursework_1_mark)
        self.create_form_entries("Coursework 2 Mark", self.coursework_2_mark)
        self.create_form_entries("Coursework 3 Mark", self.coursework_3_mark)

        button_frame = tk.Frame(self.current_page)
        button_frame.pack(pady=50)

        tk.Button(button_frame, text="Search", command=self.search_mark,
                  bg="#00bcd4", fg="black").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Update", command=self.update_marks,
                  bg="#00bcd4", fg="black").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete", command=self.delete_record,
                  bg="red", fg="black").pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(button_frame, text="Next", command=self.go_to_visualization,
                                     bg="#4CAF50", fg="white")
        self.next_button.pack(side=tk.LEFT, padx=10)
        self.next_button.config(state=tk.DISABLED)

    def create_form_entries(self, label_text, variable):
        tk.Label(self.current_page, text=label_text, font=("Arial", 12)).pack(pady=5)
        tk.Entry(self.current_page, textvariable=variable).pack(pady=5)

    def search_mark(self):
        student_id = self.student_id.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a Student ID to search!")
            return

        try:
            conn = sqlite3.connect('marks.db')
            cursor = conn.cursor()

            cursor.execute('''
            SELECT * FROM marks WHERE student_id = ?
            ''', (student_id,))

            result = cursor.fetchone()
            conn.close()

            if result:
                self.module_code.set(result[1])
                self.date_of_entry.set(result[9])
                self.coursework_1_mark.set(result[3])
                self.coursework_2_mark.set(result[4])
                self.coursework_3_mark.set(result[5])
                messagebox.showinfo("Success", "Student record found and loaded.")
            else:
                messagebox.showinfo("Not Found", "No matching record found.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to search database: {e}")

    def update_marks(self):
        student_id = self.student_id.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a Student ID to update!")
            return

        try:
            conn = sqlite3.connect('marks.db')
            cursor = conn.cursor()

            cursor.execute('''
            UPDATE marks
            SET module_code = ?, date_of_entry = ?,
                coursework_1_mark = ?, coursework_2_mark = ?, coursework_3_mark = ?
            WHERE student_id = ?
            ''', (
                self.module_code.get(), self.date_of_entry.get(),
                self.coursework_1_mark.get(), self.coursework_2_mark.get(),
                self.coursework_3_mark.get(), student_id
            ))

            if cursor.rowcount > 0:
                conn.commit()
                self.marks_updated = True
                messagebox.showinfo("Success", "Marks updated successfully!")
                self.next_button.config(state=tk.NORMAL)  # Enable Next button
            else:
                messagebox.showwarning("Not Found", "Student ID not found in the database.")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update marks: {e}")

    def delete_record(self):
        student_id = self.student_id.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a Student ID to delete!")
            return

        try:
            conn = sqlite3.connect('marks.db')
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM marks WHERE student_id = ?
                ''', (student_id,))

            if cursor.rowcount > 0:
                conn.commit()
                messagebox.showinfo("Success", f"Student ID {student_id} deleted successfully!")
                # If deleting, disable the next button as there's nothing to visualize after delete
                self.next_button.config(state=tk.DISABLED)
            else:
                messagebox.showwarning("Not Found", "Student ID not found in the database.")

            conn.close()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete record: {e}")

    def go_to_visualization(self):
        if self.marks_updated:
            self.show_visualisation()  # Call your visualization page function
        else:
            messagebox.showwarning("Warning", "Please update the marks before proceeding to the visualization.")

    def show_visualisation(self):
        self.clear_content()

        # Create main container
        viz_frame = tk.Frame(self.current_page)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Module code selection
        input_frame = tk.Frame(viz_frame)
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="Enter Module Code:",
                 font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
        module_code_entry = tk.Entry(input_frame, font=("Arial", 14))
        module_code_entry.pack(side=tk.LEFT, padx=5)

        # Initialize graph index
        self.current_graph_index = 0

        def get_module_data(module_code):
            try:
                conn = sqlite3.connect('marks.db')
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT student_name, coursework_1_mark, coursework_2_mark, coursework_3_mark
                    FROM marks
                    WHERE module_code = ?
                    ''', (module_code,))

                results = cursor.fetchall()
                conn.close()

                if not results:
                    return None

                return [{
                    'Student Name': row[0],
                    'Coursework 1 Mark': row[1],
                    'Coursework 2 Mark': row[2],
                    'Coursework 3 Mark': row[3]
                } for row in results]

            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch data: {e}")
                return None

        def calculate_grade_distribution(total_marks):
            grades = {
                'A': 0,  # 70-100
                'B': 0,  # 60-69
                'C': 0,  # 50-59
                'D': 0,  # 40-49
                'F': 0  # 0-39
            }

            for mark in total_marks:
                if mark >= 70:
                    grades['A'] += 1
                elif mark >= 60:
                    grades['B'] += 1
                elif mark >= 50:
                    grades['C'] += 1
                elif mark >= 40:
                    grades['D'] += 1
                else:
                    grades['F'] += 1

            return grades

        def display_graph(module_data, graph_type):
            # Clear previous graph if exists
            for widget in graph_frame.winfo_children():
                widget.destroy()

            if not module_data:
                messagebox.showerror("Error", "No data available for visualization")
                return

            # Extract data
            student_names = [row['Student Name'] for row in module_data]
            coursework1 = [float(row['Coursework 1 Mark']) for row in module_data]
            coursework2 = [float(row['Coursework 2 Mark']) for row in module_data]
            coursework3 = [float(row['Coursework 3 Mark']) for row in module_data]
            total_marks = [sum(marks) for marks in zip(coursework1, coursework2, coursework3)]

            # Create figure
            fig = plt.Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)

            if graph_type == 'bar':
                ax.bar(student_names, total_marks, color='blue')
                ax.set_title('Total Marks by Student')
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Total Marks')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            elif graph_type == 'pie':
                grades = calculate_grade_distribution(total_marks)
                labels = []
                sizes = []
                colors = ['#2ecc71', '#3498db', '#f1c40f', '#e67e22', '#e74c3c']

                for grade, count in grades.items():
                    if count > 0:
                        labels.append(f'Grade {grade} ({count})')
                        sizes.append(count)

                if sum(sizes) > 0:
                    patches, texts, autotexts = ax.pie(sizes,
                                                       labels=labels,
                                                       colors=colors[:len(sizes)],
                                                       autopct='%1.1f%%',
                                                       startangle=90)
                    ax.set_title('Grade Distribution')
                    ax.axis('equal')
                else:
                    ax.text(0.5, 0.5, 'No grade data available',
                            horizontalalignment='center',
                            verticalalignment='center')

            elif graph_type == 'scatter':
                ax.scatter(range(len(student_names)), total_marks, color='orange')
                ax.set_xticks(range(len(student_names)))
                ax.set_xticklabels(student_names)
                ax.set_title('Marks Distribution')
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Total Marks')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            elif graph_type == 'line':
                ax.plot(student_names, total_marks, marker='o', color='yellow')
                ax.set_title('Marks Trend')
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Total Marks')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            fig.tight_layout()

            # Embed in tkinter window
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def submit():
            module_code = module_code_entry.get()
            if not module_code:
                messagebox.showerror("Error", "Please enter a module code")
                return

            module_data = get_module_data(module_code)
            if not module_data:
                messagebox.showerror("Error", "No data found for the provided module code")
                return

            # Display initial graph
            display_graph(module_data, 'bar')

            # Enable next graph button
            next_button.config(state=tk.NORMAL)

            # Store data for later use
            next_button.module_data = module_data

        def next_graph():
            graph_types = ['bar', 'line', 'scatter', 'pie']
            self.current_graph_index = (self.current_graph_index + 1) % len(graph_types)
            display_graph(next_button.module_data, graph_types[self.current_graph_index])

        # Create submit button
        tk.Button(input_frame, text="Submit", command=submit,
                  bg="#00bcd4", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Create graph frame
        graph_frame = tk.Frame(viz_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create next graph button (initially disabled)
        next_button = tk.Button(input_frame, text="Next Graph Type", command=next_graph,
                                bg="#4CAF50", fg="white", font=("Arial", 12), state=tk.DISABLED)
        next_button.pack(side=tk.LEFT, padx=5)

        # Create close button
        tk.Button(input_frame, text="Close", command=self.show_home,
                  bg="#f44336", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkRegistrationSystem(root)
    root.mainloop()
