import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="admin",
    database="exam_system"
    )

cursor=db.cursor()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class ExamSystemApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Online Exam System")
        self.geometry("800x600")
        
        self.current_user = None
        self.role = None
        self.exam_duration = None
        self.time_remaining = None
        self.login_screen()

    def login_screen(self):
        self.clear_frame()
        
        header = ctk.CTkLabel(self, text="Welcome to the Exam System", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        login_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
        login_frame.pack(pady=20)
        
        username_label = ctk.CTkLabel(login_frame, text="Username", font=("Arial", 14))
        username_label.pack(pady=(20, 5))
        self.username_entry = ctk.CTkEntry(login_frame, width=250)
        self.username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(login_frame, text="Password", font=("Arial", 14))
        password_label.pack(pady=(10, 5))
        self.password_entry = ctk.CTkEntry(login_frame, width=250, show="*")
        self.password_entry.pack(pady=5)

        login_button = ctk.CTkButton(login_frame, text="Login", command=self.login, width=150)
        login_button.pack(pady=20)
        register_button = ctk.CTkButton(login_frame, text="Register", command=self.register_screen, width=150)
        register_button.pack(pady=10)

    def register_screen(self):
        self.clear_frame()

        header = ctk.CTkLabel(self, text="Register New Account", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        register_frame = ctk.CTkFrame(self, width=400, height=400, corner_radius=15)
        register_frame.pack(pady=20)

        username_label = ctk.CTkLabel(register_frame, text="Username", font=("Arial", 14))
        username_label.pack(pady=(20, 5))
        self.new_username_entry = ctk.CTkEntry(register_frame, width=250)
        self.new_username_entry.pack(pady=5)

        password_label = ctk.CTkLabel(register_frame, text="Password", font=("Arial", 14))
        password_label.pack(pady=(10, 5))
        self.new_password_entry = ctk.CTkEntry(register_frame, width=250, show="*")
        self.new_password_entry.pack(pady=5)

        role_label = ctk.CTkLabel(register_frame, text="Select Your Role", font=("Arial", 14))
        role_label.pack(pady=(10, 5))

        self.role_selection = ctk.StringVar(value="student")
        role_menu = ctk.CTkOptionMenu(
            register_frame,
            variable=self.role_selection,
            values=["student", "teacher"],
            width=175
        )
        role_menu.pack(pady=5)

        register_button = ctk.CTkButton(register_frame, text="Register", command=self.register, width=150)
        register_button.pack(pady=20)
        back_button = ctk.CTkButton(register_frame, text="Back to Login", command=self.login_screen, width=150)
        back_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT user_id, username, role FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            self.current_user, _, self.role = user
            if self.role == "teacher":
                self.teacher_dashboard()
            elif self.role == "student":
                self.student_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.role_selection.get()

        if role not in ["teacher", "student"]:
            messagebox.showerror("Error", "Role must be 'teacher' or 'student'")
            return
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        db.commit()
        messagebox.showinfo("Success", "Registration successful")
        self.login_screen()


    def create_exam_screen(self):
        self.clear_frame()  

        header = ctk.CTkLabel(self, text="Create New Exam", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        create_exam_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
        create_exam_frame.pack(pady=20)

        title_label = ctk.CTkLabel(create_exam_frame, text="Exam Title", font=("Arial", 14))
        title_label.pack(pady=(20, 5))
        self.exam_title_entry = ctk.CTkEntry(create_exam_frame, width=250)
        self.exam_title_entry.pack(pady=5)

        duration_label = ctk.CTkLabel(create_exam_frame, text="Duration (minutes)", font=("Arial", 14))
        duration_label.pack(pady=(10, 5))
        self.duration_entry = ctk.CTkEntry(create_exam_frame, width=250)
        self.duration_entry.pack(pady=5)

        save_button = ctk.CTkButton(create_exam_frame, text="Save Exam", command=self.save_exam, width=150)
        save_button.pack(pady=20)
        back_button = ctk.CTkButton(create_exam_frame, text="Back to Dashboard", command=self.teacher_dashboard, width=150)
        back_button.pack(pady=10)

    def save_exam(self):
        title = self.exam_title_entry.get()
        duration = self.duration_entry.get()
        cursor.execute("INSERT INTO exams (title, duration, created_by) VALUES (%s, %s, %s)",
                       (title, duration, self.current_user))
        db.commit()
        messagebox.showinfo("Success", "Exam created successfully")
        self.teacher_dashboard()

    def add_question_screen(self, exam_id):
        self.clear_frame()  

        header = ctk.CTkLabel(self, text="Add Question", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        question_label = ctk.CTkLabel(self, text="Question Text:")
        question_label.pack()
        question_entry = ctk.CTkEntry(self, width=400)
        question_entry.pack(pady=10)

        options = {}
        for opt in ["A", "B", "C", "D"]:
            opt_label = ctk.CTkLabel(self, text=f"Option {opt}:")
            opt_label.pack()
            options[opt] = ctk.CTkEntry(self, width=200)
            options[opt].pack(pady=5)

        correct_option_label = ctk.CTkLabel(self, text="Correct Option (A, B, C, or D):")
        correct_option_label.pack()
        correct_option_entry = ctk.CTkEntry(self, width=50)
        correct_option_entry.pack(pady=10)

        submit_button = ctk.CTkButton(self, text="Add Question", 
                                      command=lambda: self.add_question_to_db(exam_id, question_entry.get(), 
                                                                              options["A"].get(), options["B"].get(), 
                                                                              options["C"].get(), options["D"].get(), 
                                                                              correct_option_entry.get().upper()))
        submit_button.pack(pady=20)

        back_button = ctk.CTkButton(self, text="Back to Manage Exams", command=self.manage_exams_screen, width=150)
        back_button.pack(pady=10)

    def add_question_to_db(self, exam_id, question_text, option_a, option_b, option_c, option_d, correct_option):
        cursor.execute("""
            INSERT INTO test_questions (exam_id, question_text, option_a, option_b, option_c, option_d, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (exam_id, question_text, option_a, option_b, option_c, option_d, correct_option))
        db.commit()
        messagebox.showinfo("Question Added", "The question has been added successfully.")
        self.add_question_screen(exam_id)  


    def teacher_dashboard(self):
        self.clear_frame()
        
        header = ctk.CTkLabel(self, text="Teacher Dashboard", font=("Arial", 24, "bold"))
        header.pack(pady=20)
        
        dashboard_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
        dashboard_frame.pack(pady=20)

        ctk.CTkButton(dashboard_frame, text="Create Exam", command=self.create_exam_screen, width=200).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="Manage Exams", command=self.manage_exams_screen, width=200).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="View Student Results", command=self.teacher_view_results, width=200).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="Logout", command=self.login_screen, width=200).pack(pady=20)

    def take_exam_screen(self):
        self.clear_frame()  

        header = ctk.CTkLabel(self, text="Select Exam to Take", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        exam_selection_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
        exam_selection_frame.pack(pady=20)

        exam_label = ctk.CTkLabel(exam_selection_frame, text="Choose an Exam", font=("Arial", 14))
        exam_label.pack(pady=(20, 5))

        cursor.execute("SELECT exam_id, title FROM exams")
        exams = cursor.fetchall()
        self.exam_options = {f"{title}": exam_id for exam_id, title in exams}
        self.selected_exam = ctk.StringVar()
        
        if exams:
            self.selected_exam.set(list(self.exam_options.keys())[0])  
            exam_menu = ctk.CTkOptionMenu(exam_selection_frame, variable=self.selected_exam, values=list(self.exam_options.keys()))
            exam_menu.pack(pady=10)

            start_exam_button = ctk.CTkButton(exam_selection_frame, text="Start Exam", command=self.start_exam, width=150)
            start_exam_button.pack(pady=20)
        else:
            no_exam_label = ctk.CTkLabel(exam_selection_frame, text="No exams available.", font=("Arial", 14, "italic"))
            no_exam_label.pack(pady=10)

        back_button = ctk.CTkButton(exam_selection_frame, text="Back to Dashboard", command=self.student_dashboard, width=150)
        back_button.pack(pady=10)

    def start_exam(self):
        exam_id = self.exam_options[self.selected_exam.get()]

        cursor.execute("SELECT question_id, question_text, option_a, option_b, option_c, option_d FROM test_questions WHERE exam_id = %s", (exam_id,))
        self.questions = cursor.fetchall()

        cursor.execute("SELECT duration FROM exams WHERE exam_id = %s", (exam_id,))
        self.exam_duration = cursor.fetchone()[0] * 60  
        self.time_remaining = self.exam_duration  

        if not self.questions:
            messagebox.showinfo("No Questions", "This exam has no questions.")
            return

        self.current_question_index = 0
        self.answers = {}  
        self.exam_interface()  

    def exam_interface(self):
        self.clear_frame()

        timer_label = ctk.CTkLabel(self, text="", font=("Arial", 16))
        timer_label.pack(pady=10)
        self.update_timer(timer_label)  

        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            question_id, question_text, option_a, option_b, option_c, option_d = question_data

            question_label = ctk.CTkLabel(self, text=f"Q{self.current_question_index + 1}: {question_text}", font=("Arial", 16))
            question_label.pack(pady=20)

            self.selected_option = tk.StringVar()
            options = [("A", option_a), ("B", option_b), ("C", option_c), ("D", option_d)]
            for opt, text in options:
                option_radio = ctk.CTkRadioButton(self, text=f"{opt}: {text}", variable=self.selected_option, value=opt)
                option_radio.pack(pady=5)

            next_button = ctk.CTkButton(self, text="Next", command=self.save_answer)
            next_button.pack(pady=20)

            back_button = ctk.CTkButton(self, text="Cancel Exam", command=self.student_dashboard)
            back_button.pack(pady=10)
        else:
            self.finish_exam()

    def update_timer(self, timer_label):
        if timer_label.winfo_exists():
            if self.time_remaining > 0:
                mins, secs = divmod(self.time_remaining, 60)
                timer_label.configure(text=f"Time Remaining: {mins:02}:{secs:02}")
                self.time_remaining -= 1
                self.after(1000, self.update_timer, timer_label)
            else:
                self.finish_exam()
        else:
            print("Timer label no longer exists.")


    def save_answer(self):
        self.answers[self.questions[self.current_question_index][0]] = self.selected_option.get()
        self.current_question_index += 1
        self.exam_interface()  

    def finish_exam(self):
        self.clear_frame()

        score = self.calculate_score()
        cursor.execute("INSERT INTO student_results (user_id, exam_id, score, date_taken) VALUES (%s, %s, %s, NOW())", (self.current_user, self.exam_options[self.selected_exam.get()], score))
        db.commit()

        score_label = ctk.CTkLabel(self, text=f"Exam Finished! Your Score: {score}", font=("Arial", 20))
        score_label.pack(pady=20)

        back_button = ctk.CTkButton(self, text="Back to Dashboard", command=self.student_dashboard)
        back_button.pack(pady=20)

    def calculate_score(self):
        correct_count = 0
        for question_id, selected_answer in self.answers.items():
            cursor.execute("SELECT correct_option FROM test_questions WHERE question_id = %s", (question_id,))
            correct_option = cursor.fetchone()[0]
            if selected_answer == correct_option:
                correct_count += 1
        return (correct_count / len(self.questions)) * 100


    def manage_exams_screen(self):
        self.clear_frame()  

        header = ctk.CTkLabel(self, text="Manage Exams", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        manage_frame = ctk.CTkFrame(self, width=500, height=300, corner_radius=15)
        manage_frame.pack(pady=20)

        cursor.execute("SELECT exam_id, title FROM exams")
        exams = cursor.fetchall()

        if exams:
            for exam_id, title in exams:
                exam_label = ctk.CTkLabel(manage_frame, text=f"Exam: {title}", font=("Arial", 14))
                exam_label.pack(pady=5)

                add_question_button = ctk.CTkButton(
                manage_frame, text="Add Questions", command=lambda eid=exam_id: self.add_question_screen(eid), width=150
                )
                add_question_button.pack(pady=5)

                delete_button = ctk.CTkButton(
                manage_frame, text="Delete", command=lambda eid=exam_id: self.delete_exam(eid), width=100
                )
                delete_button.pack(pady=5)
        else:
            no_exams_label = ctk.CTkLabel(manage_frame, text="No exams available.", font=("Arial", 14, "italic"))
            no_exams_label.pack(pady=10)

        add_exam_button = ctk.CTkButton(manage_frame, text="Add New Exam", command=self.create_exam_screen, width=200)
        add_exam_button.pack(pady=20)

        back_button = ctk.CTkButton(manage_frame, text="Back to Dashboard", command=self.teacher_dashboard, width=150)
        back_button.pack(pady=20)

    def delete_exam(self, exam_id):
        cursor.execute("DELETE FROM exams WHERE exam_id = %s", (exam_id,))
        db.commit()
        messagebox.showinfo("Exam Deleted", f"Exam with ID {exam_id} has been deleted.")
        self.manage_exams_screen() 

    def teacher_view_results(self):
        self.clear_frame()

        header = ctk.CTkLabel(self, text="Student Exam Results", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        results_frame = ctk.CTkFrame(self, width=700, height=500, corner_radius=15)
        results_frame.pack(pady=20)

        cursor.execute("SELECT user_id, username FROM users WHERE role = 'student'")
        students = cursor.fetchall()

        self.student_options = {f"{username}": user_id for user_id, username in students}
        self.selected_student = ctk.StringVar()

        if students:
            self.selected_student.set(list(self.student_options.keys())[0])  
            student_menu = ctk.CTkOptionMenu(
                results_frame,
                variable=self.selected_student,
                values=list(self.student_options.keys()),
                width=200
            )
            student_menu.pack(pady=10)

            view_results_button = ctk.CTkButton(
                results_frame,
                text="View Results",
                command=self.display_student_results,
                width=150
            )
            view_results_button.pack(pady=10)
        else:
            no_students_label = ctk.CTkLabel(results_frame, text="No students available.", font=("Arial", 14, "italic"))
            no_students_label.pack(pady=10)

        back_button = ctk.CTkButton(results_frame, text="Back to Dashboard", command=self.teacher_dashboard, width=150)
        back_button.pack(pady=20)

    def display_student_results(self):
        self.clear_frame()

        header = ctk.CTkLabel(self, text=f"Results for {self.selected_student.get()}", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        results_frame = ctk.CTkFrame(self, width=700, height=500, corner_radius=15)
        results_frame.pack(pady=20)

        selected_student_id = self.student_options[self.selected_student.get()]

        cursor.execute("""
            SELECT exams.title, student_results.score, student_results.date_taken
            FROM student_results
            JOIN exams ON student_results.exam_id = exams.exam_id
            WHERE student_results.user_id = %s
            ORDER BY student_results.date_taken DESC
        """, (selected_student_id,))
        results = cursor.fetchall()

        if results:
            for exam_title, score, date_taken in results:
                result_label = ctk.CTkLabel(
                    results_frame,
                    text=f"Exam: {exam_title} | Score: {score} | Date: {date_taken}",
                    font=("Arial", 14),
                    anchor="w"
                )
                result_label.pack(fill="x", padx=20, pady=5)
        else:
            no_results_label = ctk.CTkLabel(results_frame, text="No results available for this student.", font=("Arial", 14, "italic"))
            no_results_label.pack(pady=10)

        back_button = ctk.CTkButton(results_frame, text="Back to Student List", command=self.teacher_view_results, width=150)
        back_button.pack(pady=20)

    def view_results_screen(self):
        self.clear_frame()  

        header = ctk.CTkLabel(self, text="Your Exam Results", font=("Arial", 24, "bold"))
        header.pack(pady=20)

        results_frame = ctk.CTkFrame(self, width=500, height=300, corner_radius=15)
        results_frame.pack(pady=20)

        cursor.execute("SELECT exam_id, score, date_taken FROM student_results WHERE user_id = %s", (self.current_user,))
        results = cursor.fetchall()

        if results:
            for exam_id, score, date_taken in results:
                cursor.execute("SELECT title FROM exams WHERE exam_id = %s", (exam_id,))
                exam_title = cursor.fetchone()[0]
                result_label = ctk.CTkLabel(
                    results_frame,
                    text=f"Exam: {exam_title} | Score: {score} | Date Taken: {date_taken}",
                    font=("Arial", 14)
                )
                result_label.pack(pady=5)
        else:
            no_results_label = ctk.CTkLabel(results_frame, text="No results available.", font=("Arial", 14, "italic"))
            no_results_label.pack(pady=10)

        back_button = ctk.CTkButton(results_frame, text="Back to Dashboard", command=self.return_to_dashboard, width=150)
        back_button.pack(pady=20)

    def return_to_dashboard(self):
        if self.role == "teacher":
            self.teacher_dashboard()
        elif self.role == "student":
            self.student_dashboard()

    def student_dashboard(self):
        self.clear_frame()
        
        header = ctk.CTkLabel(self, text="Student Dashboard", font=("Arial", 24, "bold"))
        header.pack(pady=20)
        
        dashboard_frame = ctk.CTkFrame(self, width=400, height=300, corner_radius=15)
        dashboard_frame.pack(pady=20)

        ctk.CTkButton(dashboard_frame, text="Take Exam", command=self.take_exam_screen, width=200).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="View Results", command=self.view_results_screen, width=200).pack(pady=10)
        ctk.CTkButton(dashboard_frame, text="Logout", command=self.login_screen, width=200).pack(pady=20)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

app = ExamSystemApp()
app.mainloop()
