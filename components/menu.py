# components.menu

import tkinter as tk
from tkinter import ttk, filedialog

class TextEditorMenu:
    def __init__(self, root, text_editor):
        self.root = root
        self.text_editor = text_editor

        # Create a menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.menu_bar.config(tearoff=False)

        # Create the File menu
        self.file_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.text_editor.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.text_editor.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.text_editor.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=self.text_editor.save_file_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.text_editor.exit_app)

        # Create the Edit menu
        print("TextEditorMenu __init__ called")
        
        
import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, relief="flat")
        self.master = master
        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_help_menu()

    def create_file_menu(self):
        self.file_menu = tk.Menu(self, relief="flat")
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.exit_app) 

    def create_edit_menu(self):
        self.edit_menu = tk.Menu(self, relief="flat")
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Select All", command=self.master.select_all, accelerator="Ctrl+A")
        self.edit_menu.add_command(label="Find", command=self.master.find, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Find and Replace", command=self.master.replace, accelerator="Ctrl+H")
        
    def create_view_menu(self):
        self.view_menu = tk.Menu(self, relief="flat")
        self.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_checkbutton(label="Word Wrap", command=self.master.toggle_word_wrap, accelerator="Ctrl+W")

    def create_help_menu(self):
        help_menu = tk.Menu(self, tearoff=0, relief="flat")  
        help_menu.add_command(label="About", command=self.master.toggle_word_wrap)  
        help_menu.add_command(label="Get Started", command=self.master.toggle_word_wrap)  
        help_menu.add_command(label="How To...", command=self.master.toggle_word_wrap)  
        self.add_cascade(label="Help", menu=help_menu) 
        
    def new_file(self):
        self.master.current_file = None
        self.master.text.delete(1.0, tk.END)
        self.master.update_status()
        
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.master.text.delete(1.0, tk.END)
                self.master.text.insert(tk.END, file.read())
            self.master.current_file = file_path
            self.master.save_last_opened_file()
            self.master.update_status()

    def save_file(self):
        if self.master.current_file:
            with open(self.master.current_file, "w") as file:
                file.write(self.master.text.get(1.0, tk.END))
            self.master.save_last_opened_file()
            self.master.update_status()
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.master.text.get(1.0, tk.END))
            self.master.current_file = file_path
            self.master.save_last_opened_file()
            self.master.update_status()

 
