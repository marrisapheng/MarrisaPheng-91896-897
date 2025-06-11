import tkinter as tk
from tkinter import messagebox

#Main window
root = tk.Tk()
root.title("Student Gradebook Manager")
root.geometry("1920x1080")
root.configure(bg="white")
root.withdraw()

#Menu window
def show_menu():
    #Close any exisiting menu window
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()
    menu_window = tk.Toplevel(root)
    menu_window.title("Menu")
    menu_window.geometry("1920x1080")
    menu_window.configure(bg="white")
    menu_window.grab_set()

    #Welcome message
    welcome_label = tk.Label(menu_window, text="Welcome to the Student Gradebook Manager!", bg="white", fg="navy", font=("arial bold", 50))
    welcome_label.place(x=230, y=150)

    #Instructions message
    instructions_label = tk.Label(menu_window, text="Please select an option below:", bg="white", fg="navy", font=("Arial", 30))
    instructions_label.place(x=525, y=210)

    #Menu buttons
    #View summary report button
    view_summary_report_button= tk.Button(menu_window, text= "View Summary Report", bg="white", fg="navy", font=("arial bold",15), command=lambda: [menu_window.destroy(), view_summary_report()])
    view_summary_report_button.place(x=530, y=300, width=200, height=50)
    #Submit summary report button
    submit_summary_report_button= tk.Button(menu_window, text= "Submit Summary Report", bg="white", fg="navy", font=("arial bold",15), command=lambda: [menu_window.destroy(), submit_summary_report()])
    submit_summary_report_button.place(x=730, y=300, width=200, height=50)
    #Close button
    close_button= tk.Button(menu_window, text= "Close", bg="white", fg="navy", font=("arial bold",15), command=lambda: [menu_window.destroy(), root.destroy()])
    close_button.place(x=655, y=350, width=150, height=40)

#Submit summary report
def submit_summary_report():
    submit_report= tk.Toplevel(root)
    submit_report.title("Submit Summary Report")
    submit_report.geometry("1920x1080")
    submit_report.configure(bg="white")
    submit_report.grab_set()

    #List for grades
    grades= []
    grade_widgets= []
    result_labels= []

    #Name and subjects question
    name_entry_label = tk.Label(submit_report, text= "Enter Your Name:", bg="white", fg="navy", font=("arial bold",15))
    name_entry_label.pack(pady=5)
    name_entry = tk.Entry(submit_report, bg="navy")
    name_entry.pack(pady=5)

    subjects_label = tk.Label(submit_report, text="Total Number of Subjects (1-5):", bg="white", fg="navy", font=("arial bold",15))
    subjects_label.pack(pady=5)
    subjects_entry = tk.Entry(submit_report, bg="navy")
    subjects_entry.pack(pady=5)

    def grade_entries():
        #Delete previous entries
        for widget in grade_widgets:
            widget.destroy()
        grade_widgets.clear()
        grades.clear()

        #Student name must be less than 30 characters
        student_name = name_entry.get().strip()
        if student_name == "" or len(student_name) > 30:
            messagebox.showerror("Invalid Input", "Name must be less than 30 characters.")
            return

        #Get number of subjects
        try:
            num_subjects= int(subjects_entry.get())
            if num_subjects <= 0 or num_subjects >=6:
                messagebox.showerror("Invalid Input", "Please enter a valid number of subjects.")
                subjects_entry.delete(0, tk.END)
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid, please enter a numeric value.")
            subjects_entry.delete(0, tk.END)
            return
        
        #Enter grade prompt
        for i in range(num_subjects):
            grade_label= tk.Label(submit_report, text= f"Enter Grade for Subject {i+1} (1-100):", bg="white", fg="navy", font=("arial bold",15))
            grade_label.pack(pady=5)
            grade_entry= tk.Entry(submit_report, bg="navy", fg="white")
            grade_entry.pack(pady=5)
            grades.append(grade_entry)
            grade_widgets.append(grade_label)
            grade_widgets.append(grade_entry)

        #Label to add clarity below grade entry prompt
        post_grade_entry_label = tk.Label(submit_report, text="Click the 'Submit Grades' button to continue.", bg="white", fg="navy", font=("arial bold", 15)) 
        post_grade_entry_label.pack(pady=5)
        grade_widgets.append(post_grade_entry_label)

        #Submit grades
        def submit_grades():
            for label in result_labels:
                label.destroy()
            result_labels.clear()
            try:
                grades_list= [float(grade.get()) for grade in grades]
                if any(grade < 0 or grade > 100 for grade in grades_list):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid grades between 0 and 100.")
                return

            #Calculate average grade
            average= sum(grades_list) / len(grades_list)
            average_label= tk.Label(submit_report,text= f"Average Grade: {average:.2f}", bg="white", fg="navy", font=("arial bold",15))
            average_label.place(x=900, y=100)

            student_name= name_entry.get()
            summary_text= f"Student Name: {student_name}, Average Grade: {average}\n"
            summary_label= tk.Label(submit_report, text= summary_text, bg="white", fg="navy", font=("arial bold",15))
            summary_label.place(x=900, y=50)

            #Save summary report to txt file
            def save_student_summary():
                student_name= name_entry.get().strip()
                if student_name == "" or len(student_name) > 30:
                    messagebox.showerror("Invalid", "Name must be less than 30 characters.")
                    return
                with open("student_records.txt", "a") as file:
                    file.write(f"Student Name: {student_name}, Average Grade: {average:.2f}\n")
                save_summary= tk.Label(submit_report, text= "Student summary report saved successfully!", bg="white", fg="navy", font=("arial bold",15))
                save_summary.place(x=900, y=200)
            #Save summary report button
            save_summary_report_button = tk.Button(submit_report, text= "Save Summary Report", bg="white", fg="navy", font=("arial bold",15), command=save_student_summary)
            save_summary_report_button.place(x=900, y=150)

        #Submit button
        submit_button= tk.Button(submit_report, text= "Submit Grades", bg="white", fg="navy",font=("arial bold",15), command=submit_grades)
        submit_button.place(width=140, height=30, x=665, y=650)
        grade_widgets.append(submit_button)

    #Button from entering subjects to entering grades
    next_button= tk.Button(submit_report, text= "Next", command=grade_entries, bg="white", fg="navy", font=("arial bold",15))
    next_button.place(width=140, height=30, x=665, y=700)

    #Return to menu button
    return_button= tk.Button(submit_report, text= "Return to Menu", bg="white", fg="navy", font=("arial bold",15), command=lambda: [submit_report.destroy(),show_menu()])
    return_button.place(width=140, height=30, x=665, y=750)


