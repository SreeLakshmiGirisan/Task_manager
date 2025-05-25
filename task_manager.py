import os
import json
from datetime import datetime

# File to store tasks
DATA_FILE = 'tasks.json'

# -------- TASK CLASS --------
class Task:
    def __init__(self, title, due_date=None, completed=False):
        self.title = title
        self.due_date = due_date  # Expected format: YYYY-MM-DD
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        # Convert the Task object to a dictionary so we can save it in a file
        return {
            'title': self.title,
            'due_date': self.due_date,
            'completed': self.completed
        }

# Convert saved dictionary back to a Task object
def task_from_dict(data):
    return Task(data['title'], data['due_date'], data['completed'])

# -------- TASK MANAGER CLASS --------
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load()  # Load existing tasks from file if any

    def add_task(self):
        title = input("\nEnter task title: ").strip()

        while True:
            due_date_input = input("Enter due date (YYYY-MM-DD): ").strip()

            try:
                due_date_obj = datetime.strptime(due_date_input, "%Y-%m-%d").date()
                today = datetime.today().date()

                if due_date_obj < today:
                    print(" Due date cannot be in the past.")
                else:
                    break
            except ValueError:
                print(" Invalid date format. Use YYYY-MM-DD.")

        # Add the task to the list
        self.tasks.append(Task(title, due_date_input))
        print(f" Task '{title}' added.")
        self.save()

    def complete_task(self):
        self.view_pending_tasks()
        try:
            index = int(input("Enter the number of the completed task: ")) - 1

            if 0 <= index < len(self.tasks) and not self.tasks[index].completed:
                self.tasks[index].mark_completed()
                print(f" Task '{self.tasks[index].title}' marked as completed.")
                self.save()
            else:
                print(" Invalid choice or task already completed.")
        except ValueError:
            print(" Enter a valid number.")

    def view_pending_tasks(self):
        print("\n Pending Tasks:")
        has_pending = False

        for i, task in enumerate(self.tasks):
            if not task.completed:
                has_pending = True
                print(f"{i+1}. {task.title} (Due: {task.due_date})")

        if not has_pending:
            print(" No pending tasks!")

    def view_completed_tasks(self):
        print("\n Completed Tasks:")
        has_completed = False

        for task in self.tasks:
            if task.completed:
                has_completed = True
                print(f"- {task.title}")

        if not has_completed:
            print("No completed tasks yet.")

    def view_all_tasks(self):
        print("\n All Tasks:")
        for i, task in enumerate(self.tasks):
            status = "Done" if task.completed else "Pending"
            print(f"{i+1}. {task.title} (Due: {task.due_date}) - {status}")

    def save(self):
        data = [task.to_dict() for task in self.tasks]
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                self.tasks = [task_from_dict(task_data) for task_data in data]

# -------- MAIN PROGRAM --------
def main():
    manager = TaskManager()
    print(" Welcome to Simple Task Manager!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Add a new task")
        print("2. Complete a task")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. View all tasks")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            manager.add_task()
        elif choice == "2":
            manager.complete_task()
        elif choice == "3":
            manager.view_pending_tasks()
        elif choice == "4":
            manager.view_completed_tasks()
        elif choice == "5":
            manager.view_all_tasks()
        elif choice == "6":
            print(" Thanks for using Task Manager!")
            break
        else:
            print(" Invalid choice. Please enter a number between 1-6.")


# Run the main function
if __name__ == "__main__":
    main()
