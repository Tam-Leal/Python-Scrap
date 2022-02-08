import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import csv
import stores


class GuiConcorrencia(object):
    def __init__(self):

        # Window Properties
        self.image = None
        self.window = tk.Tk()
        self.window.title('Market Analysis')
        self.window.geometry("700x670+300+20")
        self.window.bind("<ButtonRelease-1>", self.show_image)

        # Window Search Widgets
        img1 = tk.PhotoImage(file='./assets/global.png')
        self.btn_markets = tk.Button(self.window, text="  Market  ", command=self.search, image=img1,
                                     compound='left', bd=1)

        self.btn_markets.grid(row=0, sticky='nw', padx=20, pady=5)

        self.label_count_market = tk.Label(self.window, relief='groove', text="Nº Records:")
        self.label_count_market.place(x=470, y=28)

        self.label_count_filter = tk.Label(self.window, relief='groove', text="Nº Records:")
        self.label_count_filter.place(x=470, y=445)

        # Treeview search Markets
        self.tree = tk.ttk.Treeview(self.window, height=17)
        self.tree.grid(row=1, pady=5)
        self.tree["columns"] = ("one", "two")
        self.tree.column("#0", width=300, minwidth=270, stretch=tk.NO, anchor='center')
        self.tree.heading("#0", text="Product", anchor=tk.CENTER)

        self.tree.column("one", width=100, minwidth=150, stretch=tk.NO, anchor='center')
        self.tree.heading("one", text="Price/Kg", anchor=tk.CENTER)

        self.tree.column("two", width=150, minwidth=150, stretch=tk.NO, anchor='center')
        self.tree.heading("two", text="Local", anchor=tk.CENTER)

        # Canvas for image product
        label_hint = tk.Label(self.window, font=("Arial", 8), text="Product Image")
        label_hint.place(x=570, y=270)
        panel = tk.Canvas(self.window, width=120, height=120, highlightthickness=1,
                          highlightbackground="black")  # ---> Canvas to show product image
        panel.place(x=570, y=295)

        # Filter Widgets
        self.ent_search = tk.ttk.Entry(self.window)
        self.ent_search.grid(row=2, sticky="nw", padx=20, pady=10)
        self.ent_search.bind("<BackSpace>", self.delete_filter_tree)

        self.btn_filter_tree = tk.ttk.Button(self.window, text='Filter', command=self.filter_tree)
        self.btn_filter_tree.grid(row=2, sticky="nw", padx=160, pady=8)

        # Treview Filter
        self.tree_filter = tk.ttk.Treeview(self.window, height=8)
        self.tree_filter.grid(row=3, pady=5, padx=10)
        self.tree_filter["columns"] = ("one", 'two')
        self.tree_filter.column("#0", width=300, minwidth=270, stretch=tk.NO, anchor='center')
        self.tree_filter.heading("#0", text="Product", anchor=tk.CENTER)

        self.tree_filter.column("one", width=100, minwidth=150, stretch=tk.NO, anchor='center')
        self.tree_filter.heading("one", text="Price/Kg", anchor=tk.CENTER)

        self.tree_filter.column("two", width=150, minwidth=150, stretch=tk.NO, anchor='center')
        self.tree_filter.heading("two", text="Local", anchor=tk.CENTER)

        self.window.mainloop()

    def search(self):
        # clear csv before start
        f = open("table/datas.csv", "w")
        f.truncate()
        f.close()

        stores.gadaria()
        stores.intermezzo()
        stores.meatbox()

        with open(r'table/datas.csv', 'r') as f:
            data = csv.reader(f)
            next(data)
            for row in data:
                self.tree.insert("", 'end', text=row[0], values=(row[1], row[2]))

        # Count itens
        item_count = len(self.tree.get_children())
        self.label_count_market['text'] = f'Nº Records: {item_count}'

    def filter_tree(self):
        query = self.ent_search.get()
        selections = []
        for child in self.tree.get_children():
            if query in self.tree.item(child)['text'].lower():  # compare strings in  lower cases.
                selections.append(child)
                self.tree_filter.insert("", 'end', text=self.tree.item(child)['text'], values=(
                    self.tree.item(child)['values'][0], self.tree.item(child)['values'][1]))

        self.tree.selection_set(selections)  # ---> Products filtered stay blue

        item_count = len(self.tree_filter.get_children())  # ---> Count items
        self.label_count_filter['text'] = f'Nº Records: {item_count}'

    def delete_filter_tree(self, *args):
        self.tree_filter.delete(*self.tree_filter.get_children())
        self.ent_search.delete(0, 'end')
        self.label_count_filter['text'] = 'Nº Records:'

        item_count = len(self.tree_filter.get_children())  # ---> Count items
        self.label_count_filter['text'] = f'Nº Records: {item_count}'

    def show_image(self, *args):
        try:
            selected = self.tree.item(self.tree.selection()[0])['text']
            with open(r'table/datas.csv', 'r') as f:
                data = csv.reader(f)
                next(data)
                for row in data:
                    if row[0] == selected:
                        url = row[3]

                        req = requests.get(url)
                        pilImage = Image.open(BytesIO(req.content))
                        pilImage = pilImage.resize((140, 130), Image.ANTIALIAS)
                        self.image = ImageTk.PhotoImage(pilImage)

                panel = tk.Canvas(self.window, width=120, height=125, highlightthickness=1,
                                  highlightbackground="black")  # ---> Canvas to show product image
                panel.create_image(60, 60, image=self.image)
                panel.place(x=570, y=290)

        except Exception as tag:
            print(tag)


if __name__ == '__main__':
    GuiConcorrencia()
