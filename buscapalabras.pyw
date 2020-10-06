import tkinter as tk
import os, threading, unicodedata


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        listbox_border = tk.Frame(self, bd=1, relief="sunken", background="#fffaf0")
        listbox_border.pack(padx=6, pady=6, fill=None, expand=False)
        self.listbox = tk.Listbox(listbox_border, width=20, height=10,
                    borderwidth=0, highlightthickness=0,
                    background=listbox_border.cget("background"))
        
        scrollbar = tk.Scrollbar(listbox_border, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        intro = [ "Buscador de palabras", "",
                "Intruduce las", "letras disponibles", "",
                "Puedes usar ?", "como comodín."]
        self.listbox.insert(0, *intro)
        self.listbox.pack(padx=4, pady=4, fill="both", expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(padx=6, pady=(0,6), fill="x")
        self.entry.bind('<Return>',self.multi)

    def can_spell(self, letters, word):
        word = list(unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8'))
        letters = list(letters)
        wildcards = 0

        while letters.count("?"):
            letters.remove("?")
            wildcards += 1

        for letter in letters:
            if letter in word:
                word.remove(letter)

        return len(word) <= wildcards

    def search(self):
        letters = self.entry.get()
        self.entry.config(state="disabled")
        self.listbox.delete(0, tk.END)
        with open(os.path.dirname(__file__) + "/palabras.txt", 'r') as words_file:
            for line in words_file:
                word = line.strip()
                if len(word) > len(letters):
                    continue
                if self.can_spell(letters, word):
                    self.listbox.insert(tk.END, word)
        self.entry.config(state="normal")

    def multi(self, event):
        threading.Thread(target=self.search).start()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Buscador')
    root.resizable(0, 0)
    root.option_add("*Font", ("Consolas", 14))
    app = Application(master=root)
    app.mainloop()
