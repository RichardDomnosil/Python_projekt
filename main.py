import tkinter as tk  # Importuje Tkinter pro GUI
from tkinter import messagebox, simpledialog  # Importuje messagebox a simpledialog pro dialogová okna
import requests  # Importuje requests pro HTTP požadavky
from currencies_manager import CurrencyManager  # Importuje CurrencyManager

API_KEY = "tFjbl4CFFjIyMobFM3TPYdwsc6n4DGcX"  # API klíč pro přístup k API pro směnné kurzy

class CurrencyConverterApp:
    def __init__(self, root):
        """
        Inicializuje CurrencyConverterApp.

        Vstupy:
        - root: Hlavní okno Tkinteru.

        Výstupy:
        - Inicializuje GUI a potřebné instance.
        """
        self.root = root  # Nastaví hlavní okno
        self.root.title("Převaděč měn")  # Nastaví název hlavního okna
        self.converter = CurrencyConverter(API_KEY)  # Inicializuje CurrencyConverter s API klíčem
        self.currency_manager = CurrencyManager()  # Inicializuje CurrencyManager

        self.create_widgets()  # Vytvoří GUI prvky

    def create_widgets(self):
        """
        Vytvoří a rozmístí GUI prvky.

        Vstupy:
        - Žádné.

        Výstupy:
        - Žádné.
        """
        self.title_label = tk.Label(self.root, text="Převaděč měn", font=("Helvetica", 18))  # Vytvoří nadpis
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)  # Umístí nadpis

        self.base_currency_label = tk.Label(self.root, text="Základní měna:")  # Vytvoří popisek pro základní měnu
        self.base_currency_label.grid(row=1, column=0, padx=10, pady=5)  # Umístí popisek pro základní měnu
        self.base_currency_entry = tk.Entry(self.root)  # Vytvoří vstupní pole pro základní měnu
        self.base_currency_entry.grid(row=1, column=1, padx=10, pady=5)  # Umístí vstupní pole pro základní měnu

        self.target_currency_label = tk.Label(self.root, text="Cílová měna:")  # Vytvoří popisek pro cílovou měnu
        self.target_currency_label.grid(row=2, column=0, padx=10, pady=5)  # Umístí popisek pro cílovou měnu
        self.target_currency_entry = tk.Entry(self.root)  # Vytvoří vstupní pole pro cílovou měnu
        self.target_currency_entry.grid(row=2, column=1, padx=10, pady=5)  # Umístí vstupní pole pro cílovou měnu

        self.amount_label = tk.Label(self.root, text="Částka:")  # Vytvoří popisek pro částku
        self.amount_label.grid(row=3, column=0, padx=10, pady=5)  # Umístí popisek pro částku
        self.amount_entry = tk.Entry(self.root)  # Vytvoří vstupní pole pro částku
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5)  # Umístí vstupní pole pro částku

        self.convert_button = tk.Button(self.root, text="Převést", command=self.convert_currency)  # Vytvoří tlačítko pro převod
        self.convert_button.grid(row=4, column=0, columnspan=2, pady=10)  # Umístí tlačítko pro převod

        self.result_label = tk.Label(self.root, text="")  # Vytvoří štítek pro zobrazení výsledku
        self.result_label.grid(row=5, column=0, columnspan=2, pady=5)  # Umístí štítek pro zobrazení výsledku

        self.add_currency_button = tk.Button(self.root, text="Přidat měnu", command=self.add_currency)  # Vytvoří tlačítko pro přidání měny
        self.add_currency_button.grid(row=6, column=0, columnspan=2, pady=5)  # Umístí tlačítko pro přidání měny

        self.display_currencies_button = tk.Button(self.root, text="Zobrazit měny", command=self.display_currencies)  # Vytvoří tlačítko pro zobrazení měn
        self.display_currencies_button.grid(row=7, column=0, columnspan=2, pady=5)  # Umístí tlačítko pro zobrazení měn

    def convert_currency(self):
        """
        Provede převod měny.

        Vstupy:
        - base_currency: Třípísmenný kód základní měny.
        - target_currency: Třípísmenný kód cílové měny.
        - amount: Částka k převodu.

        Výstupy:
        - Zobrazí výsledek převodu nebo chybovou zprávu.
        """
        base_currency = self.base_currency_entry.get().upper()  # Získá a převede kód základní měny na velká písmena
        target_currency = self.target_currency_entry.get().upper()  # Získá a převede kód cílové měny na velká písmena
        amount = self.amount_entry.get()  # Získá částku k převodu

        if not base_currency.isalpha() or len(base_currency) != 3:  # Kontroluje platnost kódu základní měny
            messagebox.showerror("Chyba", "Zadejte platný třípísmenný kód základní měny.")  # Zobrazí chybovou zprávu
            return
        if not target_currency.isalpha() or len(target_currency) != 3:  # Kontroluje platnost kódu cílové měny
            messagebox.showerror("Chyba", "Zadejte platný třípísmenný kód cílové měny.")  # Zobrazí chybovou zprávu
            return
        if base_currency not in self.currency_manager.currencies:  # Kontroluje, zda je základní měna dostupná
            messagebox.showerror("Chyba", f"Základní měna {base_currency} není dostupná.")  # Zobrazí chybovou zprávu
            return
        if target_currency not in self.currency_manager.currencies:  # Kontroluje, zda je cílová měna dostupná
            messagebox.showerror("Chyba", f"Cílová měna {target_currency} není dostupná.")  # Zobrazí chybovou zprávu
            return

        try:
            amount = float(amount)  # Převede částku na float
            converted_amount = self.converter.convert(amount, base_currency, target_currency)  # Provede převod měny
            self.result_label.config(text=f"{amount} {base_currency} je {converted_amount:.2f} {target_currency}")  # Zobrazí výsledek převodu
        except ValueError:
            messagebox.showerror("Chyba", "Prosím zadejte platnou částku.")  # Zobrazí chybovou zprávu pro neplatnou částku
        except Exception as e:
            messagebox.showerror("Chyba", str(e))  # Zobrazí chybovou zprávu pro jiné chyby

    def add_currency(self):
        """
        Přidá novou měnu.

        Vstupy:
        - Žádné.

        Výstupy:
        - Zobrazí dialogové okno pro zadání kódu měny a poté informaci o úspěchu nebo chybě.
        """
        new_currency = simpledialog.askstring("Přidat měnu", "Zadejte kód nové měny (např. GBP):")  # Zobrazí dialogové okno pro zadání nové měny
        if new_currency:
            new_currency = new_currency.upper()  # Převede kód nové měny na velká písmena
            try:
                self.currency_manager.add_currency(new_currency)  # Přidá novou měnu pomocí CurrencyManager
            except Exception as e:
                messagebox.showerror("Chyba", str(e))  # Zobrazí chybovou zprávu pro případ chyby

    def display_currencies(self):
        """
        Zobrazí seznam dostupných měn.

        Vstupy:
        - Žádné.

        Výstupy:
        - Zobrazí dialogové okno s dostupnými měnami.
        """
        self.currency_manager.display_currencies()  # Zobrazí dostupné měny pomocí CurrencyManager

