import sqlite3
from datetime import datetime

# Nazwa pliku bazy danych. Będzie on stworzony w tym samym katalogu co skrypt.
DATABASE_NAME = "serwis_sprzetu.db"



def connect_db():
    """Nawiązuje połączenie z bazą danych."""
    conn = sqlite3.connect(DATABASE_NAME)
    # Ustawia row_factory, aby zwracać wiersze jako obiekty, do których można się odwoływać po nazwie kolumny.
    conn.row_factory = sqlite3.Row 
    return conn

def create_table():
    """Tworzy tabelę 'sprzet' w bazie danych, jeśli jeszcze nie istnieje."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sprzet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nazwa_sprzetu TEXT NOT NULL,
            marka_model TEXT,
            numer_seryjny TEXT,
            opis_usterki TEXT,
            nazwisko_klienta TEXT NOT NULL,
            telefon_klienta TEXT,
            data_przyjecia TEXT,
            data_wydania TEXT,
            status TEXT,
            koszt_naprawy REAL,
            uwagi TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Baza danych i tabela 'sprzet' zostały zainicjalizowane w {DATABASE_NAME}.")

def add_sprzet(data):
    """
    Dodaje nowy wpis sprzętu do bazy danych.
    :param data: Słownik zawierający dane sprzętu.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Konwertujemy słownik na krotkę wartości, zgodnie z kolejnością kolumn.
        # Sprawdzamy, czy wszystkie klucze istnieją, jeśli nie, używamy None/domyślnej wartości.
        values = (
            data.get('nazwa_sprzetu'),
            data.get('marka_model'),
            data.get('numer_seryjny'),
            data.get('opis_usterki'),
            data.get('nazwisko_klienta'),
            data.get('telefon_klienta'),
            data.get('data_przyjecia', datetime.now().strftime("%Y-%m-%d")), # Domyślnie dzisiejsza data
            data.get('data_wydania', ''), # Domyślnie puste
            data.get('status', 'Przyjęty'), # Domyślny status
            data.get('koszt_naprawy', 0.0),
            data.get('uwagi', '')
        )
        cursor.execute('''
            INSERT INTO sprzet (
                nazwa_sprzetu, marka_model, numer_seryjny, opis_usterki, 
                nazwisko_klienta, telefon_klienta, data_przyjecia, 
                data_wydania, status, koszt_naprawy, uwagi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', values)
        conn.commit()
        return "Sukces: Sprzęt dodany pomyślnie."
    except sqlite3.IntegrityError:
        return "Błąd: Sprzęt o podanym numerze seryjnym już istnieje."
    except Exception as e:
        return f"Błąd: Wystąpił błąd podczas dodawania sprzętu: {e}"
    finally:
        conn.close()

def update_sprzet(sprzet_id, data):
    """
    Aktualizuje istniejący wpis sprzętu w bazie danych.
    :param sprzet_id: ID sprzętu do aktualizacji.
    :param data: Słownik zawierający nowe dane sprzętu.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        # Tworzymy listę par kolumna=wartość do zapytania UPDATE
        set_clause = ", ".join([f"{key}=?" for key in data.keys()])
        values = tuple(data.values()) + (sprzet_id,) # Dodajemy ID na koniec dla klauzuli WHERE

        cursor.execute(f'''
            UPDATE sprzet
            SET {set_clause}
            WHERE id = ?
        ''', values)
        conn.commit()
        if cursor.rowcount > 0:
            return "Sukces: Sprzęt zaktualizowany pomyślnie."
        else:
            return "Błąd: Nie znaleziono sprzętu o podanym ID."
    except Exception as e:
        return f"Błąd: Wystąpił błąd podczas aktualizacji sprzętu: {e}"
    finally:
        conn.close()

def delete_sprzet(sprzet_id):
    """
    Usuwa wpis sprzętu z bazy danych.
    :param sprzet_id: ID sprzętu do usunięcia.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM sprzet WHERE id = ?", (sprzet_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return "Sukces: Sprzęt usunięty pomyślnie."
        else:
            return "Błąd: Nie znaleziono sprzętu o podanym ID."
    except Exception as e:
        return f"Błąd: Wystąpił błąd podczas usuwania sprzętu: {e}"
    finally:
        conn.close()

def get_all_sprzet():
    """Pobiera wszystkie wpisy sprzętu z bazy danych."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sprzet ORDER BY data_przyjecia DESC")
    data = cursor.fetchall()
    conn.close()
    return data # Zwraca listę obiektów Row (można traktować jak słowniki)

def search_sprzet(query):
    """
    Wyszukuje sprzęt na podstawie zapytania w różnych kolumnach, w tym po datach.
    :param query: Tekst wyszukiwania.
    """
    conn = connect_db()
    cursor = conn.cursor()
    search_query = f"%{query}%"
    
    # Rozszerzamy zapytanie WHERE o pola daty
    cursor.execute('''
        SELECT * FROM sprzet WHERE 
        nazwa_sprzetu LIKE ? OR 
        marka_model LIKE ? OR 
        numer_seryjny LIKE ? OR
        opis_usterki LIKE ? OR               
        nazwisko_klienta LIKE ? OR
        telefon_klienta LIKE ? OR            
        status LIKE ? OR
        data_przyjecia LIKE ? OR           -- DODANO datę przyjęcia
        data_wydania LIKE ?                -- DODANO datę wydania
        ORDER BY data_przyjecia DESC
    ''', (search_query, search_query, search_query, search_query, search_query, search_query, search_query, 
          search_query, search_query)) # !!! Musi być 9 'search_query' teraz !!!
    
    data = cursor.fetchall()
    conn.close()
    print(f"Dane z search_sprzet('{query}'): {[dict(row) for row in data]}")
    return data


# Jeśli uruchamiasz ten plik bezpośrednio, stworzy bazę danych i tabelę
if __name__ == "__main__":
    create_table()
    # Możesz dodać tutaj testowe dane, jeśli chcesz
    # add_sprzet({
    #     'nazwa_sprzetu': 'Laptop',
    #     'marka_model': 'HP EliteBook',
    #     'numer_seryjny': 'SN123456789',
    #     'opis_usterki': 'Nie ładuje baterii',
    #     'nazwisko_klienta': 'Jan Kowalski',
    #     'telefon_klienta': '123-456-789',
    #     'data_przyjecia': '2025-06-01',
    #     'status': 'W diagnostyce'
    # })
    # all_sprzet = get_all_sprzet()
    # for s in all_sprzet:
    #     print(dict(s)) # Konwertujemy Row na słownik dla łatwiejszego wyświetlania