#View summary report
def view_summary_report():
    view_report= tk.Toplevel(root)
    view_report.title("View Summary Report")
    view_report.geometry("1920x1080")
    view_report.configure(bg="white")
    view_report.grab_set()

    #Enter student name prompt
    name_prompt_label= tk.Label(view_report, text="Enter Student Name:", bg="white", fg="navy", font=("arial bold",15))
    name_prompt_label.place(x=650, y=50)

    #Search student name
    search_name_entry= tk.Entry(view_report, bg="navy", fg="white")
    search_name_entry.place(x=650, y=80, width=200, height=30)

    #Result title
    result_title_label = tk.Label(view_report, text="Result:", bg="white", fg="navy", font=("arial bold", 15))
    result_title_label.place(x=650, y=120)
    #Result label
    result_text_box = tk.Text(view_report, bg="navy", fg="white", wrap="word", height=20, width=61, font=("Arial", 15))
    result_text_box.place(x=650, y=160)

    #Scrollbar for result text box
    scrollbar = tk.Scrollbar(view_report, command=result_text_box.yview)
    scrollbar.place(x=1300, y=160, height=400)
    result_text_box.config(yscrollcommand=scrollbar.set)

    #Search for student
    def search_student():
        student_name= search_name_entry.get().strip()
        if student_name== "" or len(student_name) >= 30:
            messagebox.showerror("Invalid Input", "Name must be less than 30 characters.")
            return

        try:
            with open("student_records.txt", "r") as file:
                student_found = []
                search_student_name = student_name.lower().strip()
                for line in file:
                    line_lower = line.lower().strip()
                    if line_lower.startswith(f"student name: {search_student_name},"):
                        student_found.append(line.strip())
                if student_found:
                    result_text = "\n".join(student_found)
                else:
                    result_text = "Student not found"
        except FileNotFoundError:
            result_text = "No student found"

        #Show results in text box
        result_text_box.config(state=tk.NORMAL)
        result_text_box.delete(1.0, tk.END)
        result_text_box.insert(tk.END, result_text)
        result_text_box.config(state=tk.DISABLED)


    #Search button
    search_button = tk.Button(view_report, text="Search", bg="white", fg="navy", font=("arial bold",15), command=search_student)
    search_button.place(x=650, y=550, width=140, height=30)

    #Return to menu button
    return_button = tk.Button(view_report, text="Return to Menu", bg="white", fg="navy", font=("arial bold",15), command=lambda: [view_report.destroy(), show_menu()])
    return_button.place(x=650, y=600, width=140, height=30)


show_menu()
root.mainloop()