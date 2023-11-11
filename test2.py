"""Text widget with spell checking.

Requires installation of pyenchant
"""

import tkinter as tk
import tkinter.ttk as ttk
from enchant import Dict, tokenize
import sys

class SpellcheckText(tk.Text):
    locale = 'en_US'
    def __init__(self, master, **kwargs):
        self.afterid = None
        self.corpus = Dict(self.locale)
        self.tokenize = tokenize.get_tokenizer(self.locale)
        super(SpellcheckText, self).__init__(master, **kwargs)
        self._proxy = self._w + "_proxy"
        self.tk.call("rename", self._w, self._proxy)
        self.tk.createcommand(self._w, self._proxycmd)
        self.tag_configure('sic', foreground='red')
        self.bind('<<TextModified>>', self.on_modify)

    def _proxycmd(self, command, *args):
        """Intercept the Tk commands to the text widget and if eny of the content
        modifying commands are called, post a TextModified event."""
        cmd = (self._proxy, command)
        if args:
            cmd = cmd + args
        result = self.tk.call(cmd)
        if command in ('insert', 'delete', 'replace'):
            self.event_generate('<<TextModified>>')
        return result

    def on_modify(self, event):
        """Rate limit the spell-checking with a 100ms delay. If another modification
        event comes in within this time, cancel the after call and re-schedule."""
        try:
            if self.afterid:
                self.after_cancel(self.afterid)
            self.afterid = self.after(100, self.on_modified)
        except Exception as e:
            print(e)

    def on_modified(self):
        """Handle the spell check once modification pauses.
        The tokenizer works on lines and yields a list of (word, column) pairs
        So iterate over the words and set a sic tag on each spell check failed word."""
        self.afterid = None
        self.tag_remove('sic', '1.0', 'end')
        num_lines = [int(val) for val in self.index("end").split(".")][0]
        for line in range(1, num_lines):
            data = self.get(f"{line}.0 linestart", f"{line}.0 lineend")
            for word,pos in self.tokenize(data):
                check = self.corpus.check(word)
                print(f"{word},{pos},{check}")
                if not check:
                    start = f"{line}.{pos}"
                    end = f"{line}.{pos + len(word)}"
                    self.tag_add("sic", start, end)


class App(ttk.Frame):
    def __init__(self, master, **kwargs):
        super(App, self).__init__(master, **kwargs)
        master.wm_withdraw()
        self.create_ui()
        self.grid(row=0, column=0, sticky=tk.NSEW)
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.wm_deiconify()

    def create_ui(self):
        text = SpellcheckText(self)
        vs = ttk.Scrollbar(self, command=text.yview)
        text.configure(yscrollcommand=vs.set)
        text.grid(row=0, column=0, sticky=tk.NSEW)
        vs.grid(row=0, column=1, sticky=tk.NSEW)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

def main(args=None):
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))