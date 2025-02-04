import re
import pandas as pd

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