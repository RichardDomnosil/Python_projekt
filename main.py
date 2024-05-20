import requests


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
    
    
    # print("Response JSON:", data)
    
   
    if data['meta']['code'] == 200:
        rates = data['response']['rates']
        rate = rates.get(target_currency)
        if rate is not None:
            return rate
        else:
            raise Exception(f"Rate for {target_currency} not found in the response.")
    else:
        raise Exception("Failed to retrieve exchange rate: " + data.get('meta', {}).get('error', 'Unknown error'))

def convert_currency(api_key, amount, base_currency, target_currency):
    rate = get_exchange_rate(api_key, base_currency, target_currency)
    converted_amount = amount * rate
    return converted_amount

def main():
    print("Vítejte ve virtuální směnárně!")

    base_currency = input("Zadejte počáteční měnu (p.ř., USD): ").upper()
    target_currency = input("Zadejte koncovou měnu (p.ř., EUR): ").upper()
    amount = float(input("Zadejte kolik chvete převést: "))

    try:
        converted_amount = convert_currency(API_KEY, amount, base_currency, target_currency)
        print(f"{amount} {base_currency} is {converted_amount:.2f} {target_currency}")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
