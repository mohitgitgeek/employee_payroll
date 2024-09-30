# Predefined employee records dictionary
employee_records = {
    "E001": {
        "name": "Alice Johnson",
        "position": "Software Engineer",
        "salary": "70000"
    },
    "E002": {
        "name": "Bob Smith",
        "position": "Project Manager",
        "salary": "90000"
    },
    "E003": {
        "name": "Charlie Brown",
        "position": "Data Analyst",
        "salary": "60000"
    }
}

def add_employee():
    emp_id = input("Enter Employee ID: ")
    if emp_id in employee_records:
        print("Employee ID already exists.")
        return
    name = input("Enter Employee Name: ")
    position = input("Enter Employee Position: ")
    salary = input("Enter Employee Salary: ")
    employee_records[emp_id] = {
        "name": name,
        "position": position,
        "salary": salary
    }
    print("Employee added successfully.")

def view_employee():
    emp_id = input("Enter Employee ID to view: ")
    if emp_id in employee_records:
        print(f"ID: {emp_id}")
        print(f"Name: {employee_records[emp_id]['name']}")
        print(f"Position: {employee_records[emp_id]['position']}")
        print(f"Salary: {employee_records[emp_id]['salary']}")
    else:
        print("Employee not found.")

def update_employee():
    emp_id = input("Enter Employee ID to update: ")
    if emp_id in employee_records:
        name = input("Enter new Employee Name: ")
        position = input("Enter new Employee Position: ")
        salary = input("Enter new Employee Salary: ")
        employee_records[emp_id] = {
            "name": name,
            "position": position,
            "salary": salary
        }
        print("Employee updated successfully.")
    else:
        print("Employee not found.")

def delete_employee():
    emp_id = input("Enter Employee ID to delete: ")
    if emp_id in employee_records:
        del employee_records[emp_id]
        print("Employee deleted successfully.")
    else:
        print("Employee not found.")

def main_menu():
    while True:
        print("\nEmployee Payroll System")
        print("1. Add Employee")
        print("2. View Employee")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employee()
        elif choice == "3":
            update_employee()
        elif choice == "4":
            delete_employee()
        elif choice == "5":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

# Start the payroll system
main_menu()