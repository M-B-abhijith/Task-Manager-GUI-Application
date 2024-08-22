import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

class Task:
    def __init__(self, description, parent=None):
        self.description = description
        self.created_at = datetime.datetime.now()
        self.subtasks = []
        self.parent = parent

    def add_subtask(self, description):
        new_subtask = Subtask(description, parent=self)
        self.subtasks.append(new_subtask)
        return new_subtask

    def remove_subtask(self, subtask):
        if subtask in self.subtasks:
            self.subtasks.remove(subtask)

    def __str__(self):
        indent = "    " * self.get_level()
        return f"{indent}{self.description} (Added on {self.created_at.strftime('%Y-%m-%d %H:%M')})"

    def get_level(self):
        level = 0
        current = self.parent
        while current:
            level += 1
            current = current.parent
        return level

class Subtask(Task):
    def __init__(self, description, parent=None):
        super().__init__(description, parent=parent)

    def __str__(self):
        indent = "    " * self.get_level()
        return f"{indent}[Subtask] {self.description} (Added on {self.created_at.strftime('%Y-%m-%d %H:%M')})"

class TaskManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")
        self.master.configure(bg="#30323f")

        self.tasks = []

        self.task_entry = tk.Entry(master, width=40)
        self.task_entry.grid(row=0, column=0, padx=5, pady=5)

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task, bg="#9f68f3", fg="white", bd=2, relief="flat")
        self.add_button.grid(row=0, column=1, padx=5, pady=5)

        self.add_subtask_button = tk.Button(master, text="Add Subtask", command=self.add_subtask, bg="#7fa8f3", fg="white", bd=2, relief="flat")
        self.add_subtask_button.grid(row=0, column=2, padx=5, pady=5)

        self.task_listbox = tk.Listbox(master, width=75, height=15)
        self.task_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.delete_button = tk.Button(master, text="Delete Task/Subtask", command=self.delete_task, bg="#e48064", fg="white", relief="flat")
        self.delete_button.grid(row=2, column=0, padx=5, pady=5)

        self.clear_button = tk.Button(master, text="Clear All", command=self.clear_all, bg="#da1b56", fg="white", relief="flat")
        self.clear_button.grid(row=2, column=1, padx=5, pady=5)

    def add_task(self):
        task_description = self.task_entry.get()
        if task_description:
            new_task = Task(task_description)
            self.tasks.append(new_task)
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)

    def add_subtask(self):
        selected = self.task_listbox.curselection()
        if selected:
            task, _ = self.find_task(selected[0])
            if task:
                description = simpledialog.askstring("Input", "Enter subtask description")
                if description:
                    task.add_subtask(description)
                    self.update_task_listbox()

    def find_task(self, index, tasks=None, start_index=0):
        if tasks is None:
            tasks = self.tasks

        for task in tasks:
            if start_index == index:
                return task, start_index
            start_index += 1
            subtask_result, start_index = self.find_task(index, task.subtasks, start_index)
            if subtask_result:
                return subtask_result, start_index
        return None, start_index

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        self.insert_tasks(self.tasks)

    def insert_tasks(self, tasks, level=0):
        for task in tasks:
            self.task_listbox.insert(tk.END, str(task))
            if task.subtasks:
                self.insert_tasks(task.subtasks, level + 1)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task, _ = self.find_task(selected[0])
            if task:
                if task.parent:
                    task.parent.subtasks.remove(task)
                else:
                    self.tasks.remove(task)
                self.update_task_listbox()

    def clear_all(self):
        response = messagebox.askyesno("Clear All Tasks", "Are you sure you want to clear all tasks?")
        if response:
            self.tasks = []
            self.update_task_listbox()

def main():
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
