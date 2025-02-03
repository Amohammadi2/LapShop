import json
import pandas as pd

# مسیر فایل ذخیره اطلاعات کاربران
USER_DATA_FILE = "data/users.json"

# مسیر فایل ذخیره اطلاعات محصولات
PRODUCT_DATA_FILE = "data/laptops.csv"

# مسیر فایل لاگ فروش
SALES_LOG_FILE = "data/sales_log.csv"

SHOPPING_CART_FILE = 'data/shopping_cart.json'


def load_users():
    """بارگذاری اطلاعات کاربران از فایل."""
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    """ذخیره اطلاعات کاربران در فایل."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_shopping_cart(user):
    try:
        with open(SHOPPING_CART_FILE, 'r') as f:
            return json.load(f)[user]
    except:
        return []
    
def save_shopping_cart(user, cart: list[int]):
    with open(SHOPPING_CART_FILE, 'r') as f:
        data = json.load(f)
        data[user] = cart
    with open(SHOPPING_CART_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def load_products():
    """بارگذاری اطلاعات محصولات از فایل."""
    try:
        return pd.read_csv(PRODUCT_DATA_FILE,delimiter=',')
    except:
        return pd.DataFrame()

def save_products(df: pd.DataFrame):
    """ذخیره اطلاعات محصولات در فایل."""
    df.to_csv(PRODUCT_DATA_FILE, index=False)


def load_sales_log():
    """بارگذاری لاگ فروش از فایل."""
    try:
        return pd.read_csv(SALES_LOG_FILE,delimiter=',')
    except:
        return pd.DataFrame()

def save_sales_log(sales_log: pd.DataFrame):
    """ذخیره لاگ فروش در فایل."""
    sales_log.to_csv(SALES_LOG_FILE, index=False)