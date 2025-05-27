import tkinter as tk
from tkinter import messagebox

#Main window
root = tk.Tk()
root.title("Student Gradebook Manager")
root.geometry("1920x1080")
root.configure(bg="black")
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
    menu_window.configure(bg="black")
    menu_window.grab_set()

    #Menu buttons
    #View summary report button
    view_summary_report_button= tk.Button(menu_window, text= "View Summary Report", command=lambda: [menu_window.destroy(), view_summary_report()])
    view_summary_report_button.pack(pady=20)
    view_summary_report_button.place(x=530, y=300, width=200, height=50)
    #Submit summary report button
    submit_summary_report_button= tk.Button(menu_window, text= "Submit Summary Report", command=lambda: [menu_window.destroy(), submit_summary_report()])
    submit_summary_report_button.pack(pady=20)
    submit_summary_report_button.place(x=730, y=300, width=200, height=50)
    #Close button
    close_button= tk.Button(menu_window, text= "Close", command=lambda: [menu_window.destroy(), root.destroy()])
    close_button.pack(pady=20)
    close_button.place(x=655, y=350, width=150, height=40)

#Submit summary report
def submit_summary_report():
    submit_report= tk.Toplevel(root)
    submit_report.title("Submit Summary Report")
    submit_report.geometry("1920x1080")
    submit_report.configure(bg="black")
    submit_report.grab_set()

    #List for grades
    grades= []
    grade_widgets= []
    result_labels= []

    #Name and subjects question
    tk.Label(submit_report, text= "Enter Your Name:", bg="black").pack(pady=10)
    name_entry = tk.Entry(submit_report)
    name_entry.pack(pady=10)

    subjects_label = tk.Label(submit_report, text="Total Number of Subjects:", bg="black")
    subjects_label.pack(pady=10)
    subjects_entry = tk.Entry(submit_report)
    subjects_entry.pack(pady=10)

    def grade_entries():
        #Delete previous entries
        for widget in grade_widgets:
            widget.destroy()
        grade_widgets.clear()
        grades.clear()

        #Get number of subjects
        try:
            num_subjects= int(subjects_entry.get())
            if num_subjects <= 0 or num_subjects >=6:
                messagebox.showerror("Invalid Input", "Invalid, please enter a numeric value.")
                subjects_entry.delete(0, tk.END)
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of subjects.")
            subjects_entry.delete(0, tk.END)
            return
        
        #Enter grade prompt
        for i in range(num_subjects):
            grade_label= tk.Label(submit_report, text= f"Enter Grade for Subject {i+1}:", bg="black")
            grade_label.pack(pady=10)
            grade_entry= tk.Entry(submit_report)
            grade_entry.pack(pady=10)
            grades.append(grade_entry)
            grade_widgets.append(grade_label)
            grade_widgets.append(grade_entry)

        #Submit grades
        def submit_grades():
            for label in result_labels:
                label.destroy()
            result_labels.clear()
            try:
                grades_list= [int(grade.get()) for grade in grades]
                if any(grade < 0 or grade > 100 for grade in grades_list):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid grades between 0 and 100.")
                return
            
            #Calculate average grade
            average= sum(grades_list) / len(grades_list)
            average_label= tk.Label(submit_report,text= f"Average Grade: {average:.2f}")
            average_label.pack(pady=10)

            student_name= name_entry.get()
            summary_text= f"Student Name: {student_name}, Average Grade: {average}\n"
            summary_label= tk.Label(submit_report, text= summary_text, bg="black")
            summary_label.pack(pady=10)

            #Save summary report to txt file
            def save_student_summary():
                student_name= name_entry.get()
                if student_name== "":
                    messagebox.showerror("Invalid, Please enter a valid name.")
                    return
                with open("student_records.txt", "a") as file:
                    file.write(f"Student Name: {student_name}, Average Grade: {average:.2f}\n")
                save_summary= tk.Label(submit_report, text= "Student summary report saved successfully!", bg="black")
                save_summary.pack(pady=10)
            #Save summary button
            tk.Button(submit_report, text= "Save Summary Report", command=save_student_summary).pack(pady=10)
            #Return to menu
            tk.Button(submit_report, text= "Return to Menu", command=lambda: [submit_report.destroy(), show_menu()]).pack(pady=10)
        #Submit button
        submit_button= tk.Button(submit_report, text= "Submit Grades", command=submit_grades)
        submit_button.pack(pady=10)
        grade_widgets.append(submit_button)

    #Button from entering subjects to entering grades
    next_button= tk.Button(submit_report, text= "Next", command=grade_entries)
    next_button.pack(pady=10)

    #Return to menu button
    return_button= tk.Button(submit_report, text= "Return to Menu", command=lambda: [submit_report.destroy(),show_menu()])
    return_button.pack(pady=10)

#View summary report
def view_summary_report():
    view_report= tk.Toplevel(root)
    view_report.title("View Summary Report")
    view_report.geometry("1920x1080")
    view_report.configure(bg="black")
    view_report.grab_set()

    #Enter student name prompt
    name_prompt_label= tk.Label(view_report, text="Enter Student Name:", bg="black")
    name_prompt_label.pack(pady=10)

    #Search entry
    search_name_entry= tk.Entry(view_report)
    search_name_entry.pack(pady=10)

    result_label= tk.Label(view_report, text= "", bg="black")
    result_label.pack(pady=10)
# HERE - WHEN SEARCHING FOR STUDENT NAME, IT DOES NOT SHOW THE STUDENT NAME, INSTEAD "ALERT" IS SHOWN
    def search_student():
        student_name= search_name_entry.get().strip()
        if student_name== "":
            messagebox.showerror("Invalid Input", "Please enter a valid name.")
            return

        try:
            with open("student_records.txt", "r") as file:
                student_found = [line for line in file if student_name.lower() in line.lower()]
                if student_found:
                    result_text = "\n".join(student_found)
                    result_label.config(text=result_text)
                    return
        except FileNotFoundError:
            result_label.config(text = "Student not found")
            return
        #If student was not found
        messagebox.showerror("Student not found, please try again.")
        search_name_entry.delete(0, tk.END)
        result_label.config(text="")
                
    #Search button
    search_button = tk.Button(view_report, text="Search", command=search_student)
    search_button.pack(pady=10)

    #Return to menu button
    return_button = tk.Button(view_report, text="Return to Menu", command=lambda: [view_report.destroy(), show_menu()])
    return_button.pack(pady=10)


show_menu()
root.mainloop()