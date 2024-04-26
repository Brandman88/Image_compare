import os
import pandas as pd
from tkinter import messagebox
import tkinter as tk
from tkinter import messagebox, Tk, ttk, filedialog, Button, Label, Frame
from PIL import Image, ImageTk  # Pillow library for working with images
import re
import random
from datetime import datetime, timedelta

current_dir = os.getcwd()

def setup_exists():
    return os.path.exists("setup.txt")


def run_setup_gui():
    class SetupGUI(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Setup Process")
            self.geometry("300x200")
            self.background_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.configure(background=self.background_color) 
            self.dir_label = tk.Label(self, text="Select Default Directory:")
            self.dir_label.pack(pady=10)
            self.dir_entry = tk.Entry(self, width=40)
            self.dir_entry.pack(pady=5)
            self.browse_button = tk.Button(self, text="Browse", command=self.browse_directory)
            self.browse_button.pack(pady=5)
            self.selected_directory = None
        def browse_directory(self):
            directory = filedialog.askdirectory()
            if directory:
                self.dir_entry.delete(0, tk.END)
                self.dir_entry.insert(0, directory)
                self.selected_directory = directory
                print("Selected directory:", self.selected_directory)
                with open("setup.txt", "w") as f:
                    f.write(self.selected_directory)
                self.destroy()
    setup_gui = SetupGUI()
    setup_gui.mainloop()
    return setup_gui.selected_directory
        
def setup():
    if setup_exists():
        with open("setup.txt", "r") as file:
            default_dir = file.read().strip()
            return default_dir
    else:
        return run_setup_gui()
    
    
    
    
def get_files_in_directory(directory):
    files = []
    if os.path.exists(directory):
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                files.append(file_name)
    else:
        print("Directory does not exist:", directory)
    return files

def get_files_in_directory_from_refrence(directory, reference_date):
    files = []
    if os.path.exists(directory):
        # Convert the reference date string to a datetime object
        reference_time = datetime.strptime(reference_date, "%m-%d-%Y")
        print(reference_time)
        
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                # Get the modification time of the file
                modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                print(modification_time)
                
                # Check if the modification time is after the reference time
                if modification_time > reference_time:
                    files.append(file_name)
    else:
        print("Directory does not exist:", directory)
    return files

def get_directories_in_directory(directory):
    directories = []
    if os.path.exists(directory):
        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            if os.path.isdir(entry_path):
                directories.append(entry)
    else:
        print("Directory does not exist:", directory)
    return directories





def select_directories(default_dir):
    class DirectorySelectionGUI(tk.Tk):
        def __init__(self, default_dir):
            super().__init__()
            self.background_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.configure(background=self.background_color)
            self.title("Directory Selection")
            self.selected_directories = []
            self.tree = ttk.Treeview(self)
            self.tree.heading("#0", text="Select a Directory")
            self.tree.pack(expand=True, fill=tk.BOTH)
            self.confirm_button = tk.Button(self, text="Confirm Selection", command=self.confirm_selection, bg="green")
            self.confirm_button.pack(pady=10)
            self.populate_tree(default_dir)
        def populate_tree(self, directory):
            self.background_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.configure(background=self.background_color) 
            self.tree.delete(*self.tree.get_children())
            directories = get_directories_in_directory(directory)
            for d in directories:
                self.tree.insert("", "end", text=d, open=True)
        def confirm_selection(self):
            selection = self.tree.selection()
            if selection:
                selected_directory = self.tree.item(selection)["text"]
                print("Selected directory:", selected_directory)
                self.selected_directories.append(selected_directory)
                if len(self.selected_directories) == 1:
                    self.populate_tree(os.path.join(default_dir, selected_directory))
                elif len(self.selected_directories) == 2:
                    High_ass=self.selected_directories[0]
                    Low_ass=self.selected_directories[1]
                    High_ass_location=os.path.join(default_dir, High_ass).replace('/', '\\')
                    Low_ass_location=os.path.join(High_ass_location, Low_ass).replace('/', '\\')
                    Accept_location=os.path.join(Low_ass_location, "Accepted").replace('/', '\\')
                    Reject_location=os.path.join(Low_ass_location, "Rejected").replace('/', '\\')
                    self.selected_directories.append(Low_ass_location)
                    self.selected_directories.append(Accept_location)
                    self.selected_directories.append(Reject_location)
                    for item in self.selected_directories:
                        print(item)
                    self.destroy()
    directory_selection_gui = DirectorySelectionGUI(default_dir)
    directory_selection_gui.mainloop()
    return directory_selection_gui.selected_directories



























