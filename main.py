import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://sl-fuel-price-api.onrender.com",  # Your API domain
        "https://*.vercel.app",  # Vercel deployment domains
        "https://*.vercel.com",
        "https://relaxed-gingersnap-4787a1.netlify.app" ,  # Vercel deployment domains
        # Add other domains as needed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
