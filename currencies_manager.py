import json  # Importuje modul json pro práci s JSON soubory
import os  # Importuje modul os pro práci se souborovými cestami
from tkinter import messagebox  # Importuje messagebox pro zobrazení dialogových oken v Tkinteru

class CurrencyManager:
    def __init__(self, filename='currencies.json'):
        """
        Inicializuje CurrencyManager.

        Vstupy:
        - filename: Název souboru, kde jsou uloženy měny (defaultně 'currencies.json').

        Výstupy:
        - Inicializuje seznam měn načtením ze souboru.
        """
        self.filename = filename  # Nastaví název souboru
        self.file_path = os.path.join(os.path.dirname(__file__), filename)  # Vytvoří cestu k souboru

        # Načtení měn ze souboru
        self.currencies = self.load_currencies()  # Načte seznam měn ze souboru

    def load_currencies(self):
        """
        Načte měny ze souboru.

        Vstupy:
        - Žádné.

        Výstupy:
        - Vrací seznam měn načtených ze souboru nebo prázdný seznam, pokud soubor neexistuje.
        """
        if os.path.exists(self.file_path):  # Kontroluje, zda soubor existuje
            with open(self.file_path, 'r') as file:  # Otevře soubor pro čtení
                return json.load(file)  # Načte a vrátí seznam měn ze souboru
        return []  # Pokud soubor neexistuje, vrátí prázdný seznam

    def save_currencies(self):
        """
        Uloží aktuální seznam měn do souboru.

        Vstupy:
        - Žádné.

        Výstupy:
        - Žádné.
        """
        with open(self.file_path, 'w') as file:  # Otevře soubor pro zápis
            json.dump(self.currencies, file, indent=4)  # Uloží seznam měn do souboru

    def add_currency(self, currency_code):
        """
        Přidá novou měnu do seznamu.

        Vstupy:
        - currency_code: Třípísmenný kód nové měny (např. 'GBP').

        Výstupy:
        - Zobrazí dialogové okno s informací o úspěchu nebo chybě.
        """
        currency_code = currency_code.upper()  # Převede kód měny na velká písmena
        if not currency_code.isalpha() or len(currency_code) != 3:  # Kontroluje, zda je kód měny platný
            messagebox.showerror("Chyba", "Zadejte platný třípísmenný kód měny.")  # Zobrazí chybovou zprávu
            return

        if currency_code not in self.currencies:  # Kontroluje, zda měna není již v seznamu
            self.currencies.append(currency_code)  # Přidá novou měnu do seznamu
            self.save_currencies()  # Uloží aktualizovaný seznam měn do souboru
            messagebox.showinfo("Úspěch", f"Měna {currency_code} byla úspěšně přidána.")  # Zobrazí úspěšnou zprávu
        else:
            messagebox.showinfo("Chyba", f"Měna {currency_code} už existuje.")  # Zobrazí zprávu o duplicitní měně

    def display_currencies(self):
        """
        Zobrazí seznam dostupných měn v dialogovém okně.

        Vstupy:
        - Žádné.

        Výstupy:
        - Zobrazí dialogové okno s dostupnými měnami.
        """
        currencies_str = ", ".join(self.currencies)  # Vytvoří řetězec z dostupných měn
        messagebox.showinfo("Dostupné měny", currencies_str)  # Zobrazí dialogové okno s dostupnými měnami
