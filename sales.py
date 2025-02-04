import pandas as pd
from file_manager import load_sales_log, save_products, save_sales_log
from shopping_cart import print_shopping_cart_items

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