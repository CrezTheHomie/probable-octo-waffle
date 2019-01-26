from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.request import Request, urlopen
from urllib.parse import urlsplit
from collections import deque
import re
import csv
from fake_useragent import UserAgent
import random

ua = UserAgent()  # From here we generate a random user agent
proxies = []  # Will contain proxies [ip, port]

# Main function

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


query = "\"video production\" + miami + \"contact\""
num_searches = 5

with open('leadsDB.csv', 'w', newline='') as f:
    fieldnames = ['url', 'possible email(s)', ' possible phone(s)']
    the_writer = csv.DictWriter(f, fieldnames=fieldnames)

    the_writer.writeheader()

    for url in search(query, tld="com", num=num_searches, stop=1, pause=10):
        # get url's content
        print("\nProcessing\n %s" % url)
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors
            continue

        # extract all email addresses and phone numbers and add them into the resulting set
        new_emails_list = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        new_phones_list = set(re.findall(
            r"(\d{3}[-\.\s]??\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\(\d{3}\)\d{7})",
            response.text, re.I))

        # helper to write csv
        new_email_string = ""
        first = True
        for new_email in new_emails_list:
            if first:
                new_email_string += new_email
                first = False
            else:
                new_email_string += " || " + new_email

        # helper to write csv
        new_phone_string = ""
        first = True
        for new_phone in new_phones_list:
            if first:
                new_phone_string += new_phone
                first = False
            else:
                new_phone_string += " || " + new_phone

        # write to csv if any useful data is found
        if(new_email_string or new_phone_string is not ""):
            print("emails found: " + new_email_string)
            print("phones found: " + new_phone_string)
            the_writer.writerow(
                {'url': url,
                 'email(s)': new_email_string,
                 'phone(s)': new_phone_string})
