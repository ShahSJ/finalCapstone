# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
# Reads tasks.txt file and splits the data inside
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# A List is created to be used by the tasks
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t) # Adds each task to the list


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False # logged_in is false, force user sign in
while not logged_in:
    
    print("\n---------")
    print("| LOGIN |")
    print("---------\n")
    # User is asked to enter a username and password
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():       # if user doesn't exist, prints a error statement
        print("\nUser does not exist!")
        continue
    elif username_password[curr_user] != curr_pass:     # if password is incorrect, prints a error statement
        print("\nWrong password!")
        continue
    else:
        print("\n---------------------")
        print("| Login Successful! |")
        print("---------------------\n")
        logged_in = True

# Function to Register a new User
def reg_user():
    while True:
            new_username = input("New Username: ")
            # Checks if the username inputed already exists 
            if new_username not in username_password.keys():    
                print("\nUsername ", new_username, " Added!")
                break
            else:
                print("\nUsername Already Exists!\n")
                continue
    new_password = input("\nNew Password: ")
    confirm_password = input("Confirm Password: ")
    # Check if the new password and confirmed password are the same 
    if new_password == confirm_password:
        print("\n----------------")
        print("| New user added! |")
        print("----------------\n")
        #  If they are the same, adds user them to the user.txt file.
        username_password[new_username] = new_password
        # User data is added to txt file and a list
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))    
    else:
        # Otherwise you present a relevant error messages.
        print("\nPasswords do no match! Please try again.")

# Function to Add tasks to a selected user
def add_task():
    task_username = input("Name of person assigned to task: ")
    # If the username entered does not exist, prints an error and asks to try again
    if task_username not in username_password.keys():       
        print()
        print("User does not exist. Please enter a valid username")
        print()
        return
    task_title = input("Title of Task: ") # user prompted to input title of the task
    task_description = input("Description of Task: ") # user prompted to input Description of the task
    while True:
        try:
            # user prompted to input the completion Date of the task 
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        # If user inputs date wrong, they get an error message
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
        # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,        # Dictionary used to keep track of the tasks data
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }
    # Adds new tasks to the file
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("\n----------------------")
    print("Task successfully added.")
    print("------------------------\n")

# Function to view all tasks
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''
    for t in task_list:
        print("\n-----------------------------------")
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"-----------------------------------\n"
        print(disp_str)

