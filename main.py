# -*- coding: utf-8 -*-

"""
===================================================================
                    SCRAPING BOOKS.TOSCRAPE.COM

This program will scrape books information from books.toscrape.com 
with BeautifulSoup4, export the data to .csv files and download the
cover images to an 'exports' folder
===================================================================

"""

import time

import requests
from bs4 import BeautifulSoup

from category_info import get_cat_pages_urls


def main():
    """
    Prompt the user to choose whether they want to scrape
    the entire website or only one category
    Get all category urls into a list
    If 1 category, compare user input to list
    """
    print("\n\n-----------------------------")
    print("\n Scraping books.toscrape.com\n")
    print("-----------------------------\n\n")
    time.sleep(1)
    main_url = 'https://books.toscrape.com/'
    response = requests.get(main_url)

    if response.status_code == 200:
        print("\n- connection ok -")
        soup = BeautifulSoup(response.text, 'html.parser')
        cat_url_list = [main_url + line["href"] for line in soup.select("ul > li > ul > li > a")]

        url = input('\n\nPaste the url you would like to scrape : ')
        start_time = int(time.time())

        if url.replace('index.html', '') == main_url:
            print("\nExporting all categories...\n")
            for i in range(len(cat_url_list)):
                get_cat_pages_urls(cat_url_list[i])
            print('All books exported in {0} seconds.'.format(int(time.time()) - start_time))
            time.sleep(1)
            print('\n------END------')

        elif url in cat_url_list:
            index = cat_url_list.index(url)
            cat_url = cat_url_list[index]
            get_cat_pages_urls(cat_url)
            print('\n\nAll books exported in {0} seconds.'.format(int(time.time()) - start_time))
            time.sleep(1)
            print('\n------END------')

        else:
            print('\n\nPlease enter a valid url (full website or one category).\n\n')
            time.sleep(2)
            main()

    else:
        response.raise_for_status()
        print("\n- connection error -")
        print("Please check connection status.")
        time.sleep(1)
        retry = input("Retry? (y/n) :").lower().strip()
        while retry != "y" != "n":
            print("input error")
            retry = input("Retry? (y/n) :").lower().strip()
        if retry == "y":
            print("Restarting...")
            time.sleep(2)
            main()
        elif retry == "n":
            print('Closing application...')
            time.sleep(2)
            exit()


if __name__ == "__main__":
    main()
