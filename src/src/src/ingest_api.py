import requests

def fetch_fx_rates(base_url: str, base_currency: str) -> dict:
    # e.g., https://api.exchangerate.host/latest?base=USD
    resp = requests.get(base_url, params={"base": base_currency}, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Returns {"rates": {...}, "base": "USD", "date": "..."}
    return data