# Function to view current users Tasks
def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
           '''
    user_tasks = {}
    for task_number, t in enumerate(task_list):
        if t['username'] == curr_user:
            user_tasks[str(task_number)] = t 
            print("\n-----------------------------------")
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Task number: \t {task_number}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"-----------------------------------\n"
            print(disp_str)
            
    # Asks the user to enter a specific task number, or -1 to exit to main menu
    task_choice = input("Enter the number of the task you want to view or -1 to return to main menu: ").lower()
    if task_choice == "-1":
            return
    # If the entered number is a task number, gives option to the user to modify the tasks
    elif task_choice in user_tasks.keys():
        task_modify = input("\nPlease enter: \tmc - to mark complete\n(in lowercase)\te - to edit task : ").lower()
        # mc options marks the task as completed
        if task_modify == "mc":
            task_list[int(task_choice)]['completed'] = True 
        elif task_modify == "e":
            if task_list[int(task_choice)]['completed']:
                return print("\n This Task is complete!\n")
            else:
                change_option = input("\nPlease enter: \tu - to change assigned user\n(in lowercase)\tdd - to change due date : ").lower()
                if change_option == "u":
                    while True:
                        action = input("Enter a new user to reassign to: ")
                        if action in username_password.keys():
                            task_list[int(task_modify)]["username"] = action
                            break
                        else:
                            print("\nUsername does not exist! Please enter another username :")
                if change_option == "dd":
                    while True:
                        try:
                            new_due_date = input("\nNew due date of task (YYYY-MM-DD): ")
                            new_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            break
                        # A error given if date is inputted in an incorrect format
                        except ValueError:
                            print("\nInvalid datetime format! Please use the format YYYY-MM-DD")
                    task_list[int(task_choice)]["due_date"] = new_date_time
                # If user inputs date wrong, they get an error message
                else:
                    return print("\nInvalid Option! Please try again.")
        else:
            return print("\nInvalid Option! Please try again.")
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("\n------------------------------------")
        print("| Task has been updated successfully! |")
        print("------------------------------------\n")
    else:
        print("\nInvalid Task Number entered! Please try again and enter a valid Task Number! ")

# Function to generate reports     
def generate_reports():
    # This will allow the admin user to generate the following two reports:
    # A) Task_overview.txt B) user_overview.txt
    if curr_user == 'admin':
        task_tracker = len(task_list)
        incompleted_tasks = []
        completed_tasks = []
        overdue_tasks = []
        for t in task_list:
            if t['completed']:
                completed_tasks.append(t['username'])
            else:
                incompleted_tasks.append(t['username'])
                if t['due_date'] < datetime.today():
                    overdue_tasks.append(t['username'])
        percentage_incomplete = 100.0 * float(len(incompleted_tasks))/ float(task_tracker)
        percentage_overdue = 100.0 * float(len(overdue_tasks))/ float(task_tracker)
        registered_users = len(username_password.keys())
        incompleted = {}
        completed = {}
        overdue = {}
        total = {}
        for user in username_password.keys():
            incompleted[user] = incompleted_tasks.count(user)
            completed[user] = completed_tasks.count(user)
            overdue[user] = overdue_tasks.count(user)
            total[user] = incompleted[user] + completed[user]

        # Outputs the results to task_overview.txt file
        with open("task_overview.txt", "w") as task_overview:
            output_overview_t = f"Total Tasks:\t\t{task_tracker}\n"
            output_overview_t += f"Completed Tasks:\t{len(completed_tasks)}\n"
            output_overview_t += f"Incompleted Tasks:\t{len(incompleted_tasks)}\n"
            output_overview_t += f"Overdue Tasks:\t\t{len(overdue_tasks)}\n"
            output_overview_t += f"Percentage of Tasks incompleted:\t{percentage_incomplete:.2f}%\n"
            output_overview_t += f"Percentage of Tasks overdue:\t{percentage_overdue:.2f}%\n"
            task_overview.write(output_overview_t)

        # - Outputs the results to user_overview.txt
        with open("user_overview.txt", "w") as user_overview:
            output_overview_u = f"Total Users:\t\t{registered_users}\n"
            output_overview_u += f"Total Tasks:\t\t{task_tracker}\n"
            output_overview_u += f"USER\t\tTASKS\t\t%ASSIGNED\t%COMPLETE\t%INCOMPLETE\t%OVERDUE\n"
            for user in username_password.keys():
                output_overview_u += f"{user}:\t\t{total[user]}"
                output_overview_u += f"\t\t{100.0*total[user]/task_tracker:.2f}"
                # If user has no tasks, the if statement prevents error of divison by 0
                if total[user] == 0:
                    output_overview_u += f"\t\tN/A"
                    output_overview_u += f"\t\tN/A"
                    output_overview_u += f"\t\tN/A\n"
                # Outputs percentage of tasks the users have completed, not complete and overdue.
                # The Formatting ensures 2 decimal places
                else:
                    output_overview_u += f"\t\t{100.0*completed[user]/total[user]:.2f}"
                    output_overview_u += f"\t\t{100.0*incompleted[user]/total[user]:.2f}"
                    output_overview_u += f"\t\t{100.0*overdue[user]/total[user]:.2f}\n"
            user_overview.write(output_overview_u)
        print("\n----------------------")
        print("| Reports Generated! |")
        print("----------------------\n")
    else:
        print("\n---------------------------------")
        print("| You Must be admin to do this! |")
        print("---------------------------------\n")

def display_stats():

    '''If the user is an admin they can display statistics about number of users
            and tasks.'''
    num_users = len(username_password.keys())
    num_tasks = len(task_list)
    if curr_user == "admin":
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------") 
        # checks to see if the files already exist, if not runs generate_report() to create them
        if not (os.path.exists("task_overview.txt") and os.path.exists("user_overview.txt")):
            generate_reports()
        # Opens the task_overview.txt file    
        with open("task_overview.txt", "r") as file:
            data_tasks = file.read()
            print("\n Task Overview: \n", data_tasks)
        # Opens the user_overview.txt file
        with open("user_overview.txt", "r") as file:
            data_users = file.read()
            print("\n Task Overview: \n", data_users)
    else:
        print("\n---------------------------------")
        print("| You Must be admin to do this! |")
        print("---------------------------------\n")

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()    
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds': 
        display_stats()   

    elif menu == 'e':
        print("\n--------------")
        print('| Goodbye!!! |')
        print("--------------\n")
        exit()

    else:
        print("You have made a wrong choice, Please Try again")