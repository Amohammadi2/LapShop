from scraper import start_scraping
from menu import clear_screen, main_menu
from utils import check_data_folder, create_missing_files


if __name__ == '__main__':
    # if it doesn't exist, we need to setup the app first
    if not check_data_folder():
        print("You still haven't initialized the inventory, run the 'init_inventory.py' script first to scrape some data")
        exit()
    main_menu()