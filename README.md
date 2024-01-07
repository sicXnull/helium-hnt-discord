# Helium Discord Notification

This script grabs HNT/IOT wallet balances and converts to USD/Other currencies

![image](https://github.com/sicXnull/helium-hnt-discord-embed/assets/31908995/353d429f-3a7b-4a40-97c8-4d707089bcc8)


## Installation


## Edit the following variables

1. `coingecko_api_key` - Create a free coingecko API key https://apiguide.coingecko.com/getting-started/getting-started


2. `hnt_address` , `iot_address` & `mobile_address` Your Helium/IOT/Mobile token account number. Leave blank if you do not have IOT/Mobile
  * https://solscan.io/account/Your-Account-Number#portfolio

![image](https://github.com/sicXnull/helium-hnt-discord/assets/31908995/cf0236ef-fa63-4831-b325-008143f115c5)


3. `webhook_url` - add your discord webhook 

4. `currency_code` - Currently set to USD. Set to the supported currencies or add your own Current options

```
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
```


## Run 

Run as cronjob. Example, every 6 hours. 

```
0 */6 * * * python3 /opt/helium/helium.py
```

