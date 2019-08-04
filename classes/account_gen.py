# BSTN Account Generator
# Developed by @icysevnth - sevnth#0007

import requests
import names
import random
from datetime import datetime
from threading import Thread
import cloudscraper
import time
from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask
import sys
from colorama import Fore, init
init()

class BSTNGen():

    def __init__(self, catchall, password, captcha_solver, apikey, last_name, street, street_n, street2, zip_code, city, country, proxies):
        if '@' not in catchall:
            self.error("ERROR: Invalid catchall")
            exit()

        self.email = catchall
        self.proxies = [item.replace('\n','') for item in proxies]
        self.password = password
        self.provider = captcha_solver
        self.apikey = apikey
        self.host = 'http://www.bstn.com'
        self.last_name = last_name
        self.street = street
        self.street_n = street_n
        self.street2 = street2
        self.zip_code = zip_code
        self.city = city
        self.country = country
        
        self.s = cloudscraper.create_scraper(interpreter='js2py', recaptcha={'provider': self.provider,'api_key': self.apikey})

    def status(self, msg):
        print(Fore.CYAN + '[{}]: {}'.format(datetime.now(), str(msg)))
    def errorstatus(self, msg):
        print(Fore.YELLOW + '[{}]: {}'.format(datetime.now(), str(msg)))
    def error(self, msg):
        print(Fore.RED + '[{}]: {}'.format(datetime.now(), str(msg)))
    def success(self, msg):
        print(Fore.GREEN + '[{}]: {}'.format(datetime.now(), str(msg)))


    def get_random_ua(self):
        return random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        ])

    def choose_proxy(self, proxy_list):

        px = random.choice(proxy_list)

        if len(px.split(':'))  == 2:

            return {
                'http': 'http://{}'.format(px),
                'https': 'http://{}'.format(px)
                }

        elif len(px.split(':')) == 4:

            splitted = px.split(':')

            return {
                'http': 'http://{0}:{1}@{2}:{3}'.format(splitted[2], splitted[3], splitted[0], splitted[1]),
                'https': 'https://{0}:{1}@{2}:{3}'.format(splitted[2], splitted[3], splitted[0], splitted[1])
            }


    def enter(self):

        headers = {
            'Referer': 'https://www.bstn.com/it/',
            'User-Agent': self.get_random_ua(),
            'x-requested-with':	'XMLHttpRequest',
            'cache-control':'max-age=0'
        }

        name = names.get_first_name(gender='male')
        email = name + str(random.randint(10000, 10000000)) + self.email
        site_key = '6LfauBUUAAAAALXH1ZCY-B7RK-17mExJxJtf1ml6'
            
        if self.provider == '2captcha':
            
            self.status('Solving captcha...')

            urlcap = "http://2captcha.com/in.php?key=" + self.apikey + "&method=userrecaptcha&googlekey=" + site_key + "&pageurl=" + self.host 
            resp = self.s.get(urlcap) 
            
            if resp.text[0:2] != 'OK': 
                quit('Service error. Error code:' + resp.text) 
            
            captcha_id = resp.text[3:]
            fetch_url = "http://2captcha.com/res.php?key="+ self.apikey + "&action=get&id=" + captcha_id
    
            for i in range(1, 10):  
                time.sleep(5)
                resp = self.s.get(fetch_url)
                if resp.text[0:2] == 'OK':
                    break
            response = resp.text[3:]
        
        elif self.provider == 'anticaptcha':
            
            self.status('Solving captcha...')
        
            client = AnticaptchaClient(self.apikey)
            task = NoCaptchaTaskProxylessTask(self.host, site_key)
            job = client.createTask(task)
            job.join()
            response = job.get_solution_response()
        
        else:
            
            self.error('You must provide a captcha solver & api key on your config.json!')
            sys.exit()

        try:
            
            #print(self.choose_proxy(self.proxies))

            parameters = {
                "personal[email]": email,
                "personal[email_repeat]": email,
                "personal[password]": self.password,
                "personal[password_repeat]": self.password,
                "billaddress[salutation]": "1",
                "billaddress[forename]": name,
                "billaddress[lastname]": self.last_name,
                "billaddress[street]": self.street,
                "billaddress[street_number]": self.street_n,
                "billaddress[addition]": self.street2,
                "billaddress[zipcode]": self.zip_code,
                "billaddress[city]": self.city,
                "billaddress[country]": self.country,
                "billaddress[phone]": "",
                "shippingaddress[company]": "",
                "shippingaddress[salutation]": "1",
                "shippingaddress[forename]": name,
                "shippingaddress[lastname]": self.last_name,
                "shippingaddress[street]": self.street,
                "shippingaddress[street_number]": self.street_n,
                "shippingaddress[addition]": self.street2,
                "shippingaddress[zipcode]": self.zip_code,	
                "shippingaddress[city]": self.city,
                "shippingaddress[country]": self.country,
                "g-recaptcha-response": response
            }

            if len(self.proxies) > 0:
                #print(self.choose_proxy(self.proxies))
                accountPost = self.s.post("https://www.bstn.com/it/register/address", data=parameters, headers=headers, proxies=self.choose_proxy(self.proxies))
            else:
                accountPost = self.s.post("https://www.bstn.com/it/register/address", data=parameters, headers=headers)
            
            self.status('Registering account [{}]...'.format(accountPost.status_code))
            
            while accountPost.status_code == 403:
                self.error("You're banned from BSTN, rotating proxies...")
                
                if len(self.proxies) > 0:
                    #print(self.choose_proxy(self.proxies))
                    accountPost = self.s.post("https://www.bstn.com/it/register/address", data=parameters, headers=headers, proxies=self.choose_proxy(self.proxies))
                
                else:
                    self.errorstatus("Error: you don't have any proxies.")
                    sys.exit()
            
            print(accountPost.text)
            
            if 'kundenkonto' in accountPost.text or accountPost.status_code == 200:
                
                with open("accounts.txt", "a") as accounts:
                    accounts.write(email + ':' + self.password + "\n")
                
                    self.success('Account successfully created!')

        except requests.exceptions.ConnectionError:
            pass
        except Exception as e:
            self.error('An exception occured: {}'.format(e.__class__.__name_))
            time.sleep(2)
            sys.exit()
        
    def run(self, num):
        for i in range(num):
            Thread(target=self.enter).start()