from utils import check_data_folder, create_missing_files
from scraper import start_scraping

if __name__ == '__main__':
    if not check_data_folder():
        create_missing_files()
    start_scraping()

print("[LOG] Scraping successfully finished, now you can run 'main.py' script")