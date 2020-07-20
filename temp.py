import json


def get_client(secrets_path):
    'Returns an OAuth client, using the given path as a secrets store'
    # Find you
    API_KEY = '<Your API Key, AKA Client ID>@AMER.OAUTHAP'
    REDIRECT_URI = '<Your Redirect URI>'

    import os
    import pickle
    from requests_oauthlib import OAuth2Session

    # Load old token from secrets directory
    token_path = os.path.join(os.path.expanduser(secrets_path), 'token.json')
    token = None
    try:
        with open(token_path, 'rb') as f:
            token = pickle.load(f)
            print(token)
    except FileNotFoundError:
        pass

    # On failure, fetch a new token using OAuth and Selenium. Unfortunately TD
    # only supports the webapp workflow, so we have to open up a browser.
    if token is None:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        oauth = OAuth2Session(API_KEY, redirect_uri=REDIRECT_URI)
        authorization_url, state = oauth.authorization_url(
            'https://auth.tdameritrade.com/auth')

        # Open a Chrome browser to take the credentials
        chrome_options = Options()
        user_data_dir = os.path.join(secrets_path, 'chrome')
        chrome_options.add_argument("user-data-dir={}".format(user_data_dir))
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(authorization_url)

            # Wait to catch the redirect
            import time
            callback_url = ''
            while not callback_url.startswith(REDIRECT_URI):
                callback_url = driver.current_url
                time.sleep(1)

            token = oauth.fetch_token(
                'https://api.tdameritrade.com/v1/oauth2/token',
                authorization_response=callback_url,
                access_type='offline',
                client_id=API_KEY,
                include_client_id=True)

    # Record the token
    def update_token(t):
        with open(token_path, 'wb') as f:
            pickle.dump(t, f)
    update_token(token)

    # Return a new session configured to refresh credentials
    return OAuth2Session(API_KEY, token=token,
                         auto_refresh_url='https://api.tdameritrade.com/v1/oauth2/token',
                         auto_refresh_kwargs={'client_id': API_KEY},
                         token_updater=update_token)


client = get_client(secrets_path)
resp = client.get(
    'https://api.tdameritrade.com/v1/marketdata/quotes',
    params={'apikey': API_KEY, 'symbol': 'AAPL'})
resp = resp.json()
