import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser

def select_problem(df):
    if df['Attempt Number'].max() > 0:  # Ensure there are attempted problems
        weights = 1 / (1 + df['Attempt Number'])
    else:
        weights = None
    return df.sample(weights=weights)


def filter_categories(c, v):
    global filtered
    if v.get() == 1:
        # Add all problems of category c if not already present
        if c not in filtered['Category'].unique():
            filtered = pd.concat([filtered, df[df['Category'] == c]], ignore_index=True)   
    if v.get() == 0:
        # Remove all problems of category c
        filtered = filtered[filtered['Category'] != c]
        
def update_progress(df, problem_id, time_spent, file_path):
    df.loc[problem_id, 'Attempt Number'] += 1
    df.loc[problem_id, 'Time Spent'] += time_spent
    df.to_csv(file_path, index=False)
    messagebox.showinfo("Update Successful", "Your progress has been saved!")

def show_problem():
    global selected_problem
    selected_problem = select_problem(filtered)
    problem_name.set(f"Problem: {selected_problem['Name'].values[0]}")
    problem_link.set(f"Link: {selected_problem['Link'].values[0]}")
    just_link.set(f"{selected_problem['Link'].values[0]}")

def submit_time():
    try:
        time_spent = int(time_spent_var.get())
        update_progress(df, selected_problem.index[0], time_spent, file_path)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for time spent.")

def open_link():
    webbrowser.open(just_link.get())

# Load data
file_path = 'neetcode150.csv'
df = pd.read_csv(file_path)
filtered = df.copy()

# Setup GUI
root = tk.Tk()
root.title("NeetCode Problem Selector")

problem_name = tk.StringVar()
problem_link = tk.StringVar()
time_spent_var = tk.StringVar()
just_link = tk.StringVar()
categories = {category: tk.IntVar(value=1) for category in df['Category'].unique()}

for category, var in categories.items():
    tk.Checkbutton(root, text=category, variable=var, onvalue=1, offvalue=0, command=lambda c=category, v=var: filter_categories(c, v)).pack()

tk.Button(root, text="Show Random Problem", command=show_problem).pack(pady=(20, 0))
tk.Label(root, textvariable=problem_name).pack(pady=(5, 5))
link_label = tk.Label(root, textvariable=problem_link, fg="yellow", cursor="tcross")
link_label.pack(pady=(5, 20))
link_label.bind("<Button-1>", lambda e: open_link())
tk.Entry(root, textvariable=time_spent_var).pack(pady=(5, 5))
tk.Button(root, text="Submit Time", command=submit_time).pack(pady=(0, 20))

root.mainloop()
