import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import schedule
import time
import subprocess
import threading

DATABASE = "schedule.db"

# -----------------------------
# Database Setup & Operations
# -----------------------------
def init_db():
    """Create the schedule table if it does not exist."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # Store just HH:MM (TEXT)
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_schedule(run_time):
    """Add a new scheduled time to the database (run_time = 'HH:MM')."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO schedule (run_time) VALUES (?)", (run_time,))
    conn.commit()
    conn.close()

def get_schedules():
    """Retrieve all schedules as a list of (id, run_time) tuples."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, run_time FROM schedule ORDER BY run_time")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_schedule(schedule_id):
    """Delete a schedule from the database by ID."""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM schedule WHERE id=?", (schedule_id,))
    conn.commit()
    conn.close()

# -----------------------------
# Scheduling Logic
# -----------------------------
def run_script():
    """
    This is the function that schedule will call each day at the specified time.
    Replace the placeholder logic with your actual OBS automation call or script.
    """
    print("Running OBS script...")
    # Example: call a separate Python script
    # Adjust the path/command as needed
    subprocess.run(["python", "obs_connect.py"])

def end_obs_stream():
    """
    This is the function that schedule will call each day at the specified time.
    Replace the placeholder logic with your actual OBS automation call or script.
    """
    print("Ending OBS stream...")
    # Example: call a separate Python script
    # Adjust the path/command as needed
    subprocess.run(["python", "obs_end_stream.py"])

def load_schedules_from_db():
    """
    Clear the current schedule and re-add jobs based on what's in the database.
    """
    schedule.clear()
    rows = get_schedules()
    for row in rows:
        schedule_time = row[1]  # 'HH:MM'
        # Add a daily schedule for each time
        schedule.every().day.at(schedule_time).do(run_script)
        
        hour =schedule_time.split(":")[0]
        minute = schedule_time.split(":")[1]

        end_hour = (int(hour) + 7) % 24
        end_minute = (int(minute) + 50) % 60

        # sheduled_end = f'{int(hour)+7}:{minute}'
        scheduled_end = f'{int(end_hour):02d}:{int(end_minute):02d}'

        print(f"End time: {scheduled_end}")

        # Automatically end the stream after 7 hours 59 minutes
        schedule.every().day.at(scheduled_end).do(end_obs_stream)

def schedule_loop():
    """
    This runs in a background thread so the GUI remains responsive.
    Continuously runs schedule.run_pending() every second.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)

# -----------------------------
# Tkinter GUI
# -----------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OBS Daily Scheduler")
        self.geometry("500x350")

        # Initialize DB and load schedules
        init_db()
        load_schedules_from_db()

        # Start the background scheduler thread (daemon=True stops it with GUI)
        threading.Thread(target=schedule_loop, daemon=True).start()

        self.create_widgets()
        self.populate_schedule_list()

    def create_widgets(self):
        # Label/Entry for "HH:MM"
        self.label = ttk.Label(self, text="Enter daily time (HH:MM) 24-hour format:")
        self.label.pack(pady=10)

        self.run_time_entry = ttk.Entry(self, width=10)
        self.run_time_entry.pack(pady=5)

        # Button to add a new schedule
        self.add_button = ttk.Button(self, text="Add Schedule", command=self.add_schedule_gui)
        self.add_button.pack(pady=5)

        # Listbox to display scheduled times
        self.schedule_list = tk.Listbox(self, width=40, height=8)
        self.schedule_list.pack(pady=10)

        # Button to delete a selected schedule
        self.delete_button = ttk.Button(self, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(pady=5)

    def add_schedule_gui(self):
        """Validate HH:MM, store in DB, refresh the schedule and the list."""
        run_time = self.run_time_entry.get().strip()
        if not self.validate_time_format(run_time):
            messagebox.showerror("Error", "Invalid time format. Use HH:MM (24-hour).")
            return

        # Add to DB
        add_schedule(run_time)
        # Refresh in-memory schedule
        load_schedules_from_db()
        # Update GUI list
        self.populate_schedule_list()

        self.run_time_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Scheduled daily run at {run_time}.")

    def validate_time_format(self, time_str):
        """Check if time_str is in 'HH:MM' 24-hour format."""
        try:
            datetime.datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False

    def populate_schedule_list(self):
        """Refresh the list of schedules displayed in the GUI."""
        self.schedule_list.delete(0, tk.END)
        schedules = get_schedules()
        for sched in schedules:
            sched_id, sched_time = sched
            self.schedule_list.insert(tk.END, f"{sched_id}: {sched_time}")

    def delete_selected(self):
        """Delete the schedule that is currently selected in the listbox."""
        selection = self.schedule_list.curselection()
        if selection:
            index = selection[0]
            schedule_item = self.schedule_list.get(index)
            # Expected format: "id: HH:MM"
            schedule_id = schedule_item.split(":")[0]
            delete_schedule(schedule_id)
            # Refresh schedule in memory
            load_schedules_from_db()
            # Refresh GUI
            self.populate_schedule_list()
        else:
            messagebox.showerror("Error", "No schedule selected.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