class CurrencyConverter:
    def __init__(self, api_key):
        """
        Inicializuje CurrencyConverter.

        Vstupy:
        - api_key: API klíč pro přístup k API pro směnné kurzy.

        Výstupy:
        - Inicializuje CurrencyConverter s daným API klíčem.
        """
        self.api_key = api_key  # Nastaví API klíč
        self.api_url = "https://api.currencybeacon.com/v1/latest"  # Nastaví URL API pro směnné kurzy

    def get_exchange_rate(self, base_currency, target_currency):
        """
        Získá směnný kurz mezi dvěma měnami.

        Vstupy:
        - base_currency: Třípísmenný kód základní měny.
        - target_currency: Třípísmenný kód cílové měny.

        Výstupy:
        - Vrací směnný kurz mezi základní a cílovou měnou nebo vyvolá výjimku v případě chyby.
        """
        params = {
            'api_key': self.api_key,  # API klíč pro ověření
            'base': base_currency,  # Základní měna
            'symbols': target_currency  # Cílová měna
        }
        response = requests.get(self.api_url, params=params)  # Odešle HTTP GET požadavek na API
        data = response.json()  # Získá data v JSON formátu z odpovědi

        if data['meta']['code'] == 200:  # Kontroluje, zda je odpověď úspěšná
            rates = data['response']['rates']  # Získá směnné kurzy z odpovědi
            rate = rates.get(target_currency)  # Získá směnný kurz pro cílovou měnu
            if rate is not None:
                return rate  # Vrací směnný kurz
            else:
                raise Exception(f"Kurz pro měnu {target_currency} nebyl nalezen v odpovědi.")  # Vyvolá výjimku, pokud směnný kurz není nalezen
        else:
            raise Exception("Selhalo získání směnného kurzu: " + data.get('meta', {}).get('error', 'Neznámá chyba'))  # Vyvolá výjimku, pokud požadavek selže

    def convert(self, amount, base_currency, target_currency):
        """
        Provede převod částky mezi dvěma měnami.

        Vstupy:
        - amount: Částka k převodu.
        - base_currency: Třípísmenný kód základní měny.
        - target_currency: Třípísmenný kód cílové měny.

        Výstupy:
        - Vrací převedenou částku.
        """
        rate = self.get_exchange_rate(base_currency, target_currency)  # Získá směnný kurz mezi měnami
        converted_amount = amount * rate  # Provede převod částky
        return converted_amount  # Vrací převedenou částku

    def add_currency(self, new_currency):
        raise NotImplementedError("Tato funkce není implementována v tomto zadání.")  # Metoda není implementována

    def get_available_currencies(self):
        raise NotImplementedError("Tato funkce není implementována v tomto zadání.")  # Metoda není implementována

if __name__ == "__main__":
    root = tk.Tk()  # Vytvoří hlavní okno Tkinteru
    app = CurrencyConverterApp(root)  # Inicializuje aplikaci
    root.mainloop()  # Spustí hlavní smyčku Tkinteru
