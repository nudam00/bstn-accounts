# BSTN Account Generator

Generate as many accounts as you wish on [BSTN](https://www.bstn.com)

Requires python 3.6 or above.

## Config

+ **accounts**:  number of accounts you want to create
+ **captcha_solver**: your captcha solver provider (e.g: 2captcha)
+ **api_key**: your api key
+ **catchall**: your catchall (e.g: @xyz.club)
+ **password**: your accounts desired passowrd
+ **address_last_name**: your surname
+ **address_street**: your address street
+ **address_street_number**: your address street number
+ **address_street_2**: your address addition (leave blank if you don't have one)
+ **address_zip_code**: your zip code
+ **address_city**: your city
+ **address_country_id**: your `BSTN country ID` (you can easily find this with Chrome devtools)



## How to Run

+ Download python installer from [here](https://www.python.org/downloads/release/python-367/) (skip if you already have python 3.6 or above)
+ Install every required module (e.g `pip3 install modulename`)
+ Edit `config.json`
+ Type proxies in `proxies.txt` or clear file to run without proxies
+ Run `main.py` by typing `python3 main.py` on terminal.


MacOS / Linux users: `pip3 / python3`

Windows users: `pip / python`
