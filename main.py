from lib.scrapper import Scrapper

if __name__ == "__main__":
    url_to_scrape = input("Enter the URL to scrape: ")
    Scrapper.scrape_url(url_to_scrape)
