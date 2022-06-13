import csv
import json
import os
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm, trange


class BookScraper:
    def __init__(self):
        self.root_url = "https://books.toscrape.com/"
        self.root_response = requests.get(self.root_url)
        self.root_soup = BeautifulSoup(self.root_response.text, 'html.parser')
        self.books = {}

        self.exports_dir = "exports/"
        self.csv_dir = "csv/"
        self.json_dir = "json/"
        self.covers_dir = "covers/"

    def start_scraper(self, config):
        """
        Create 'exports' directory and sub-directories
        Test connection
        Parse config options and start scraping process
        Return error for failed connection
        @param config: dict of config args
        """
        try:
            os.mkdir(self.exports_dir)
            os.mkdir(f"{self.exports_dir}{self.json_dir}")
            os.mkdir(f"{self.exports_dir}{self.csv_dir}")
            os.mkdir(f"{self.exports_dir}{self.covers_dir}")
        except FileExistsError:
            pass

        if self.root_response.status_code == 200:
            print("\n- connection ok -")
            categories = self.setup_categories()

            if config["category"]:
                if "html" in config["category"]:
                    if "index" not in config["category"]:
                        config["category"] = config["category"][:11] + "index.html"
                    categories = [(name, url) for name, url in categories if url == config["category"]]
                else:
                    categories = [(name, url) for name, url in categories if name == config["category"]]
                if not categories:
                    print("Invalid category, please retry.")
                    exit()

            book_urls = self.get_book_urls(categories)
            self.book_data(categories, book_urls)

            if config["json"]:
                self.export_json(categories)
            if config["csv"]:
                self.export_csv(categories)
            if not config["ignore_covers"]:
                self.download_images(categories)

        else:
            print(self.root_response.raise_for_status())
            exit()

    def setup_categories(self):
        """
        Get all categories names and urls
        @return: list of categories tuples (name, url)
        """
        categories = []
        categories_urls = [
            self.root_url + line["href"] for line in self.root_soup.select("ul > li > ul > li > a")
        ]
        category_names = self.root_soup.find("ul", class_="nav nav-list").find("ul").find_all("li")

        for i, url in enumerate(categories_urls):
            categories.append((category_names[i].text.strip().lower(), url))

        return categories

    def get_book_urls(self, categories):
        """
        For each category, get all books urls
        Check for extra pages (more than 20 books)
        Clean urls and return dict by category
        @param categories: list of categories tuples (name, url)
        @return: dict of all book urls lists by category
        """
        book_urls = {}

        for category in tqdm(categories, desc="Loading urls", ncols=80):
            response = requests.get(category[1])
            soup = BeautifulSoup(response.text, 'html.parser')
            books_total = int(soup.select_one("form > strong").text)
            if books_total > 20:
                page_total = int(soup.find("li", {"class": "current"}).text.replace("Page 1 of", ""))
            else:
                page_total = 1

            book_urls_clean = []
            for i in range(page_total):
                if page_total == 1:
                    response = requests.get(category[1])
                else:
                    response = requests.get(category[1].replace("index", f"page-{i + 1}"))
                soup = BeautifulSoup(response.text, "html.parser")
                book_raw_urls = [line["href"] for line in soup.select("ol > li > article > h3 > a")]
                for book in book_raw_urls:
                    book_urls_clean.append(book.replace("../../../", f"{self.root_url}catalogue/"))

            book_urls[category[0]] = book_urls_clean

        return book_urls

    def book_data(self, categories, book_urls):
        """
        For each book in a category, scrape and clean book data
        Add data to books instance
        @param categories: list of categories tuples (name, url)
        @param book_urls: dict of all book urls lists by category
        """
        for i in trange(len(categories), desc="Extracting data", ncols=80):
            self.books[categories[i][0]] = []

            for url in book_urls[categories[i][0]]:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                product_info = soup.find_all('td')
                description = soup.select_one("article > p").text.replace(' ...more', '')
                if description.isspace():
                    description = 'n/a'
                img = soup.find("div", {"class": "item active"}).find("img")
                img_url = img["src"].replace("../../", f"{self.root_url}")
                book_data = {
                    'product_page_url': url,
                    'universal_product_code': product_info[0].text,
                    'title': str(soup.find('h1').text),
                    'price_including_tax': product_info[3].text,
                    'price_excluding_tax': product_info[2].text,
                    'number_available': re.sub(r"\D", "", product_info[5].text),
                    'product_description': description,
                    'category': categories[i][0],
                    'review_rating': f"{self.review_rating(soup.select_one('.star-rating').attrs['class'][1])} star(s)",
                    'image_url': img_url
                }
                self.books[categories[i][0]].append(book_data)

    @staticmethod
    def review_rating(rating):
        """
        Compare star rating string to possible ratings list elements
        Convert rating into integer
        @param rating: star rating string
        @return: rating type int
        """
        ratings = ['One', 'Two', 'Three', 'Four', 'Five']
        for i, mark in enumerate(ratings):
            if rating == mark:
                return i + 1

    def export_csv(self, categories):
        """
        Export book data to csv files in exports directory
        @param categories: list of categories tuples (name, url)
        """
        headers = [
            'product_page_url',
            'universal_product_code',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url'
        ]

        for category in tqdm(categories, desc="Exporting to csv", ncols=80):
            csv_filename = category[0].lower().replace(' ', '_') + ".csv"
            csv_fullpath = f"./{self.exports_dir}{self.csv_dir}{csv_filename}"
            with open(csv_fullpath, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.books[category[0]])

    def export_json(self, categories):
        """
        Export book data to json files in exports directory
        @param categories: list of categories tuples (name, url)
        """
        for category in tqdm(categories, desc="Exporting to json", ncols=80):
            json_filename = category[0].lower().replace(' ', '_') + ".json"
            json_fullpath = f"./{self.exports_dir}{self.json_dir}{json_filename}"
            json_data = json.dumps(self.books[category[0]], indent=4)
            with open(json_fullpath, "w") as json_file:
                json_file.write(json_data)

    def download_images(self, categories):
        """
        Create category dirs within covers directory
        Set name for image files as "upc + book title"
        Download cover images
        @param categories: list of categories tuples (name, url)
        """
        for category in tqdm(categories, desc="Downloading cover images", ncols=80):
            img_category_dir = f"{self.exports_dir}{self.covers_dir}{category[0]}/"
            if not os.path.isdir(img_category_dir):
                os.mkdir(img_category_dir)

            for book in self.books[category[0]]:
                clean_img_name = ''.join([x for x in book['title'][:100] if x.isalnum() or x in ' ']).replace(' ', '_')
                img_name = f"{book['universal_product_code']}_{clean_img_name}.jpg"
                img_data = requests.get(book['image_url'])
                img_path = os.path.join(img_category_dir, img_name)
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data.content)
