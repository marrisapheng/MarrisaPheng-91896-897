import tkinter as tk
from tkinter import messagebox

#Main window
root = tk.Tk()
root.title("Student Gradebook Manager")
root.geometry("1080x1080")
root.configure(bg="black")

#Menu window
def show_menu():
    menu_window = tk.Toplevel(root)
    menu_window.title("Menu")
    menu_window.geometry("1080x1080")
    menu_window.configure(bg="black")

#Submit summary report
def submit_summary_report():
    submit_report = tk.Toplevel(root)
    submit_report.title("Submit Summary Report")
    submit_report.geometry("1080x1080")
    submit_report.configure(bg="black")

    #List for grades
    grades = []

    #Name and subjects question
    tk.Label(submit_report, text="Enter Your Name:", bg="black").pack(pady=10)
    name_entry = tk.Entry(submit_report)
    name_entry.pack(pady=10)

    subjects_label = tk.Label(submit_report, text="Total Number of Subjects:", bg="black")
    subjects_label.pack(pady=10)
    subjects_entry = tk.Entry(submit_report)
    subjects_entry.pack(pady=10)

    def grade_entries():
        #Delete previous entries
        for widget in grades:
            widget.destroy()
        grades.clear()

        #Get number of subjects
        try:
            num_subjects = int(subjects_entry.get())
            if num_subjects <= 0 or num_subjects >=6:
                messagebox.showerror("Invalid Input", "Number of subjects is invalid, please try again.")
                subjects_entry.delete(0, tk.END)
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of subjects.")
            subjects_entry.delete(0, tk.END)
            return
        
        #Enter grade prompt
        for i in range(num_subjects):
            grade_label = tk.Label(submit_report, text=f"Enter Grade for Subject {i+1}:", bg="black")
            grade_label.pack(pady=10)
            grade_entry = tk.Entry(submit_report)
            grade_entry.pack(pady=10)
            grades.append(grade_entry)

        #Submit grades
        def submit_grades():
            try:
                grades_list = [int(grade.get()) for grade in grades]
                if any(grade < 0 or grade > 100 for grade in grades_list):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid grades between 0 and 100.")
                return
            
            #Calculate average grade
            average = sum(grades_list) / len(grades_list)
            average_label = tk.Label(submit_report,text= f"Average Grade: {average:.2f}")
            average_label.pack(pady=10)

            #Show summary report
            def show_summary_report():
                student_name = name_entry.get()
                summary_text = f"Student Name: {student_name}, Average Grade: {average}\n"
                summary_label = tk.Label(submit_report, text=summary_text, bg="black")
                summary_label.pack(pady=10)
            
            #Show summary report button
            summary_button = tk.Button(submit_report, text="Show Summary Report", command=show_summary_report)
            summary_button.pack(pady=10)

        #Submit button
        submit_button = tk.Button(submit_report, text="Submit Grades", command=submit_grades)
        submit_button.pack(pady=10)

    #Button from entering subjects to entering grades
    next_button = tk.Button(submit_report, text="Next", command=grade_entries)
    next_button.pack(pady=10)

#View summary report
def view_summary_report():
    view_report = tk.Toplevel(root)
    view_report.title("View Summary Report")
    view_report.geometry("1080x1080")
    view_report.configure(bg="black")

#View summary report button
view_summary_report_button = tk.Button(root, text="View Summary Report", command=view_summary_report)
view_summary_report_button.pack(pady=20)
#Submit summary report button
submit_summary_report_button = tk.Button(root, text="Submit Summary Report", command=submit_summary_report)
submit_summary_report_button.pack(pady=20)
#Close button
close_button = tk.Button(root, text="Close", command=root.destroy)
close_button.pack(pady=20)

root.mainloop()

#this is my initial commit