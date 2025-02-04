import os
import json

def check_data_folder():
    # Check if the 'data' folder exists
    if os.path.exists('data') and os.path.isdir('data'):
        return True
    else:
        return False
    
def create_missing_files():
    os.makedirs('data')
    print("Created 'data' folder.")
    # Define the files and their initial content
    files_to_create = {
        'laptops.csv': '',
        'sales_log.csv': '',
        'shopping_cart.json': {},
        'users.json': {}
    }

    # Create the files if they don't exist
    for filename, content in files_to_create.items():
        file_path = os.path.join('data', filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                if filename.endswith('.json'):
                    # Write JSON content
                    json.dump(content, file, indent=4)
                else:
                    # Write empty content for CSV files
                    file.write(content)
            print(f"Created file: {file_path}")
        else:
            print(f"File already exists: {file_path}")

def clear_screen():
    os.system('cls')