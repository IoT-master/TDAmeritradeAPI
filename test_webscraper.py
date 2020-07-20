from Webscraper import LoginClass
from TDAmeritrade import TDAmeritrade
import ujson


def load_from_json(filename):
    with open(filename, 'r') as f:
        return ujson.loads(f.read())


config = load_from_json('Confidential/config.json')
fetching_token = LoginClass()
fetching_token.logging_in(
    f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={config['redirect_uri']}&client_id={config['client_id']}%40AMER.OAUTHAP")
fetching_token.browser.find_element_by_id(
    'username').send_keys(config['username'])
fetching_token.browser.find_element_by_id(
    'password').send_keys(config['password'])
fetching_token.browser.find_element_by_id('accept').click()
fetching_token.browser.implicitly_wait(1)
fetching_token.browser.find_element_by_id('accept').click()
fetching_token.browser.implicitly_wait(1)
my_input = input('Give me user code =>')
fetching_token.browser.find_element_by_id('smscode').send_keys(my_input)
fetching_token.browser.find_element_by_id('accept').click()
fetching_token.browser.implicitly_wait(1)
fetching_token.browser.find_element_by_id('accept').click()
print(fetching_token.browser.current_url)
