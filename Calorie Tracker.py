import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime
import os

class CalorieTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("💎 Premium Calorie Tracker 💎")
        master.geometry("500x400")
        master.configure(bg="#F5F5F5")

        self.load_data()

        self.label = tk.Label(master, text="Calorie Tracker", font=("Arial", 24, "bold"), bg="#F5F5F5", fg="#333333")
        self.label.pack(pady=20)

        self.add_button = tk.Button(master, text="Add Calories", command=self.add_calories, font=("Arial", 14), bg="#4CAF50", fg="#FFFFFF", padx=10)
        self.add_button.pack(pady=10)

        self.view_button = tk.Button(master, text="View Calories", command=self.view_calories, font=("Arial", 14), bg="#3498DB", fg="#FFFFFF", padx=10)
        self.view_button.pack(pady=10)

        self.edit_button = tk.Button(master, text="Edit Entry", command=self.edit_entry, font=("Arial", 14), bg="#E67E22", fg="#FFFFFF", padx=10)
        self.edit_button.pack(pady=10)

        self.delete_button = tk.Button(master, text="Delete Entry", command=self.delete_entry, font=("Arial", 14), bg="#E74C3C", fg="#FFFFFF", padx=10)
        self.delete_button.pack(pady=10)

        self.exit_button = tk.Button(master, text="Exit", command=self.master.destroy, font=("Arial", 14), bg="#E74C3C", fg="#FFFFFF", padx=10)
        self.exit_button.pack(pady=10)

    def load_data(self):
        if not hasattr(self, 'data'):
            self.data = {}
            if os.path.exists('calories.json'):
                with open('calories.json', 'r') as file:
                    self.data = json.load(file)

    def save_data(self):
        with open('calories.json', 'w') as file:
            json.dump(self.data, file, indent=2)

    def add_calories(self):
        date = datetime.now().strftime("%Y-%m-%d")
        food = simpledialog.askstring("Add Calories", "Enter the food name:")
        calories = simpledialog.askinteger("Add Calories", "Enter the calories:")

        if food and calories is not None:
            if date not in self.data:
                self.data[date] = []

            self.data[date].append({"food": food, "calories": calories})
            self.save_data()
            message = f"Added {calories} calories from {food} on {date}."
            messagebox.showinfo("Calorie Tracker", message)

    def view_calories(self):
        if not self.data:
            messagebox.showinfo("Calorie Tracker", "No data available.")
        else:
            message = "Date\t\tFood\t\tCalories\n------------------------\n"
            for date, entries in self.data.items():
                for entry in entries:
                    message += f"{date}\t{entry['food']}\t{entry['calories']}\n"
            messagebox.showinfo("Calorie Tracker", message)

    def edit_entry(self):
        if not self.data:
            messagebox.showinfo("Calorie Tracker", "No data available to edit.")
            return

        date_to_edit = simpledialog.askstring("Edit Entry", "Enter the date to edit (YYYY-MM-DD):")

        if date_to_edit and date_to_edit in self.data:
            entries = self.data[date_to_edit]
            entry_to_edit = simpledialog.askinteger("Edit Entry", "Enter the number of the entry to edit:\n\n" +
                                                               "\n".join([f"{i+1}. {entry['food']} - {entry['calories']} calories" for i, entry in enumerate(entries)]))

            if entry_to_edit is not None and 0 < entry_to_edit <= len(entries):
                selected_entry = entries[entry_to_edit - 1]
                new_food = simpledialog.askstring("Edit Entry", f"Edit food (current: {selected_entry['food']}):", initialvalue=selected_entry['food'])
                new_calories = simpledialog.askinteger("Edit Entry", f"Edit calories (current: {selected_entry['calories']}):", initialvalue=selected_entry['calories'])

                if new_food is not None and new_calories is not None:
                    selected_entry['food'] = new_food
                    selected_entry['calories'] = new_calories
                    self.save_data()
                    message = f"Edited entry to {new_food} - {new_calories} calories on {date_to_edit}."
                    messagebox.showinfo("Calorie Tracker", message)
            elif entry_to_edit is not None:
                messagebox.showinfo("Calorie Tracker", "Invalid entry number. No entries were edited.")
        elif date_to_edit:
            messagebox.showinfo("Calorie Tracker", f"No entries found for the date {date_to_edit}.")

    def delete_entry(self):
        if not self.data:
            messagebox.showinfo("Calorie Tracker", "No data available to delete.")
            return

        date_to_delete = simpledialog.askstring("Delete Entry", "Enter the date to delete (YYYY-MM-DD):")

        if date_to_delete and date_to_delete in self.data:
            entries = self.data[date_to_delete]
            entry_to_delete = simpledialog.askinteger("Delete Entry", "Enter the number of the entry to delete:\n\n" +
                                                               "\n".join([f"{i+1}. {entry['food']} - {entry['calories']} calories" for i, entry in enumerate(entries)]))

            if entry_to_delete is not None and 0 < entry_to_delete <= len(entries):
                deleted_entry = entries.pop(entry_to_delete - 1)
                self.save_data()
                message = f"Deleted entry: {deleted_entry['food']} - {deleted_entry['calories']} calories on {date_to_delete}."
                messagebox.showinfo("Calorie Tracker", message)
            elif entry_to_delete is not None:
                messagebox.showinfo("Calorie Tracker", "Invalid entry number. No entries were deleted.")
        elif date_to_delete:
            messagebox.showinfo("Calorie Tracker", f"No entries found for the date {date_to_delete}.")

def main():
    root = tk.Tk()
    app = CalorieTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
