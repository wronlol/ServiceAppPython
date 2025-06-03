import tkinter as tk
from tkinter import messagebox, ttk
import database # Importujemy nasz moduł bazy danych
from datetime import datetime

class ServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikacja do Zarządzania Serwisem Sprzętu")
        self.root.geometry("1200x700")
        
        self.sort_column = 'Data Przyjęcia'
        self.sort_reverse = True
        
        self.selected_sprzet_id = None 

        database.create_table()
        self.create_widgets()
        self.load_sprzet_to_treeview(sort_by_column=self.sort_column, sort_reverse=self.sort_reverse)
        
    def sort_treeview_column(self, col):
        """Sortuje dane w Treeview po kliknięciu nagłówka kolumny."""
        # Pobierz wszystkie elementy z Treeview
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        
        # Jeśli kliknięto w tę samą kolumnę, odwróć kierunek sortowania
        if col == self.sort_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False # Domyślnie sortuj rosnąco dla nowej kolumny
        
        # Ustal funkcję klucza do sortowania w zależności od typu danych
        def sort_key(item_value):
            if col in ["Data Przyjęcia", "Data Wydania"]:
                # Spróbuj przekonwertować na datę, jeśli to możliwe, w przeciwnym razie pozostaw jako string
                try:
                    return datetime.strptime(item_value, "%Y-%m-%d")
                except ValueError:
                    return item_value # Jeśli format daty jest zły, sortuj jako string
            elif col == "ID" or col == "Koszt Naprawy":
                try:
                    return float(item_value)
                except ValueError:
                    return 0 # Wartość domyślna dla błędnych liczb
            return item_value.lower() if isinstance(item_value, str) else item_value


        # Sortuj dane
        data.sort(key=lambda t: sort_key(t[0]), reverse=self.sort_reverse)

        # Zmień kolejność elementów w Treeview
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index) # Przenieś element na nową pozycję
        
        # Aktualizuj nagłówek kolumny, aby pokazać strzałkę sortowania
        self.tree.heading(col, text=f"{col} {'↓' if self.sort_reverse else '↑'}")
        
        # Zresetuj inne nagłówki, aby usunąć strzałki sortowania
        for other_col in self.tree['columns']:
            if other_col != col:
                self.tree.heading(other_col, text=other_col.replace('↓', '').replace('↑', '').strip())    
    

    def set_today_date(self):
        """Ustawia dzisiejszą datę w polu 'Data Przyjęcia'."""
        if 'data_przyjecia' in self.entries and isinstance(self.entries['data_przyjecia'], tk.Entry):
            self.entries['data_przyjecia'].delete(0, tk.END) # Najpierw wyczyść
            self.entries['data_przyjecia'].insert(0, datetime.now().strftime("%Y-%m-%d"))

    def set_today_issue_date(self): # <--- DODAJ TĘ FUNKCJĘ
        """Ustawia dzisiejszą datę w polu 'Data Wydania'."""
        if 'data_wydania' in self.entries and isinstance(self.entries['data_wydania'], tk.Entry):
            self.entries['data_wydania'].delete(0, tk.END) # Najpierw wyczyść
            self.entries['data_wydania'].insert(0, datetime.now().strftime("%Y-%m-%d"))
    

    def create_widgets(self):
        # --- Frame dla formularza i przycisków akcji ---
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Sekcja formularza
        form_frame = tk.LabelFrame(control_frame, text="Dane sprzętu", padx=10, pady=10)
        form_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        labels_info = [
            {"text": "Nazwa Sprzętu:", "key": "nazwa_sprzetu"},
            {"text": "Marka/Model:", "key": "marka_model"},
            {"text": "Numer Inw:", "key": "numer_seryjny"},
            {"text": "Opis Usterki:", "key": "opis_usterki"},
            {"text": "Nazwisko Klienta:", "key": "nazwisko_klienta"},
            {"text": "Telefon Klienta:", "key": "telefon_klienta"},
            {"text": "Data Przyjęcia:", "key": "data_przyjecia"},
            {"text": "Data Wydania:", "key": "data_wydania"},
            {"text": "Status:", "key": "status"},
            {"text": "Koszt Naprawy:", "key": "koszt_naprawy"},
            {"text": "Uwagi:", "key": "uwagi"}
        ]
        
        self.entries = {} # Słownik do przechowywania referencji do widżetów Entry
        
        for i, label_data in enumerate(labels_info):
            key = label_data["key"]
            text = label_data["text"]

            tk.Label(form_frame, text=text).grid(row=i, column=0, sticky="w", pady=2)

            if key == "status":
                status_options = ["Przyjęty", "Wydany"] # Zmienione opcje
                self.status_var = tk.StringVar(self.root)
                self.status_var.set("Przyjęty") # Domyślna wartość, możesz zmienić na inną, jeśli wolisz
                status_menu = ttk.OptionMenu(form_frame, self.status_var, *status_options)
                status_menu.grid(row=i, column=1, sticky="ew", pady=2)
                self.entries[key] = self.status_var # Zapisujemy StringVar dla statusu
            elif key == "data_przyjecia": # Sekcja dla Data Przyjęcia
                entry = tk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, sticky="ew", pady=2)
                self.entries[key] = entry
                
                # Dodajemy przycisk obok pola Data Przyjęcia
                set_receive_date_button = tk.Button(form_frame, text="Dzisiaj", command=self.set_today_date)
                set_receive_date_button.grid(row=i, column=2, padx=5, sticky="w")
                # Ustawiamy od razu dzisiejszą datę przy tworzeniu pola
                # self.set_today_receive_date() # Opcjonalnie: możesz zakomentować, jeśli wolisz, żeby pole było puste domyślnie
            elif key == "data_wydania": # Sekcja dla Data Wydania
                entry = tk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, sticky="ew", pady=2)
                self.entries[key] = entry
                
                # Dodajemy przycisk obok pola Data Wydania
                set_issue_date_button = tk.Button(form_frame, text="Dzisiaj", command=self.set_today_issue_date)
                set_issue_date_button.grid(row=i, column=2, padx=5, sticky="w")
            else:
                entry = tk.Entry(form_frame, width=40)
                entry.grid(row=i, column=1, sticky="ew", pady=2)
                self.entries[key] = entry # Zapisujemy referencję do Entry

        
        # Sekcja przycisków formularza
        button_form_frame = tk.Frame(form_frame)
        button_form_frame.grid(row=len(labels_info), column=0, columnspan=2, pady=10)
        # Używamy len(labels_info) zamiast len(labels), aby uzyskać poprawny numer wiersza
        button_form_frame.grid(row=len(labels_info), column=0, columnspan=2, pady=10)

        self.add_button = tk.Button(button_form_frame, text="Dodaj Sprzęt", command=self.add_sprzet_to_db)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.update_button = tk.Button(button_form_frame, text="Aktualizuj Sprzęt", command=self.update_sprzet_in_db, state=tk.DISABLED)
        self.update_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(button_form_frame, text="Wyczyść Formularz", command=self.clear_entries)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        
        # --- Sekcja wyszukiwania i operacji na liście ---
        search_frame = tk.LabelFrame(control_frame, text="Wyszukiwanie i Akcje", padx=10, pady=10)
        search_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(search_frame, text="Szukaj:").pack(pady=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<Return>", self.perform_search_event) # Wyszukiwanie po naciśnięciu Enter

        search_button = tk.Button(search_frame, text="Wyszukaj", command=self.perform_search)
        search_button.pack(pady=5)

        refresh_button = tk.Button(search_frame, text="Odśwież Listę", command=self.load_sprzet_to_treeview)
        refresh_button.pack(pady=5)

        delete_button = tk.Button(search_frame, text="Usuń Zaznaczone", command=self.delete_selected_sprzet)
        delete_button.pack(pady=5)

        # --- Frame dla listy sprzętu (Treeview) ---
        list_frame = tk.Frame(self.root, padx=10, pady=10)
        list_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Kolumny dla Treeview
        columns = (
            "ID", "Nazwa Sprzętu", "Marka/Model", "Numer Inw", "Opis Usterki",
            "Nazwisko Klienta", "Telefon Klienta", "Data Przyjęcia", "Data Wydania",
            "Status", "Koszt Naprawy", "Uwagi"
        )
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Paski przewijania
        scrollbar_y = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(side="left", fill="both", expand=True)

        # Ustawienie nagłówków i szerokości kolumn
        for col in columns:
            self.tree.heading(col, text=col, anchor="w", 
                              command=lambda _col=col: self.sort_treeview_column(_col)) # Dodano komendę sortowania
            # Dostosuj szerokości kolumn według potrzeb
            if col == "ID": self.tree.column(col, width=40, minwidth=30)
            elif col == "Nazwa Sprzętu": self.tree.column(col, width=120, minwidth=80)
            elif col == "Marka/Model": self.tree.column(col, width=120, minwidth=80)
            elif col == "Numer Inw": self.tree.column(col, width=100, minwidth=70)
            elif col == "Opis Usterki": self.tree.column(col, width=200, minwidth=150)
            elif col == "Nazwisko Klienta": self.tree.column(col, width=120, minwidth=80)
            elif col == "Telefon Klienta": self.tree.column(col, width=100, minwidth=70)
            elif col == "Data Przyjęcia" or col == "Data Wydania": self.tree.column(col, width=90, minwidth=70)
            elif col == "Status": self.tree.column(col, width=100, minwidth=70)
            elif col == "Koszt Naprawy": self.tree.column(col, width=80, minwidth=60)
            elif col == "Uwagi": self.tree.column(col, width=150, minwidth=100)
            else: self.tree.column(col, width=80, minwidth=50)

        
        # Powiązanie kliknięcia na wiersz z funkcją edycji
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def add_sprzet_to_db(self):
        """Pobiera dane z formularza i dodaje nowy wpis do bazy danych."""
        data = self._get_form_data()
        
        # Podstawowa walidacja
        if not data['nazwa_sprzetu'] or not data['nazwisko_klienta']:
            messagebox.showerror("Błąd Walidacji", "Nazwa sprzętu i Nazwisko klienta są wymagane!")
            return

        try:
            # Próba konwersji koszt_naprawy na float
            data['koszt_naprawy'] = float(data['koszt_naprawy']) if data['koszt_naprawy'] else 0.0
        except ValueError:
            messagebox.showerror("Błąd Walidacji", "Koszt naprawy musi być liczbą!")
            return

        result = database.add_sprzet(data)
        if "Sukces" in result:
            messagebox.showinfo("Informacja", result)
            self.clear_entries()
            self.load_sprzet_to_treeview()
        else:
            messagebox.showerror("Błąd", result)

    def update_sprzet_in_db(self):
        """Aktualizuje zaznaczony wpis sprzętu w bazie danych."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać sprzęt do aktualizacji z listy.")
            return

        sprzet_id = self.tree.item(selected_item, 'values')[0] # Pobieramy ID z pierwszej kolumny

        data = self._get_form_data()

        # Podstawowa walidacja
        if not data['nazwa_sprzetu'] or not data['nazwisko_klienta']:
            messagebox.showerror("Błąd Walidacji", "Nazwa sprzętu i Nazwisko klienta są wymagane!")
            return

        try:
            data['koszt_naprawy'] = float(data['koszt_naprawy']) if data['koszt_naprawy'] else 0.0
        except ValueError:
            messagebox.showerror("Błąd Walidacji", "Koszt naprawy musi być liczbą!")
            return
        
        result = database.update_sprzet(sprzet_id, data)
        if "Sukces" in result:
            messagebox.showinfo("Informacja", result)
            self.clear_entries()
            self.load_sprzet_to_treeview()
            self.add_button.config(state=tk.NORMAL) # Włączamy przycisk Dodaj
            self.update_button.config(state=tk.DISABLED) # Wyłączamy przycisk Aktualizuj
        else:
            messagebox.showerror("Błąd", result)


    def delete_selected_sprzet(self):
        """Usuwa zaznaczony sprzęt z bazy danych po potwierdzeniu."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Proszę wybrać sprzęt do usunięcia.")
            return

        sprzet_id = self.tree.item(selected_item, 'values')[0]
        
        if messagebox.askyesno("Potwierdź usunięcie", f"Czy na pewno chcesz usunąć sprzęt o ID: {sprzet_id}?"):
            result = database.delete_sprzet(sprzet_id)
            if "Sukces" in result:
                messagebox.showinfo("Informacja", result)
                self.load_sprzet_to_treeview()
                self.clear_entries() # Wyczyść formularz po usunięciu
                self.add_button.config(state=tk.NORMAL) 
                self.update_button.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Błąd", result)

    def _get_form_data(self):
        """Pobiera dane z pól formularza i zwraca je jako słownik."""
        data = {
            'nazwa_sprzetu': self.entries['nazwa_sprzetu'].get(),
            'marka_model': self.entries['marka_model'].get(),
            'numer_seryjny': self.entries['numer_seryjny'].get(),
            'opis_usterki': self.entries['opis_usterki'].get(),
            'nazwisko_klienta': self.entries['nazwisko_klienta'].get(),
            'telefon_klienta': self.entries['telefon_klienta'].get(),
            'data_przyjecia': self.entries['data_przyjecia'].get(),
            'data_wydania': self.entries['data_wydania'].get(),
            'status': self.entries['status'].get(),
            'koszt_naprawy': self.entries['koszt_naprawy'].get(),
            'uwagi': self.entries['uwagi'].get()
        }
        return data

    def clear_entries(self):
        """Czyści wszystkie pola formularza i resetuje przyciski."""
        for key, entry_widget in self.entries.items():
            if isinstance(entry_widget, tk.Entry):
                entry_widget.delete(0, tk.END)
        # Resetowanie wartości dla OptionMenu
        self.status_var.set("Przyjęty")
        
        self.add_button.config(state=tk.NORMAL) # Włącz przycisk Dodaj
        self.update_button.config(state=tk.DISABLED) # Wyłącz przycisk Aktualizuj
        self.tree.selection_remove(self.tree.focus()) # Usuń zaznaczenie w Treeview

    def load_sprzet_to_treeview(self, sort_by_column=None, sort_reverse=False):
        """Ładuje wszystkie dane sprzętu z bazy danych do Treeview."""
        # Usuń wszystkie istniejące elementy z Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        sprzet_data = database.get_all_sprzet()
        for item in sprzet_data:
            # item to obiekt sqlite3.Row, który działa jak słownik i jak krotka
            # Spróbujmy użyć dostępu przez indeks, aby uniknąć duplikacji
            self.tree.insert("", "end", values=(
                item[0],  # id
                item[1],  # nazwa_sprzetu
                item[2],  # marka_model
                item[3],  # numer_seryjny
                item[4],  # opis_usterki
                item[5],  # nazwisko_klienta
                item[6],  # telefon_klienta
                item[7],  # data_przyjecia  
                item[8],  # data_wydania
                item[9],  # status
                item[10], # koszt_naprawy
                item[11]  # uwagi
            ))

    def on_tree_select(self, event):
        """Obsługuje kliknięcie na wiersz w Treeview - ładuje dane do formularza."""
        selected_item = self.tree.focus()
        if not selected_item:
            return

        values = self.tree.item(selected_item, 'values')
        
        # Wypełnij pola formularza danymi z wybranego wiersza
        # Upewnij się, że indeksy odpowiadają kolumnom w Treeview
        self.clear_entries() # Najpierw wyczyść
        self.entries['nazwa_sprzetu'].insert(0, values[1])
        self.entries['marka_model'].insert(0, values[2])
        self.entries['numer_seryjny'].insert(0, values[3])
        self.entries['opis_usterki'].insert(0, values[4])
        self.entries['nazwisko_klienta'].insert(0, values[5])
        self.entries['telefon_klienta'].insert(0, values[6])
        self.entries['data_przyjecia'].insert(0, values[7])
        self.entries['data_wydania'].insert(0, values[8])
        self.status_var.set(values[9]) # Ustawienie OptionMenu
        self.entries['koszt_naprawy'].insert(0, values[10])
        self.entries['uwagi'].insert(0, values[11])

        # Zmień stan przycisków: wyłącz "Dodaj", włącz "Aktualizuj"
        self.add_button.config(state=tk.DISABLED)
        self.update_button.config(state=tk.NORMAL)

    def perform_search_event(self, event):
        """Wywołuje wyszukiwanie po naciśnięciu Enter w polu wyszukiwania."""
        self.perform_search()

    def perform_search(self):
        """Przeprowadza wyszukiwanie i aktualizuje Treeview."""
        query = self.search_entry.get().strip()
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not query:
            self.load_sprzet_to_treeview() # Jeśli pole puste, załaduj wszystko
            return

        search_results = database.search_sprzet(query)
        if not search_results:
            messagebox.showinfo("Brak wyników", f"Nie znaleziono sprzętu pasującego do '{query}'.")
            self.load_sprzet_to_treeview() # Możesz tu zdecydować, czy wyczyścić czy pokazać wszystko
            return

        for item in search_results:
            # Konwertujemy sqlite3.Row na słownik, a następnie pobieramy wartości w ustalonej kolejności
            item_dict = dict(item) 

            self.tree.insert("", "end", values=(
                item_dict['id'],
                item_dict['nazwa_sprzetu'],
                item_dict['marka_model'],
                item_dict['numer_seryjny'],
                item_dict['opis_usterki'],
                item_dict['nazwisko_klienta'],
                item_dict['telefon_klienta'],
                item_dict['data_przyjecia'], # Upewnij się, że to jest dokładnie ten klucz
                item_dict['data_wydania'],
                item_dict['status'],
                item_dict['koszt_naprawy'],
                item_dict['uwagi']
            ))


if __name__ == "__main__":
    root = tk.Tk()
    app = ServiceApp(root)
    root.mainloop()