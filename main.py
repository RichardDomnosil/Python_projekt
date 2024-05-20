import requests
import json
from currency_manager import CurrencyManager

# Váš API klíč
API_KEY = "tFjbl4CFFjIyMobFM3TPYdwsc6n4DGcX"

def get_exchange_rate(api_key, base_currency, target_currency):
    url = "https://api.currencybeacon.com/v1/latest"
    params = {
        'api_key': api_key,
        'base': base_currency,
        'symbols': target_currency
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Ladící výpisy pro kontrolu odpovědi
    print("Odpověď JSON:", data)
    
    # Kontrola kódu odpovědi
    if data['meta']['code'] == 200:
        rates = data['response']['rates']
        rate = rates.get(target_currency)
        if rate is not None:
            return rate
        else:
            raise Exception(f"Kurz pro měnu {target_currency} nebyl nalezen v odpovědi.")
    else:
        raise Exception("Selhalo získání směnného kurzu: " + data.get('meta', {}).get('error', 'Neznámá chyba'))

def convert_currency(api_key, amount, base_currency, target_currency):
    rate = get_exchange_rate(api_key, base_currency, target_currency)
    converted_amount = amount * rate
    return converted_amount

def main():
    manager = CurrencyManager()
    print("Vítejte v převaděči měn!")

    while True:
        print("\nMenu:")
        print("1. Převést měnu")
        print("2. Přidat novou měnu")
        print("3. Zobrazit dostupné měny")
        print("4. Ukončit program")
        volba = input("Vyberte možnost: ")

        if volba == '1':
            zakladni_mena = input("Zadejte základní měnu (např. USD): ").upper()
            cilova_mena = input("Zadejte cílovou měnu (např. EUR): ").upper()
            castka = float(input("Zadejte částku k převodu: "))

            try:
                prevedena_castka = convert_currency(API_KEY, castka, zakladni_mena, cilova_mena)
                print(f"{castka} {zakladni_mena} je {prevedena_castka:.2f} {cilova_mena}")
            except Exception as e:
                print("Chyba:", str(e))

        elif volba == '2':
            nova_mena = input("Zadejte kód nové měny k přidání (např. GBP): ").upper()
            manager.add_currency(nova_mena)

        elif volba == '3':
            manager.display_currencies()

        elif volba == '4':
            print("Ukončení programu.")
            break

        else:
            print("Neplatná volba. Zkuste to prosím znovu.")

if __name__ == "__main__":
    main()
