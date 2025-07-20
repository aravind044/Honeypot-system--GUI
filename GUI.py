import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from collections import Counter
import datetime
import re


LOG_FILE = "honeypot_log.txt"

def read_log():
    """Reads the honeypot log file and extracts attack data."""
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        
        attacks = []
        for line in lines:
            match = re.search(r"\[(.*?)\] IP: (.*?) \| Data: (.*)", line)
            if match:
                timestamp, ip, data = match.groups()
                attacks.append((timestamp, ip, data))
        return attacks
    except FileNotFoundError:
        messagebox.showerror("Error", "Log file not found!")
        return []

def display_data():
    """Displays the log data in the GUI table."""
    for row in table.get_children():
        table.delete(row)
    
    attacks = read_log()
    for attack in attacks:
        table.insert("", "end", values=attack)

def show_chart():
    """Generates a pie chart of attack frequency by IP address."""
    attacks = read_log()
    ip_counts = Counter(ip for _, ip, _ in attacks)

    if not ip_counts:
        messagebox.showinfo("Info", "No data available to display.")
        return

    plt.figure(figsize=(6, 6))
    plt.pie(ip_counts.values(), labels=ip_counts.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Attack Frequency by IP Address")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Honeypot Attack Analysis")
root.geometry("600x400")

# Table
columns = ("Timestamp", "IP Address", "Login Attempt")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)
table.pack(pady=10, expand=True, fill="both")

# Load initial data
display_data()

# Run GUI
root.mainloop()