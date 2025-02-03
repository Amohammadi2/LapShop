import os
import json
import pandas as pd
import re
from functools import reduce
from file_manager import load_products, save_products, load_users, save_users, load_sales_log, save_sales_log, load_shopping_cart, save_shopping_cart

def clear_screen():
    """پاک کردن خروجی ترمینال."""
    os.system('cls' if os.name == 'nt' else 'clear')

def login():
    """ورود کاربر."""
    users = load_users()
    username = input("username: ")
    password = input("password: ")

    if username in users and users[username] == password:
        print("Login succeeded")
        input('Press enter to continue...')
        return username
    else:
        print("Username or password is incorrect")
        input('Press enter to continue...')
        return None

def register():
    """ثبت نام کاربر."""
    users = load_users()
    username = input("new username: ")
    password = input("new passwrod: ")

    if username in users:
        print("This username already exists, please choose another one")
        register() # repeat the process again
    else:
        users[username] = password
        save_users(users)
        print("Successfully registered")
        input('Press enter to continue...')

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

def display_products(df: pd.DataFrame):
    """نمایش محصولات در قالب جدولی."""
    if df.empty:
        print("No products found")
        input('Press enter to continue...')
        return
    start = 0
    chunk_size = 50
    end = chunk_size
    total_rows = len(df)
    print('~~~ Lapshop / Products ~~~~')
    while start < total_rows:
        # Display the current chunk of rows
        print(df[start:end].to_string())
        
        # Ask the user if they want to load more rows
        user_input = input("Do you want to load more rows? (y/n): ").strip().lower()
        
        if user_input != 'y':
            print("Loading stopped by user.")
            break
        
        # Update the start and end indices for the next chunk
        start = end
        end += chunk_size
        
        # Ensure we don't go beyond the total number of rows
        if end > total_rows:
            end = total_rows
    input('Press enter to return...')

def parse_condition(condition):
    """تجزیه و تحلیل شرط فیلتر."""
    condition = condition.strip()
    match = re.match(r'([a-zA-Z]+)\s*([=><!]+)\s*("?[a-zA-Z0-9\s]+"?|\d+)', condition)
    if not match:
        return None
    field, operator, value = match.groups()
    value = value.strip('"')
    try:
        if value.isdigit():
            value = int(value)
        return field, operator, value
    except ValueError:
      return None

def apply_condition(df, field, operator, value):
    # Convert value to the appropriate type (e.g., int, float, or str)
    try:
        value = int(value)
    except ValueError:
        try:
            value = float(value)
        except ValueError:
            pass  # Keep as string
    
    # Apply the filter based on the operator
    if operator == "==":
        return df[field] == value
    elif operator == "!=":
        return df[field] != value
    elif operator == "<":
        return df[field] < value
    elif operator == "<=":
        return df[field] <= value
    elif operator == ">":
        return df[field] > value
    elif operator == ">=":
        return df[field] >= value
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def apply_filters(df, filter_str):
    # Split the filter_str into tokens (conditions and operators)
    tokens = filter_str.split()
    
    # Stack to keep track of conditions and operators
    stack = []
    i = 0
    while i < len(tokens):
        if tokens[i] in ["AND", "OR"]:
            # Push the operator onto the stack
            stack.append(tokens[i])
            i += 1
        else:
            # Parse the condition
            condition = ' '.join(tokens[i:i+3])  # A condition is 3 tokens (e.g., "price < 700000")
            field, operator, value = parse_condition(condition)
            mask = apply_condition(df, field, operator, value)
            stack.append(mask)
            i += 3
    
    # Evaluate the stack with proper precedence (AND has higher precedence than OR)
    # First, evaluate all AND operations
    and_evaluated_stack = []
    j = 0
    while j < len(stack):
        if isinstance(stack[j], pd.Series):  # It's a mask
            and_evaluated_stack.append(stack[j])
            j += 1
        elif stack[j] == "AND":
            # Pop the last mask and apply AND with the next mask
            left_mask = and_evaluated_stack.pop()
            right_mask = stack[j + 1]
            and_evaluated_stack.append(left_mask & right_mask)
            j += 2
        elif stack[j] == "OR":
            # Push OR operator to the stack for later evaluation
            and_evaluated_stack.append(stack[j])
            j += 1
    
    # Now evaluate all OR operations
    final_mask = and_evaluated_stack[0]
    j = 1
    while j < len(and_evaluated_stack):
        if and_evaluated_stack[j] == "OR":
            # Apply OR with the next mask
            right_mask = and_evaluated_stack[j + 1]
            final_mask = final_mask | right_mask
            j += 2
        else:
            j += 1
    
    # Apply the final mask to the DataFrame
    filtered_df = df[final_mask]
    return filtered_df

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


def finalize_purchase(user:str, cart: list[int], products_df: pd.DataFrame):
    """نهایی کردن خرید و آپدیت موجودی."""
    if not cart:
        print("Your cart is empty, try adding a few items first")
        input('Press enter to continue...')
        return products_df

    print("Your shopping cart items:")
    print_shopping_cart_items(products_df, cart)

    confirm = input("Are you sure you wanna finalize your purchase? (y/n): ").strip().lower()
    if confirm != 'y':
      print("Purchase cancled")
      return products_df

    # ثبت لاگ فروش
    final_shopping_cart = products_df.iloc[cart].copy()
    final_shopping_cart['user'] = user
    sales_log = load_sales_log()
    if sales_log.empty:
        sales_log = pd.DataFrame(columns=final_shopping_cart.columns)
    sales_log = pd.concat([sales_log, final_shopping_cart], ignore_index=True)
    save_sales_log(sales_log)
    print("Purchase successful")# حذف محصولات فروخته شده از لیست محصولات موجود
    product_ids_to_remove = set(cart)
    products_df = products_df.drop(product_ids_to_remove, errors='ignore')

    # اپدیت اطلاعات محصولات
    save_products(products_df)
    input('Press enter to continue...')

    return products_df


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

if __name__ == "__main__":
    main_menu()