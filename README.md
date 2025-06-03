Aplikacja do Zarządzania Serwisem Sprzętu

Aplikacja desktopowa w Pythonie z wykorzystaniem biblioteki Tkinter, służąca do zarządzania przyjęciami i wydaniami sprzętu w serwisie. Umożliwia dodawanie, edytowanie, usuwanie i wyszukiwanie wpisów dotyczących sprzętu.
Spis Treści

    Wymagania
    Instalacja
    Uruchamianie Aplikacji
    Funkcjonalności
    Struktura Projektu
    Baza Danych

Wymagania

Do uruchomienia aplikacji potrzebujesz zainstalowanego Pythona w wersji 3.x.
Instalacja

    Sklonuj repozytorium (lub pobierz pliki):
    Bash

git clone https://github.com/wronlol/ServiceAppPython.git

Przejdź do katalogu projektu:
Bash

    cd ServiceAppPython

    Zainstaluj wymagane biblioteki: Aplikacja korzysta głównie ze standardowych modułów Pythona (Tkinter, sqlite3, datetime), więc zazwyczaj nie wymaga dodatkowych instalacji przez pip.

Uruchamianie Aplikacji

Aby uruchomić aplikację, po prostu wykonaj plik main_app.py:
Bash

python main_app.py

Funkcjonalności

Aplikacja oferuje następujące możliwości:

    Dodawanie nowego sprzętu: Wprowadź szczegóły dotyczące sprzętu (nazwa, marka/model, numer seryjny, opis usterki, dane klienta, daty, status, uwagi).
    Edycja istniejącego sprzętu: Wybierz wpis z tabeli, aby załadować jego dane do formularza, a następnie zaktualizuj je.
    Usuwanie sprzętu: Wybierz wpis z tabeli i usuń go.
    Wyszukiwanie: Szukaj sprzętu po różnych kryteriach (nazwa, marka/model, numer seryjny, opis usterki, nazwisko klienta, numer telefonu, status, daty).
    Sortowanie tabeli: Kliknij w nagłówek dowolnej kolumny, aby posortować dane rosnąco/malejąco.
    Status naprawy: Status sprzętu można ustawić jako "Przyjęty" lub "Wydany".

Struktura Projektu

    main_app.py: Główny plik aplikacji zawierający interfejs użytkownika (Tkinter) i logikę działania.
    database.py: Moduł odpowiedzialny za interakcję z bazą danych SQLite. Zawiera funkcje do tworzenia tabel, dodawania, pobierania, aktualizowania i usuwania danych sprzętu.

Baza Danych

Aplikacja używa lekkiej bazy danych SQLite, przechowywanej w pliku serwis_sprzetu.db w katalogu głównym projektu.

    Tabela sprzet: Przechowuje wszystkie informacje o każdym przyjętym urządzeniu.

Ważne: Przy pierwszym uruchomieniu lub po poważniejszych zmianach w strukturze bazy danych (np. dodaniu/usunięciu kolumn), może być konieczne usunięcie pliku serwis_sprzetu.db w celu odbudowania bazy od podstaw.
