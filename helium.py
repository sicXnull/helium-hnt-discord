import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

coingecko_api_key = "<api-key>"
hnt_address = "" #replace with hnt_address
iot_address = "" #replace with iot_address, if blank, will be skipped
mobile_address = "" #replace with mobile_address, if blank, will be skipped
webhook_url = "https://discord.com/api/webhooks/<embed>"
currency_code = "USD" 

currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "JPY": "¥",
    "GBP": "£",
    "CHF": "Fr.",
    "CAD": "C$",
    "AUD": "A$",
    "CNY": "¥",
    "INR": "₹",
}

def fetch_balance(address):
    if address:
        curl_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTokenAccountBalance",
            "params": [address]
        }

        url_solana = "https://api.mainnet-beta.solana.com"
        headers_solana = {"Content-Type": "application/json"}
        response = requests.post(url_solana, json=curl_data, headers=headers_solana)

        if response.status_code == 200:
            return response.json()
        else:
            return None
    else:
        return None

response_hnt = fetch_balance(hnt_address)
response_iot = fetch_balance(iot_address)
response_mobile = fetch_balance(mobile_address)

if (not hnt_address or response_hnt) and (not iot_address or response_iot) and (not mobile_address or response_mobile):
    uiAmountString_hnt = response_hnt["result"]["value"]["uiAmountString"] if response_hnt else ""
    uiAmountString_iot = response_iot["result"]["value"]["uiAmountString"] if response_iot else ""
    uiAmountString_mobile = response_mobile["result"]["value"]["uiAmountString"] if response_mobile else ""

    url_coingecko_hnt = "https://api.coingecko.com/api/v3/simple/price"
    params_coingecko_hnt = {
        "ids": "helium",
        "vs_currencies": currency_code,
        "x_cg_demo_api_key": coingecko_api_key
    }
    response_coingecko_hnt = requests.get(url_coingecko_hnt, params=params_coingecko_hnt)

    url_coingecko_iot = "https://api.coingecko.com/api/v3/simple/price"
    params_coingecko_iot = {
        "ids": "helium-iot",
        "vs_currencies": currency_code,
        "x_cg_demo_api_key": coingecko_api_key
    }
    response_coingecko_iot = requests.get(url_coingecko_iot, params=params_coingecko_iot)

    if response_coingecko_hnt.status_code == 200 and response_coingecko_iot.status_code == 200:
        response_json_coingecko_hnt = response_coingecko_hnt.json()
        response_json_coingecko_iot = response_coingecko_iot.json()

        usd_price_hnt = response_json_coingecko_hnt["helium"][currency_code.lower()]
        usd_price_iot = response_json_coingecko_iot["helium-iot"][currency_code.lower()]

        
        currency_symbol = currency_symbols.get(currency_code, "")

        if hnt_address:
            hnt_balance_currency = float(uiAmountString_hnt) * usd_price_hnt

        if iot_address:
            iot_balance_currency = float(uiAmountString_iot) * usd_price_iot

        if mobile_address:
            mobile_balance_currency = float(uiAmountString_mobile) * usd_price_hnt

        total_balance_currency = (hnt_balance_currency if hnt_address else 0) + (iot_balance_currency if iot_address else 0) + (mobile_balance_currency if mobile_address else 0)

        
        webhook = DiscordWebhook(url=webhook_url)

        
        embed = DiscordEmbed(title="HNT/IOT/Mobile Balance", color=0x00ff00)
        embed.set_thumbnail(url="https://cryptologos.cc/logos/helium-hnt-logo.png")

        if hnt_address:
            embed.add_embed_field(name=f"HNT Price", value=f"{currency_symbol} {usd_price_hnt:.2f}", inline=False)
            embed.add_embed_field(name="HNT Balance", value=f"{uiAmountString_hnt} HNT", inline=False)
            embed.add_embed_field(name=f"HNT Balance", value=f"{currency_symbol} {hnt_balance_currency:.2f}", inline=False)

        if iot_address:
            embed.add_embed_field(name="IOT Balance", value=f"{uiAmountString_iot} IOT", inline=False)
            embed.add_embed_field(name=f"IOT Balance", value=f"{currency_symbol} {iot_balance_currency:.2f}", inline=False)

        if mobile_address:
            embed.add_embed_field(name="Mobile Balance", value=f"{uiAmountString_mobile} Mobile", inline=False)
            embed.add_embed_field(name=f"Mobile Balance", value=f"{currency_symbol} {mobile_balance_currency:.2f}", inline=False)

        embed.add_embed_field(name=f"Total", value=f"{currency_symbol} {total_balance_currency:.2f}", inline=False)

        webhook.add_embed(embed)

        response = webhook.execute()

    else:
        print(f"Error fetching {currency_code} prices from CoinGecko:", response_coingecko_hnt.status_code,
              response_coingecko_iot.status_code)
else:
    print("Error fetching Balances:", response_hnt.status_code if hnt_address else None,
          response_iot.status_code if iot_address else None,
          response_mobile.status_code if mobile_address else None)
