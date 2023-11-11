import tkinter as tk
from tkinter import ttk
import re


class FindWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('400x100')
        self.title('Search')
        self.configure(bg="white")
        
        self.text = parent.text
        
        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Add a weight to make the frame fill the parent
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.find_label = ttk.Label(self.frame, text='Find Word')
        self.find_entry = ttk.Entry(self.frame)
        self.find_btn = ttk.Button(self.frame, text='Find',
                command=self.find)
        self.find_label.grid(row=1, column=0, sticky="nsew", padx=5)
        self.find_entry.grid(row=1, column=1, sticky="nsew")
        self.find_btn.grid(row=1, column=2, sticky="nsew", padx=5)
        
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.frame.columnconfigure(0, weight=2)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=2)
        self.word_to_find = self.find_entry.get()
        self.counter = 0

    def find(self):
        if self.word_to_find != self.find_entry.get():
            self.word_to_find = self.find_entry.get()
            self.counter = 0
        if self.word_to_find:
            text = self.text.get(1.0, tk.END)
            text = text.lower()  # Convert the text to lowercase for case-insensitive search
            word_to_find = self.word_to_find.lower()

            # Find all occurrences of the word
            matches = [m.start() for m in re.finditer(fr'\b{re.escape(word_to_find)}\b', text)]
            
            # Remove previous highlights
            self.text.tag_remove("highlight", "1.0", tk.END)

            # If there are matches, highlight the first word with a red background
            if matches:
                current_index = matches[0 + self.counter]
                current_end_index = current_index + len(word_to_find)
                self.text.tag_add("red_highlight", f"1.0+{current_index}c", f"1.0+{current_end_index}c")
                self.text.tag_config("red_highlight", background="red")
                
                # If there are more matches, highlight them in blue
                for start_index in matches:
                    # if start_index == current_index:
                    #     continue
                    end_index = start_index + len(word_to_find)
                    self.text.tag_add("highlight", f"1.0+{start_index}c", f"1.0+{end_index}c")
                    self.text.tag_config("highlight", background="blue")
                self.text.tag_remove("red_highlight", "1.0", tk.END)
                match_length = len(matches) -1
                if self.counter < match_length:
                    self.counter += 1
                    self.text.tag_add("red_highlight", f"1.0+{current_index}c", f"1.0+{current_end_index}c")
                else:
                    self.counter = 0
            else:
                self.matches = []



class ReplaceWindow(FindWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Replace')
        self.geometry('400x180')

        self.replace_label = ttk.Label(self.frame, text='Replace')
        self.replace_entry = ttk.Entry(self.frame)
        self.replace_btn = ttk.Button(self.frame, text='Replace',
                command=self.replace)
        self.replace_all_btn = ttk.Button(self.frame, text='Replace All',
                command=self.replace_all)
        
        self.replace_label.grid(row=2, column=0, sticky="nsew", padx=5)
        self.replace_entry.grid(row=2, column=1, sticky="nsew", pady=10)
        self.replace_btn.grid(row=2, column=2, sticky="nsew", padx=5)
        self.replace_all_btn.grid(row=3, column=2, sticky="nsew", padx=5)
        
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(4, weight=2)
    
    def replace(self):
        word_to_find = self.find_entry.get()
        word_to_replace = self.replace_entry.get()
        if word_to_find:
            text = self.text.get(1.0, tk.END)
            text = text.lower()
            word_to_find = word_to_find.lower()
            matches = [m.start() for m in re.finditer(fr'\b{re.escape(word_to_find)}\b', text)]
            

            # Replace all occurrences of the word
            text = text[:matches[self.counter - 1]] + word_to_replace + text[matches[self.counter -1] + len(word_to_find):]
            
            # Update the text widget with the modified text
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, text)
        
    def replace_all(self):
        word_to_find = self.find_entry.get()
        word_to_replace = self.replace_entry.get()
        if word_to_find and word_to_replace:
            text = self.text.get(1.0, tk.END)
            text = text.lower()  # Convert the text to lowercase for case-insensitive search
            word_to_find = word_to_find.lower()

            # Replace all occurrences of the word
            text = re.sub(fr'\b{re.escape(word_to_find)}\b', word_to_replace, text)
            
            # Update the text widget with the modified text
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, text)