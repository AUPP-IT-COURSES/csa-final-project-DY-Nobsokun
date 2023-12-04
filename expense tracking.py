import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import csv

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    if date and category and amount:
        with open("expenses.txt", "a") as file:
            file.write(f"{date},{category},{amount}\n")
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        view_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")

def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text
        with open("expenses.txt", "r") as file:
            lines = file.readlines()
        with open("expenses.txt", "w") as file:
            for line in lines:
                if line.strip() != f"{date},{category},{amount}":
                    file.write(line)
        status_label.config(text="Expense deleted successfully!", fg="green")
        view_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

def view_expenses():
    global expenses_tree
    if os.path.exists("expenses.txt"):
        total_expense = 0
        expenses_tree.delete(*expenses_tree.get_children())
        with open("expenses.txt", "r") as file:
            for line in file:
                date, category, amount = line.strip().split(",")
                expenses_tree.insert("", tk.END, values=(date, category, amount))
                total_expense += float(amount)
        total_label.config(text=f"Total Expense: {total_expense:.2f}")
    else:
        total_label.config(text="No expenses recorded.")
        expenses_tree.delete(*expenses_tree.get_children())

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entries for adding expenses
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the status of expense addition and deletion
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create buttons to view and delete expenses
view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=7, column=0, padx=5, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=7, column=1, padx=5, pady=10)

# Check if the 'expenses.txt' file exists; create it if it doesn't
if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass

def visualize_expenses():
    categories = {}
    if os.path.exists("expenses.txt"):
        with open("expenses.txt", "r") as file:
            for line in file:
                _, category, amount = line.strip().split(",")
                if category in categories:
                    categories[category] += float(amount)
                else:
                    categories[category] = float(amount)

        if categories:
            plt.figure(figsize=(8, 8))
            plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', startangle=140)
            plt.title('Expense Distribution by Category')
            plt.show()
        else:
            status_label.config(text="No expenses to visualize!", fg="red")
    else:
        status_label.config(text="No expenses recorded.", fg="red")


# Create a button to visualize expenses
visualize_button = tk.Button(root, text="Visualize Expenses", command=visualize_expenses)
visualize_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)

def select_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text
        date_entry.delete(0, tk.END)
        date_entry.insert(0, date)
        category_entry.delete(0, tk.END)
        category_entry.insert(0, category)
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, amount)
        status_label.config(text="Expense selected for editing.", fg="blue")
    else:
        status_label.config(text="Please select an expense to edit.", fg="red")

def update_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        old_date, old_category, old_amount = item_text
        new_date = date_entry.get()
        new_category = category_entry.get()
        new_amount = amount_entry.get()

        if new_date and new_category and new_amount:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()

            with open("expenses.txt", "w") as file:
                for line in lines:
                    if line.strip() == f"{old_date},{old_category},{old_amount}":
                        file.write(f"{new_date},{new_category},{new_amount}\n")
                    else:
                        file.write(line)

            status_label.config(text="Expense updated successfully!", fg="green")
            view_expenses()
        else:
            status_label.config(text="Please fill all the fields!", fg="red")
    else:
        status_label.config(text="Please select an expense to update!", fg="red")


# Create buttons for selecting and updating expenses
select_button = tk.Button(root, text="Select Expense", command=select_expense)
select_button.grid(row=14, column=0, padx=5, pady=10)

update_button = tk.Button(root, text="Update Expense", command=update_expense)
update_button.grid(row=14, column=1, padx=5, pady=10)

def export_to_csv():
    if os.path.exists("expenses.txt"):
        with open("expenses.txt", "r") as file:
            expenses_data = [line.strip().split(",") for line in file]

        csv_file_path = "expenses.csv"

        with open(csv_file_path, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Date", "Category", "Amount"])
            csv_writer.writerows(expenses_data)

        status_label.config(text=f"Expense data exported to {csv_file_path}.", fg="green")
    else:
        status_label.config(text="No expenses recorded.", fg="red")


# Create a button to export expenses to CSV
export_csv_button = tk.Button(root, text="Export to CSV", command=export_to_csv)
export_csv_button.grid(row=16, column=0, columnspan=2, padx=5, pady=10)


# Display existing expenses on application start
view_expenses()

root.mainloop()
