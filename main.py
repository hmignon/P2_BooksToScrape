import argparse
import time

from scraper import BookScraper


def timer(start):
    end_time = int(time.time()) - start
    print(f"\n\nBooks exported in {end_time // 60} mins {end_time % 60} secs.")


def main():
    parser = argparse.ArgumentParser(
        description="BooksToScrape",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-c", "--csv", action="store_true", help="Export to csv files")
    parser.add_argument("-j", "--json", action="store_true", help="Export to json files")
    parser.add_argument("--ignore-covers", action="store_true", help="Skip cover downloads")
    parser.add_argument("--category", type=str, nargs="?", default=None, help="Scrape one category (name or full url)")
    args = parser.parse_args()
    config = vars(args)
    if not config["json"] and not config["csv"]:
        config["csv"] = True

    start = int(time.time())
    scraper = BookScraper()
    scraper.start_scraper(config)
    timer(start)


if __name__ == "__main__":
    main()
