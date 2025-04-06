import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/fuel-prices")
def get_fuel_prices():
    url = "https://ceypetco.gov.lk/marketing-sales/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    cards = soup.select('div.cards-container div.card')
    prices = []

    for card in cards:
        title = card.find('h2').get_text(strip=True)
        price_line = card.find('p').get_text(strip=True)
        price = price_line.split(':')[-1].strip()
        effect_date = card.find_all('p')[1].get_text(strip=True)

        prices.append({
            'fuel_type': title,
            'price_per_litre': price,
            'effective_date': effect_date
        })

    return {"fuel_prices": prices}
