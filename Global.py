import os
import pandas as pd
from tkinter import messagebox
import tkinter as tk
from tkinter import messagebox, Tk, ttk, filedialog, Button, Label, Frame, Canvas
from PIL import Image, ImageTk  # Pillow library for working with images
import re
import random
from datetime import datetime, timedelta
import customtkinter as ctk
import shutil




green = "#00FF00"
red = "#FF0000"
lighter_green = "#66FF66"
darker_green = "#009900"
lighter_red = "#FF6666"
darker_red = "#990000"
white="#FFFFFF"


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

class ImageOutput1(Canvas):
    def __init__(self,parent, resize_image):
        super().__init__(master=parent,background='#FFF')
        self.grid(column=0,row=0,sticky ='nsew')
        self.bind('<Configure>',resize_image)
        
    
class ImageOutput2(Canvas):
    def __init__(self ,parent, resize_image):
        super().__init__(master=parent,background='#FFF')
        self.grid(column=1,row=0,sticky ='nsew')
        self.bind('<Configure>',resize_image)
    
class Output_reject(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent,
            command=lambda: close_func("reject"), 
            text='Reject',
            text_color=lighter_red,
            fg_color = 'transparent',
            width = 40, height =40,
            corner_radius=0,
            hover_color= darker_red)
        self.grid(row=1, column=0, padx=5, pady=5)
    
class Output_accept(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent,
            command=lambda: close_func("accept"),
            text='Accept',
            text_color=lighter_green,
            fg_color = 'transparent',
            width = 40, height =40,
            corner_radius=0,
            hover_color= darker_green)
        self.grid(row=1, column=1, padx=5, pady=5)
        
def move_file(file, destination):
    shutil.move(file, destination)

class Output_Disapprove(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent,
            command=lambda: close_func("Disapprove"), 
            text='Disapprove',
            text_color=lighter_red,
            fg_color = 'transparent',
            width = 40, height =40,
            corner_radius=0,
            hover_color= darker_red)
        self.grid(row=2, column=0, padx=5, pady=5)


class Output_Approve(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent,
            command=lambda: close_func("Approve"),
            text='Approve',
            text_color=lighter_green,
            fg_color = 'transparent',
            width = 40, height =40,
            corner_radius=0,
            hover_color= darker_green)
        self.grid(row=2, column=1, padx=5, pady=5)
        
def check_number_is_in_both_lists(number, list1, list2):
    # Check if the number appears in either list
    found_in_list1 = any(number in string for string in list1)
    found_in_list2 = any(number in string for string in list2)
    if found_in_list1 and found_in_list2:
        return "Both"
    else:
        print("not both")
        num=check_number_in_either_list(number, list1, list2)
        return num
    
def check_number_in_either_list(number, list1, list2):
    # Check if the number appears in a string within either list
    for string in list1:
        if number in string:
            print(number)
            print(1)
            return 1
    for string in list2:
        if number in string:
            print(number)
            print(2)
            return 2


def add_string_after_final_backslash(strings, extra_string):
    modified_strings = []
    for string in strings:
        parts = string.rsplit('\\', 1)  # Split the string at the last '\\'
        if len(parts) == 2:  # Ensure there is at least one '\\'
            modified_string = parts[0] + '\\' + extra_string + parts[1]
            modified_strings.append(modified_string)
        else:
            # If there's no '\\', simply add the extra string at the end
            modified_strings.append(string + '\\' + extra_string)
    return modified_strings



