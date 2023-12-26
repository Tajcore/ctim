from urllib.parse import urlencode

import requests

# Configuration for OAuth
client_secret = "gbmy7NXG1PDPvW2x4dHyFFNnQ0i22T6axX6yEaeF9wndclejYHQWdAwcEgEYeyR7dmy07lzFfM1SkjmyetGloRvjTADOx2k8rn4tdNomVPvaw6hnYdMj7m7iNuCo7SlP"  # noqa: E501
client_id = "Aru35B2NfM5EI4mpyWOkoxnN1k10Wamy3lTI7GMX"
authorization_base_url = "https://api.thompson.gr/o/authorize/"
token_url = "https://api.thompson.gr/o/token/"
redirect_uri = "http://127.0.0.1:8088/"
scope = "read"


# User Authorization
# Construct the authorization URL
params = {"response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri, "scope": scope}

print(params)

authorization_url = f"{authorization_base_url}?{urlencode(params)}"

print("Please go here and authorize:", authorization_url)

# Get the authorization verifier code from the callback URL
# redirect_response = input('Paste the full redirect URL here: ')

# Extract the code from the redirect response
# from urllib.parse import urlparse, parse_qs
# parsed_url = urlparse(redirect_response)
# code = parse_qs(parsed_url.query)['code'][0]

token_url = "https://api.thompson.gr/o/token/"
code = input("Paste the code from the redirect URL here: ")

# Exchange the code for an access token
data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret,
}

print(data)

response = requests.post(token_url, data=data)

# Check if the request was successful
if response.status_code == 200:
    token = response.json()
    print("Access Token:", token)
else:
    print("Failed to obtain access token:", response, response.status_code, response.text)
