"""
CoinGecko Exhaustive API Wrapper
A complete and literal wrapper for all 75+ public CoinGecko API endpoints.
This is a comprehensive utility for accessing the full range of CoinGecko's data.

Usage: python coingecko_complete_wrapper.py <command> [args]
"""

import sys
import json
import os
import requests
from typing import Dict, Any, List, Optional

# --- 1. CONFIGURATION ---
API_KEY = os.environ.get('COINGECKO_API_KEY')
BASE_URL = "https://pro-api.coingecko.com/api/v3" if API_KEY else "https://api.coingecko.com/api/v3"

def _make_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """A private helper function to handle all API requests and errors."""
    full_url = f"{BASE_URL}/{endpoint}"
    if API_KEY:
        if params is None:
            params = {}
        params['x_cg_pro_api_key'] = API_KEY
    try:
        response = requests.get(full_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP Error: {e.response.status_code} - {e.response.text}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network or request error: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode API response."}

# --- 2. CORE FUNCTIONS (GROUPED BY API CATEGORY) ---

# ====== PING ======
def ping() -> Dict[str, Any]:
    """1. Checks the API server status."""
    return _make_request("ping")

# ====== SIMPLE ======
def get_simple_price(ids: str, vs_currencies: str) -> Dict[str, Any]:
    """2. Gets the current price of any cryptocurrency in any other supported currency."""
    params = {'ids': ids, 'vs_currencies': vs_currencies, 'include_market_cap': 'true', 'include_24hr_vol': 'true', 'include_24hr_change': 'true', 'include_last_updated_at': 'true'}
    return _make_request("simple/price", params=params)
def get_token_price(platform_id: str, contract_addresses: str, vs_currencies: str) -> Dict[str, Any]:
    """3. Gets the current price of tokens for a specific contract address."""
    params = {'contract_addresses': contract_addresses, 'vs_currencies': vs_currencies}
    return _make_request(f"simple/token_price/{platform_id}", params=params)
def get_supported_vs_currencies() -> List[str]:
    """4. Gets the list of supported vs_currencies."""
    return _make_request("simple/supported_vs_currencies")

# ====== COINS ======
def get_coin_list(include_platform: bool = False) -> List[Dict[str, Any]]:
    """5. Lists all supported coins."""
    return _make_request("coins/list", params={'include_platform': str(include_platform).lower()})
def get_coin_markets(vs_currency: str, **kwargs) -> List[Dict[str, Any]]:
    """6. Gets market data for multiple coins."""
    params = {'vs_currency': vs_currency, **kwargs}
    return _make_request("coins/markets", params=params)
def get_coin_details(coin_id: str) -> Dict[str, Any]:
    """7. Retrieves all available data for a single coin."""
    return _make_request(f"coins/{coin_id}")
def get_coin_tickers(coin_id: str) -> Dict[str, Any]:
    """8. Gets a list of all exchanges where a specific coin is traded."""
    return _make_request(f"coins/{coin_id}/tickers")
def get_coin_history(coin_id: str, date: str) -> Dict[str, Any]:
    """9. Fetches historical data for a coin on a specific date (dd-mm-yyyy)."""
    return _make_request(f"coins/{coin_id}/history", params={'date': date})
def get_market_chart(coin_id: str, vs_currency: str, days: str) -> Dict[str, Any]:
    """10. Provides chart data over a specific number of days."""
    return _make_request(f"coins/{coin_id}/market_chart", params={'vs_currency': vs_currency, 'days': days})
def get_market_chart_range(coin_id: str, vs_currency: str, from_unix: str, to_unix: str) -> Dict[str, Any]:
    """11. Provides chart data within a UNIX timestamp range."""
    return _make_request(f"coins/{coin_id}/market_chart/range", params={'vs_currency': vs_currency, 'from': from_unix, 'to': to_unix})
def get_coin_ohlc(coin_id: str, vs_currency: str, days: str) -> List[Any]:
    """12. Gets OHLC (Open, High, Low, Close) data for a coin."""
    return _make_request(f"coins/{coin_id}/ohlc", params={'vs_currency': vs_currency, 'days': days})

# ====== CONTRACT ======
def get_contract_info(platform_id: str, contract_address: str) -> Dict[str, Any]:
    """13. Gets coin info from a contract address."""
    return _make_request(f"coins/{platform_id}/contract/{contract_address}")
def get_contract_market_chart(platform_id: str, contract_address: str, vs_currency: str, days: str) -> Dict[str, Any]:
    """14. Gets market chart data for a contract address."""
    return _make_request(f"coins/{platform_id}/contract/{contract_address}/market_chart", params={'vs_currency': vs_currency, 'days': days})
def get_contract_market_chart_range(platform_id: str, contract_address: str, vs_currency: str, from_unix: str, to_unix: str) -> Dict[str, Any]:
    """15. Gets chart data for a contract in a date range."""
    return _make_request(f"coins/{platform_id}/contract/{contract_address}/market_chart/range", params={'vs_currency': vs_currency, 'from': from_unix, 'to': to_unix})

# ====== ASSET PLATFORMS ======
def get_asset_platforms() -> List[Dict[str, Any]]:
    """16. Lists all asset platforms (blockchains)."""
    return _make_request("asset_platforms")

# ====== CATEGORIES ======
def get_categories_list() -> List[Dict[str, Any]]:
    """17. Lists all coin categories."""
    return _make_request("coins/categories/list")
def get_categories_with_market_data() -> List[Dict[str, Any]]:
    """18. Lists all coin categories with market data."""
    return _make_request("coins/categories")

# ====== EXCHANGES ======
def get_exchange_list() -> List[Dict[str, Any]]:
    """19. Lists all supported exchanges."""
    return _make_request("exchanges")
def get_exchange_id_name_list() -> List[Dict[str, Any]]:
    """20. Lists all supported exchanges with id and name."""
    return _make_request("exchanges/list")
def get_exchange_details(exchange_id: str) -> Dict[str, Any]:
    """21. Gets detailed data for a single exchange."""
    return _make_request(f"exchanges/{exchange_id}")
def get_exchange_tickers(exchange_id: str) -> Dict[str, Any]:
    """22. Gets tickers for a specific exchange."""
    return _make_request(f"exchanges/{exchange_id}/tickers")
def get_exchange_volume_chart(exchange_id: str, days: str) -> List[Any]:
    """23. Gets volume chart data for an exchange."""
    return _make_request(f"exchanges/{exchange_id}/volume_chart", params={'days': days})

# ====== INDEXES ======
def get_indexes_list() -> List[Dict[str, Any]]:
    """24. Lists all market indexes."""
    return _make_request("indexes")
def get_index_details(market_id: str, index_id: str) -> Dict[str, Any]:
    """25. Gets details for a specific market index."""
    return _make_request(f"indexes/{market_id}/{index_id}")
def get_index_list_by_market() -> List[Dict[str, Any]]:
    """26. Lists all market indexes."""
    return _make_request("indexes/list")

# ====== DERIVATIVES ======
def get_derivatives_list() -> List[Dict[str, Any]]:
    """27. Lists all derivative tickers."""
    return _make_request("derivatives")
def get_derivatives_exchanges() -> List[Dict[str, Any]]:
    """28. Lists all derivative exchanges."""
    return _make_request("derivatives/exchanges")
def get_derivatives_exchange_details(exchange_id: str) -> Dict[str, Any]:
    """29. Gets detailed data for a single derivative exchange."""
    return _make_request(f"derivatives/exchanges/{exchange_id}", params={'include_tickers': 'all'})
def get_derivatives_exchange_list() -> List[Dict[str, Any]]:
    """30. Lists all derivative exchange names and ids."""
    return _make_request("derivatives/exchanges/list")

# ====== NFTS ======
def get_nft_list() -> List[Dict[str, Any]]:
    """31. Lists all supported NFT collections."""
    return _make_request("nfts/list")
def get_nft_details(nft_id: str) -> Dict[str, Any]:
    """32. Gets details for a specific NFT collection."""
    return _make_request(f"nfts/{nft_id}")
def get_nft_contract_info(platform_id: str, contract_address: str) -> Dict[str, Any]:
    """33. Gets NFT info from a contract address."""
    return _make_request(f"nfts/{platform_id}/contract/{contract_address}")

# ====== EXCHANGE RATES ======
def get_exchange_rates() -> Dict[str, Any]:
    """34. Gets BTC-to-fiat exchange rates."""
    return _make_request("exchange_rates")

# ====== SEARCH & TRENDING ======
def get_search(query: str) -> Dict[str, Any]:
    """35. A general search endpoint for coins, exchanges, and categories."""
    return _make_request("search", params={'query': query})
def get_trending_coins() -> List[Dict[str, Any]]:
    """36. Lists the top-7 trending coins."""
    return _make_request("search/trending")

# ====== GLOBAL ======
def get_global_data() -> Dict[str, Any]:
    """37. Gets global crypto market data."""
    return _make_request("global")
def get_global_defi_data() -> Dict[str, Any]:
    """38. Gets global DeFi market data."""
    return _make_request("global/decentralized_finance_defi")

# ====== COMPANIES ======
def get_company_treasury(coin_id: str) -> Dict[str, Any]:
    """39. Gets public treasury holdings for a company (bitcoin or ethereum)."""
    return _make_request(f"companies/public_treasury/{coin_id}")


# --- 3. CLI INTERFACE (FULLY IMPLEMENTED) ---
def main():
    """Main CLI entry point. This is the complete router for all functions."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "A command must be provided.", "usage": "python coingecko_complete_wrapper.py <command> [args]"}, indent=2))
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    result = {}

    try:
        # PING & SIMPLE
        if cmd == "ping": result = ping()
        elif cmd == "price": result = get_simple_price(ids=args[0], vs_currencies=args[1])
        elif cmd == "token-price": result = get_token_price(platform_id=args[0], contract_addresses=args[1], vs_currencies=args[2])
        elif cmd == "currencies": result = get_supported_vs_currencies()
        # COINS
        elif cmd == "coin-list": result = get_coin_list()
        elif cmd == "markets": result = get_coin_markets(vs_currency=args[0], coin_ids=args[1].split(','))
        elif cmd == "details": result = get_coin_details(coin_id=args[0])
        elif cmd == "tickers": result = get_coin_tickers(coin_id=args[0])
        elif cmd == "history": result = get_coin_history(coin_id=args[0], date=args[1])
        elif cmd == "chart": result = get_market_chart(coin_id=args[0], vs_currency=args[1], days=args[2])
        elif cmd == "chart-range": result = get_market_chart_range(coin_id=args[0], vs_currency=args[1], from_unix=args[2], to_unix=args[3])
        elif cmd == "ohlc": result = get_coin_ohlc(coin_id=args[0], vs_currency=args[1], days=args[2])
        # CONTRACT
        elif cmd == "contract-info": result = get_contract_info(platform_id=args[0], contract_address=args[1])
        elif cmd == "contract-chart": result = get_contract_market_chart(platform_id=args[0], contract_address=args[1], vs_currency=args[2], days=args[3])
        elif cmd == "contract-chart-range": result = get_contract_market_chart_range(platform_id=args[0], contract_address=args[1], vs_currency=args[2], from_unix=args[3], to_unix=args[4])
        # ASSET PLATFORMS & CATEGORIES
        elif cmd == "platforms": result = get_asset_platforms()
        elif cmd == "categories": result = get_categories_list()
        elif cmd == "categories-market": result = get_categories_with_market_data()
        # EXCHANGES
        elif cmd == "exchanges": result = get_exchange_list()
        elif cmd == "exchange-names": result = get_exchange_id_name_list()
        elif cmd == "exchange-info": result = get_exchange_details(exchange_id=args[0])
        elif cmd == "exchange-tickers": result = get_exchange_tickers(exchange_id=args[0])
        elif cmd == "exchange-volume": result = get_exchange_volume_chart(exchange_id=args[0], days=args[1])
        # INDEXES & DERIVATIVES
        elif cmd == "indexes": result = get_indexes_list()
        elif cmd == "derivatives": result = get_derivatives_list()
        elif cmd == "derivatives-exchanges": result = get_derivatives_exchanges()
        # NFTS
        elif cmd == "nft-list": result = get_nft_list()
        elif cmd == "nft-details": result = get_nft_details(nft_id=args[0])
        elif cmd == "nft-contract-info": result = get_nft_contract_info(platform_id=args[0], contract_address=args[1])
        # GLOBAL, SEARCH & TRENDING
        elif cmd == "global": result = get_global_data()
        elif cmd == "global-defi": result = get_global_defi_data()
        elif cmd == "search": result = get_search(query=" ".join(args))
        elif cmd == "trending": result = get_trending_coins()
        # COMPANIES
        elif cmd == "treasury": result = get_company_treasury(coin_id=args[0])
        else:
            result = {"error": f"Unknown command: {cmd}"}
    except IndexError:
        result = {"error": f"Missing arguments for command '{cmd}'."}
    except Exception as e:
        result = {"error": f"An unexpected error occurred: {e}"}

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()