import pandas as pd
from utils import clear_screen

def add_to_cart(cart: list[int]):
    """افزودن کالا به سبد خرید."""
    while True:
        try:
            product_indices = input("Enter a comma-separated list of numbers to choose products: ")
            selected_indices = [int(i.strip()) for i in product_indices.split(',')]
            cart.extend(selected_indices)
            print(f"{len(selected_indices)} products were added to your cart")
            input('Press enter to continue...')
            return cart

        except (ValueError, IndexError):
            print("Invalid input, please choose current range of numbers for products")
            input('Press enter to continue...')
            continue

def remove_from_cart(cart: list[int]):
    while True:
        try:
            product_indices = input("Enter a comma-separated list of numbers to remove from your cart: ")
            selected_indices = [int(i.strip()) for i in product_indices.split(',')]
            for i in selected_indices:
                cart[i] = -1
            while -1 in cart:
                cart.remove(-1)
            print(f"{len(selected_indices)} products were removed from your cart")
            input('Press enter to continue...')
            return cart

        except (ValueError, IndexError):
            print("Invalid input, please choose current range of numbers for products")
            input('Press enter to continue...')
            continue

def clear_cart(cart: list[int]):
    if input('Are you sure you wanna clear all items? (y/n)') != 'y':
        return
    cart.clear()

def print_shopping_cart_items(products_df: pd.DataFrame, cart: list[int]):
    print('------------------[ITEMS]------------------')
    if len(cart) != 0:
        print(products_df.iloc[cart].to_string())
    else:
        print('Your shopping cart is empty, try adding a few items')

def show_shopping_cart(products_df: pd.DataFrame, cart: list[int]):
    while True:
        clear_screen()
        print("~~~~ LapShop / Shopping Cart ~~~~")
        print('1. Add new items')
        print('2. Remove items')
        print('3. Clear all items')
        print('4. Back to main menu')
        print_shopping_cart_items(products_df, cart)

        choice = input("Enter your choice: ")
        if choice == '1':
            add_to_cart(cart)
        elif choice == '2':
            remove_from_cart(cart)
        elif choice == '3':
            clear_cart(cart)
        elif choice == '4':
            break
        else:
            print('Invalid choice')
            input('Press enter to continue...')