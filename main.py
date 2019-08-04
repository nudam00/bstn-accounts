from classes.account_gen import BSTNGen
import json

try:
    config = json.load(open('config.json'))

    catchall = config['catchall']
    accounts = config['accounts']
    password = config['password']
    captcha_solver = config['captcha_solver']
    apikey = config['api_key']
    last_name = config['address_last_name']
    street = config['address_street']
    street_n = config['address_street_number']
    street2 = config['address_street_2']
    zip_code = config['address_zipcode']
    city = config['address_city']
    country = config['address_country_id']

    proxies = open('proxies.txt').readlines()
    print("Loaded %d proxies"%len(proxies))

    account = BSTNGen(catchall, password, captcha_solver, apikey, last_name, street, street_n, street2, zip_code, city, country, proxies)
    account.run(accounts)

# case where config file is missing
except FileNotFoundError:
    print("FATAL ERROR: Could not find config file")

# case where config file is not valid json
except json.decoder.JSONDecodeError:
    print("FATAL ERROR: Could not read config file, invalid JSON")

# case where we don't know the cause of the exception
except Exception as e:
    print("Unknown error: " + str(e))