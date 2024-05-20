import json
import os

class CurrencyManager:
    def __init__(self, filename='currencies.json'):
        self.filename = filename
        self.file_path = os.path.join(os.path.dirname(__file__), filename)

        self.currencies = self.load_currencies()

    def load_currencies(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return json.load(file)
        return []

    def save_currencies(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.currencies, file, indent=4)

    def add_currency(self, currency_code):
        currency_code = currency_code.upper()
        if currency_code not in self.currencies:
            self.currencies.append(currency_code)
            self.save_currencies()
            print(f"Měna {currency_code} byla úspěšně přidána.")
        else:
            print(f"Měna {currency_code} už existuje.")

    def display_currencies(self):
        print("Dostupné měny:", ", ".join(self.currencies))
