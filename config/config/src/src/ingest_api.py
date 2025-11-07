import requests

def fetch_fx_rates(base_url: str, base_currency: str) -> dict:
    """Fetch latest FX rates with the given base currency (e.g., USD)."""
    resp = requests.get(base_url, params={"base": base_currency}, timeout=30)
    resp.raise_for_status()
    js = resp.json()
    # Expected keys: "base", "date", "rates": {CUR: rate_per_base}
    return js
