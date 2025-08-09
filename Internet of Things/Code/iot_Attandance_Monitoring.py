import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from supabase import create_client, Client
root = tk.Tk()
root.title("Swipe In Device")
root.geometry("625x500")

url = "https://rhdfsunxhfebzzwkicfd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJoZGZzdW54aGZlYnp6d2tpY2ZkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NDY3MzE0MSwiZXhwIjoyMDcwMjQ5MTQxfQ.eEwEtr-u8DGAp1HaFUqkA3LMm7jpyrxi6gN-e002pFk"
supabase: Client = create_client(url, key)
columns = ("Name", "ID", "In Time", "Out Time", "Location", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)
def submit_data():
    name = name_entry.get()
    id = int(id_entry.get())
    in_time = in_time_entry.get()
    out_time = out_time_entry.get()
    location = location_entry.get()
    date = date_entry.get()
    data = {
        "Emp_ID": id, "Name": name, "Location": location, "Date": date, "InTime": in_time,
        "OutTime": out_time
    }
    response = supabase.table("EmployeeLogginSystem").insert(data).execute()

    if response :
        messagebox.showinfo("Success", "Data stored in cloud")
    else:
        messagebox.showerror("Error", f"Failed to store data: {response}")

def read_data():
    for row in tree.get_children():
        tree.delete(row)

    response = supabase.table("EmployeeLogginSystem").select("*").execute()

    for row in response.data:
        tree.insert("", tk.END, values=(
            row["Name"], row["Emp_ID"], row["InTime"],
            row["OutTime"], row["Location"], row["Date"]
        ))

# Labels and Entry widgets
fields = [
    ("Name", "name_entry"),
    ("ID", "id_entry"),
    ("In Time (HH:MM)", "in_time_entry"),
    ("Out Time (HH:MM)", "out_time_entry"),
    ("Location", "location_entry"),
    ("Date (DD/MM/YYYY)", "date_entry")
]

entries = {}

for i, (label_text, var_name) in enumerate(fields):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=0, pady=5, sticky="w")
    entry = tk.Entry(root, width=20)
    entry.grid(row=i, column=1, padx=0, pady=5)
    entries[var_name] = entry

# Assign entries to variables
name_entry = entries["name_entry"]
id_entry = entries["id_entry"]
in_time_entry = entries["in_time_entry"]
out_time_entry = entries["out_time_entry"]
location_entry = entries["location_entry"]
date_entry = entries["date_entry"]

# Submit button
submit_btn = tk.Button(root, text="Submit", command=submit_data)
submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=20)
read_btn = tk.Button(root, text="Read Data", command=read_data)
read_btn.grid(row=len(fields)+1, column=0, columnspan=2, pady=5)

# Treeview for displaying data
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=len(fields)+2, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
