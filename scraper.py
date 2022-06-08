import csv
import os
import re

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class BookScraper:
    def __init__(self):
        self.main_url = "https://books.toscrape.com/"
        self.response = requests.get(self.main_url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.exports_dir = "exports/"
        self.csv_dir = "csv/"
        self.covers_dir = "covers/"

    def start_scraper(self):
        """
        Create exports directory and sub-directories
        Test connection
        Return error for failed connection
        """
        try:
            os.mkdir(self.exports_dir)
            os.mkdir(f"{self.exports_dir}{self.csv_dir}")
            os.mkdir(f"{self.exports_dir}{self.covers_dir}")
        except FileExistsError:
            pass

        if self.response.status_code == 200:
            print("\n- connection ok -")
            self.get_urls()

        else:
            print(self.response.raise_for_status())
            exit()

    def get_urls(self):
        """
        Get all categpries urls
        Get all urls from each category
        """
        urls = {}
        book_info = {}
        categories = []
        categories_urls = [
            self.main_url + line["href"] for line in self.soup.select("ul > li > ul > li > a")
        ]

        print("\nGetting urls...")
        for url in tqdm(categories_urls):
            category_name = url.replace('https://books.toscrape.com/catalogue/category/books/', '')
            category_name = category_name.replace('/index.html', '').replace('_', '').replace('-', ' ')
            category_name = re.sub(r'\d+', '', category_name)
            categories.append(category_name)
            book_info[f"{category_name}"] = []

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            books_total = int(soup.select_one("form > strong").text)
            if books_total > 20:
                page_total = int(soup.find("li", {"class": "current"}).text.replace("Page 1 of", ""))
            else:
                page_total = 1

            book_urls_clean = []
            for i in range(page_total):
                if page_total == 1:
                    response = requests.get(url)
                else:
                    response = requests.get(url.replace('index', f"page-{i + 1}"))
                soup = BeautifulSoup(response.text, 'html.parser')
                book_urls = [line["href"] for line in soup.select("ol > li > article > h3 > a")]
                for book in book_urls:
                    book_urls_clean.append(book.replace("../../../", "https://books.toscrape.com/catalogue/"))

            urls[f"{category_name}"] = book_urls_clean

        self.book_data(urls, book_info, categories)

    def book_data(self, urls, book_info, categories):
        """
        Scrape book info for each category
        @param urls: dict of all books urls
        @param book_info: empty dict of books data
        @param categories: list of all categories names
        """
        print("\nDownloading book info...")
        for i in tqdm(range(len(urls))):
            for url in urls[f"{categories[i]}"]:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                product_info = soup.find_all('td')
                description = soup.select_one("article > p").text.replace(' ...more', '')
                if description.isspace():
                    description = 'n/a'
                img = soup.find("div", {"class": "item active"}).find("img")
                img_url = img["src"].replace("../../", f"{self.main_url}")
                book_data = {
                    'product_page_url': url,
                    'universal_product_code': product_info[0].text,
                    'title': str(soup.find('h1').text),
                    'price_including_tax': product_info[3].text,
                    'price_excluding_tax': product_info[2].text,
                    'number_available': re.sub(r"\D", "", product_info[5].text),
                    'product_description': description,
                    'category': categories[i],
                    'review_rating': f"{self.review_rating(soup.select_one('.star-rating').attrs['class'][1])} star(s)",
                    'image_url': img_url
                }
                book_info[f"{categories[i]}"].append(book_data)

        self.export_csv(categories, book_info)
        self.download_images(book_info, categories)

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

    def export_csv(self, categories, book_info):
        """
        Export book data to csv files in exports directory
        @param categories: list of categories names
        @param book_info: dict of all books info
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

        print("\nExporting data...")
        for category in tqdm(categories):
            csv_filename = category.lower().replace(' ', '_') + ".csv"
            csv_fullpath = f"./{self.exports_dir}{self.csv_dir}{csv_filename}"
            with open(csv_fullpath, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                writer.writerows(book_info[f"{category}"])

    def download_images(self, book_info, categories):
        """
        Download cover images to exports directory
        @param book_info: dict of all books info
        @param categories: list of categories names
        """
        print("\nDownloading cover images...")
        for category in tqdm(categories):
            img_category_dir = f"{self.exports_dir}{self.covers_dir}{category}/"
            if not os.path.isdir(img_category_dir):
                os.mkdir(img_category_dir)

            for book in book_info[f'{category}']:
                clean_img_name = ''.join([x for x in book['title'][:100] if x.isalnum() or x in ' ']).replace(' ', '_')
                img_name = f"{book['universal_product_code']}_{clean_img_name}.jpg"
                img_data = requests.get(book['image_url'])

                img_path = os.path.join(img_category_dir, img_name)
                with open(img_path, 'wb') as handler:
                    handler.write(img_data.content)
