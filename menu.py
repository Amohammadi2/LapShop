from file_manager import (load_products, load_shopping_cart, save_shopping_cart)
from products import display_products, apply_filters
from sales import finalize_purchase
from utils import clear_screen
from authorization import login, register
from shopping_cart import show_shopping_cart


def main_menu():
    """منوی اصلی."""
    while True:
        clear_screen()
        print("~~~~ LapShop ~~~~")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            username = login()
            if username:
                show_user_menu(username)
        elif choice == '2':
            register()
        elif choice == '3':
            break
        else:
            print("Invalid choice")
            input('Press enter to continue...')


def show_user_menu(username):
    """منوی کاربر بعد از لاگین."""
    products_df = load_products()
    cart = load_shopping_cart(username)
    while True:
        clear_screen()
        print(f"Welcome, {username}!")
        print("1. Products list")
        print("2. Apply filters")
        print("3. Shopping cart")
        print("4. Finalize purchase")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_products(products_df)
        elif choice == '2':
            while True:
              filter_str = input("Enter the filter condition: ")
              try:
                filtered_products = apply_filters(products_df, filter_str)
              except:
                print("Incorrect filter condition")
              else:
                  if filtered_products.empty:
                      print("No product was found with the search criteria")
                      input("Press enter to continue... ")
                  else:
                      display_products(filtered_products)
                  break
        elif choice == '3':
            show_shopping_cart(products_df, cart)
            save_shopping_cart(username, cart)
        elif choice == '4':
            products_df = finalize_purchase(username, cart, products_df)
            save_shopping_cart(username, [])
            cart = []
        elif choice == '5':
            break
        else:
            print("Invalid choice")