def create_image_display(compare_list,Low_ass_location):
    compare_list_index = 0  # Initialize the index variable
    accepted_images = []
    rejected_images = []
    new_home = []
    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            ctk.set_appearance_mode('dark')
            self.geometry('1000x600')
            self.title('Image Inspector')
            self.minsize(1400,800)
            self.window_closed = False 
            self.compare_list = compare_list
            self.current_index = 0
            #layout
            
            self.rowconfigure(0, weight= 6)
            self.rowconfigure(1, weight= 1)
            
            self.columnconfigure(0, weight= 3)
            self.columnconfigure(1, weight= 3)
            
            self.accept_button = None
            self.reject_button = None
            #widgets
            self.initialize_display()
            
            
        def initialize_display(self):
            if self.current_index < len(self.compare_list):
                two_images = self.compare_list[self.current_index]
                self.import_image(two_images, Low_ass_location)
            else:
                print("done")
                self.return_results()
            
        def import_image(self,two_images,Low_ass_location):
            print("Entered Import Image")
            image1=two_images[0]
            image2=two_images[1]
            image1_loc=os.path.join(Low_ass_location, image1).replace('/', '\\')
            image2_loc=os.path.join(Low_ass_location, image2).replace('/', '\\')
            
            Accept_location=os.path.join(Low_ass_location, "Accepted").replace('/', '\\')
            Reject_location=os.path.join(Low_ass_location, "Rejected").replace('/', '\\')
            
            image1_loc_a=os.path.join(Accept_location, image1).replace('/', '\\')
            image1_loc_r=os.path.join(Reject_location, image1).replace('/', '\\')
            
            image2_loc_a=os.path.join(Accept_location, image2).replace('/', '\\')
            image2_loc_r=os.path.join(Reject_location, image2).replace('/', '\\')
            self.image_path1=image1_loc
            self.image_path2=image2_loc
            self.image1=Image.open(image1_loc)
            self.image2=Image.open(image2_loc)
           
            # Get the maximum dimensions of the images
            max_width = max(self.image1.width, self.image2.width)
            max_height = max(self.image1.height, self.image2.height)
            

            # Resize the images to have equal dimensions
            self.image1 = self.image1.resize((max_width, max_height))
            self.image2 = self.image2.resize((max_width, max_height))

            # Convert images to Tkinter PhotoImage objects
            self.image_ratio1 = self.image1.size[0] / self.image1.size[1]
            self.image_ratio2 = self.image2.size[0] / self.image2.size[1]
            self.image_tk1 = ImageTk.PhotoImage(self.image1)
            self.image_tk2 = ImageTk.PhotoImage(self.image2)
            
            if hasattr(self, 'image_output1'):
                self.image_output1.destroy()  # Remove the previous ImageOutput1 instance if exists
            if hasattr(self, 'image_output2'):
                self.image_output2.destroy()  # Remove the previous ImageOutput2 instance if exists
           
            self.image_output1 = ImageOutput1(self,self.resize_image)
            self.image_output2 = ImageOutput2(self,self.resize_image)
            
            self.accept_button=Output_accept(self,self.close_choice)
            self.reject_button=Output_reject(self,self.close_choice)
            self.accept_button.grid(row=1, column=0, padx=5, pady=5)
            self.reject_button.grid(row=1, column=1, padx=5, pady=5)
            
        def resize_image(self, event):
            canvas_ratio=event.width / event.height
            if canvas_ratio > self.image_ratio1:
                image_height1 = int(event.height)
                image_width1 = int(image_height1 * self.image_ratio1)
            else:
                image_width1 = int(event.width)
                image_height1 = int(image_width1 / self.image_ratio1)
            
            if canvas_ratio > self.image_ratio2:
                image_height2 = int(event.height)
                image_width2 = int(image_height2 * self.image_ratio2)
            else:
                image_width2 = int(event.width)
                image_height2 = int(image_width2 / self.image_ratio2)
            self.image_output1.delete("all")
            self.image_output2.delete("all")
            resized_image1=self.image1.resize((image_width1,image_height1))
            resized_image2=self.image2.resize((image_width2,image_height2))
            self.image_tk1=ImageTk.PhotoImage(resized_image1)
            self.image_tk2=ImageTk.PhotoImage(resized_image2)
            
            self.image_output1.create_image(event.width /2 , event.height /2 , image=self.image_tk1)
            #self.image_output1.grid(row=0, column=0, padx=5, pady=5)
            self.image_output2.create_image(event.width /2 , event.height /2 , image=self.image_tk2)
            #self.image_output2.grid(row=0, column=1, padx=5, pady=5)
            
        def return_results(self):
            # Handle returning the accepted and rejected images
            # Finally, close the application
            simple_accepted_images=[]
            simple_rejected_images=[]
            for image in accepted_images:
                simple_accepted_images.append(image.split('\\')[-1])
            for image in rejected_images:
                simple_rejected_images.append(image.split('\\')[-1])
                
            simple_whole_list = simple_accepted_images + simple_rejected_images
            whole_list=accepted_images+rejected_images
            self.display_results(simple_accepted_images,simple_rejected_images,whole_list,simple_whole_list )


            return accepted_images, rejected_images
                
        def display_results(self,simple_accepted_images,simple_rejected_images,whole_list,simple_whole_list):
             # Clear previous content
            self.clear_display()
            
            # Create labels for listbox titles
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight= 6)
            self.rowconfigure(2, weight= 1)
            accepted_label = tk.Label(self, text="Accepted Images", fg="white", bg="black")
            rejected_label = tk.Label(self, text="Rejected Images", fg="white", bg="black")

            # Position the labels
            accepted_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))
            rejected_label.grid(row=0, column=1, padx=(5, 10), pady=(10, 5))

            # Create the listboxes
            accepted_listbox = tk.Listbox(self, name="accepted_listbox", fg="black")
            rejected_listbox = tk.Listbox(self, name="rejected_listbox", fg="black")

            # Position the listboxes
            accepted_listbox.grid(row=1, column=0, padx=(10, 5), pady=(0, 5))
            rejected_listbox.grid(row=1, column=1, padx=(5, 10), pady=(0, 5))

                # Display accepted images in the left listbox
            unique_ID = set()
            for item in simple_whole_list:
                parts = item.split(' ')[0]
                unique_ID.add(parts)
            for item in unique_ID:
                temp_list_A=[]
                temp_list_R=[]
                result=check_number_is_in_both_lists(item, simple_accepted_images, simple_rejected_images)
                print(result)
                if result == "Both":
                    print("The number is present in both lists.")
                    for items in simple_accepted_images:
                        if items.split(' ')[0] == item:
                            temp_list_A.append(items)
                    for items in simple_rejected_images:
                        if items.split(' ')[0] == item:
                            temp_list_R.append(items)
                    if (temp_list_A[0].split(' ')[1] == temp_list_A[1].split(' ')[1]):
                        if (temp_list_A[0].split(' ')[1].lower() != "view"):
                            combined=temp_list_A[0].split(' ')[0]+ "( " +temp_list_A[0].split(' ')[1]+" )"
                        else:
                            combined=temp_list_A[0].split(' ')[0]+ "( NOT " +temp_list_R[0].split(' ')[1]+" Connector )"
                        accepted_listbox.insert(tk.END, combined)
                        print(combined)
                    if (temp_list_R[0].split(' ')[1] == temp_list_R[1].split(' ')[1]):
                        if (temp_list_R[0].split(' ')[1].lower() != "view"):
                            combined=temp_list_R[0].split(' ')[0]+ "( " +temp_list_R[0].split(' ')[1]+" )"
                        else:
                            combined=temp_list_R[0].split(' ')[0]+ "( NOT " +temp_list_A[0].split(' ')[1]+" Connector )"
                        rejected_listbox.insert(tk.END, combined)
                        print(combined)
                else: #the number is present in one list
                    if result == 1:
                        accepted_listbox.insert(tk.END, item)
                        print(item)
                    elif result == 2:
                        rejected_listbox.insert(tk.END, item)
                        print(item)
            self.approve_button=Output_Approve(self,self.mover)
            self.disapprove_button=Output_Disapprove(self,self.mover)
            self.approve_button.grid(row=2, column=0, padx=5, pady=5)
            self.disapprove_button.grid(row=2, column=1, padx=5, pady=5)
                
                        
        def mover(self, button):
            if button == "Approve":
                tempA=add_string_after_final_backslash(accepted_images,"Accepted\\")
                tempB=add_string_after_final_backslash(rejected_images,"Rejected\\")
                new_home=tempA+tempB
                print(new_home)
                whole_list=accepted_images+rejected_images
                for i in range(len(whole_list)):
                    move_file(whole_list[i],new_home[i])            
                self.on_close()
                print("Approve button clicked")
            elif button == "Disapprove":
                # Handle reject button click
                print("Disapproved button clicked")
                self.on_close()
                
            
            
            
            
        def close_choice(self, button):
            if button == "accept":
                accepted_images.append(self.image_path1)
                accepted_images.append(self.image_path2)
                print("Accept button clicked")
            elif button == "reject":
                # Handle reject button click
                rejected_images.append(self.image_path1)
                rejected_images.append(self.image_path2)
                print("Reject button clicked")
            self.current_index += 1  # Move to the next pair of images
            self.clear_display()
            self.initialize_display()  # Initialize next pair of images

        def clear_display(self):
            # Clear previous images and buttons
            if hasattr(self, 'image_output1'):
                self.image_output1.destroy()
            if hasattr(self, 'image_output2'):
                self.image_output2.destroy()
                
                
        def on_close(self):
            self.window_closed = True
            self.destroy()
            
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Handle window close event
    app.mainloop()
    
    return accepted_images, rejected_images
            

            
            
            
    

























