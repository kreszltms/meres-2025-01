import tkinter as tk
from tkinter import filedialog, messagebox
import csv


class Fuggohid:
    def __init__(self, helyezes, nev, foldrajzi_hely, orszag, hossz, atadas_eve):
        self.helyezes = helyezes
        self.nev = nev
        self.foldrajzi_hely = foldrajzi_hely
        self.orszag = orszag
        self.hossz = hossz
        self.atadas_eve = atadas_eve

    def __str__(self):
        return f"{self.nev} ({self.orszag}) - {self.hossz} m, {self.atadas_eve}"


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Függőhidak Kezelése")
        self.geometry("600x400")
        self.fuggohidak = []

        self.create_widgets()

    def create_widgets(self):
        # ListBox a hidak neveinek megjelenítésére
        self.listbox_hidak = tk.Listbox(self)
        self.listbox_hidak.pack(fill=tk.BOTH, expand=True)
        self.listbox_hidak.bind('<<ListboxSelect>>', self.on_select_hid)

        # Szövegdobozok a híd adatainak megjelenítésére
        self.text_nev = tk.Entry(self, state='readonly')
        self.text_nev.pack(fill=tk.X)
        self.text_hely = tk.Entry(self, state='readonly')
        self.text_hely.pack(fill=tk.X)
        self.text_orszag = tk.Entry(self, state='readonly')
        self.text_orszag.pack(fill=tk.X)
        self.text_hossz = tk.Entry(self, state='readonly')
        self.text_hossz.pack(fill=tk.X)
        self.text_ev = tk.Entry(self, state='readonly')
        self.text_ev.pack(fill=tk.X)

        # Rádiógombok a szűréshez (2000 előtti és utáni hidak)
        self.radio_var = tk.IntVar()
        self.radio_elotte = tk.Radiobutton(self, text="2000 előtt épült", variable=self.radio_var, value=1, command=self.filter_hidak)
        self.radio_elotte.pack(anchor='w')
        self.radio_utan = tk.Radiobutton(self, text="2000 után épült", variable=self.radio_var, value=2, command=self.filter_hidak)
        self.radio_utan.pack(anchor='w')

        # Menü
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Fájl megnyitás", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Kilépés", command=self.quit)
        self.menu_bar.add_cascade(label="Fájl", menu=self.file_menu)
        self.config(menu=self.menu_bar)

        # Keresés gomb
        self.search_button = tk.Button(self, text="Keresés", command=self.open_search_form)
        self.search_button.pack(pady=10)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.read_csv(file_path)
            except Exception as e:
                messagebox.showerror("Hiba", f"Nem sikerült beolvasni a fájlt: {e}")

    def read_csv(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            next(reader)  # Skip the header line
            self.fuggohidak.clear()
            for row in reader:
                helyezes = int(row[0])
                nev = row[1]
                foldrajzi_hely = row[2]
                orszag = row[3]
                hossz = int(row[4])
                atadas_eve = int(row[5])
                fuggohid = Fuggohid(helyezes, nev, foldrajzi_hely, orszag, hossz, atadas_eve)
                self.fuggohidak.append(fuggohid)
            self.update_listbox()

    def update_listbox(self):
        self.listbox_hidak.delete(0, tk.END)
        for hid in self.fuggohidak:
            self.listbox_hidak.insert(tk.END, hid.nev)

    def on_select_hid(self, event):
        selected_index = self.listbox_hidak.curselection()
        if selected_index:
            selected_hid = self.fuggohidak[selected_index[0]]
            self.text_nev.config(state='normal')
            self.text_nev.delete(0, tk.END)
            self.text_nev.insert(0, selected_hid.nev)
            self.text_nev.config(state='readonly')

            self.text_hely.config(state='normal')
            self.text_hely.delete(0, tk.END)
            self.text_hely.insert(0, selected_hid.foldrajzi_hely)
            self.text_hely.config(state='readonly')

            self.text_orszag.config(state='normal')
            self.text_orszag.delete(0, tk.END)
            self.text_orszag.insert(0, selected_hid.orszag)
            self.text_orszag.config(state='readonly')

            self.text_hossz.config(state='normal')
            self.text_hossz.delete(0, tk.END)
            self.text_hossz.insert(0, str(selected_hid.hossz))
            self.text_hossz.config(state='readonly')

            self.text_ev.config(state='normal')
            self.text_ev.delete(0, tk.END)
            self.text_ev.insert(0, str(selected_hid.atadas_eve))
            self.text_ev.config(state='readonly')

    def filter_hidak(self):
        filtered_hidak = []
        if self.radio_var.get() == 1:  # 2000 előtt
            filtered_hidak = [hid for hid in self.fuggohidak if hid.atadas_eve < 2000]
        elif self.radio_var.get() == 2:  # 2000 után
            filtered_hidak = [hid for hid in self.fuggohidak if hid.atadas_eve >= 2000]

        self.listbox_hidak.delete(0, tk.END)
        for hid in filtered_hidak:
            self.listbox_hidak.insert(tk.END, hid.nev)

    def open_search_form(self):
        search_form = SearchForm(self.fuggohidak)
        search_form.grab_set()


class SearchForm(tk.Toplevel):
    def __init__(self, fuggohidak):
        super().__init__()
        self.title("Keresés")
        self.geometry("400x300")
        self.fuggohidak = fuggohidak

        self.combo_orszag = tk.StringVar()
        self.combo_box = tk.OptionMenu(self, self.combo_orszag, *sorted(set(h.orszag for h in fuggohidak)))
        self.combo_box.pack(pady=10)

        self.search_button = tk.Button(self, text="Keresés", command=self.search)
        self.search_button.pack(pady=10)

        self.result_text = tk.Text(self, height=10, width=40)
        self.result_text.pack(pady=10)

        self.close_button = tk.Button(self, text="Bezárás", command=self.destroy)
        self.close_button.pack(pady=10)

    def search(self):
        selected_country = self.combo_orszag.get()
        results = [hid.nev for hid in self.fuggohidak if hid.orszag == selected_country]
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "\n".join(results))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
