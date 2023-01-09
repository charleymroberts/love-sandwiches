# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures from the user
    """
    while True:
        #while True is an infinite loop that is only stopped by the break command
        print("Please enter sales data from the last market")
        print("Sales data should be separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid!")
            break
        #the 'if' here refers to the return True/False in the validate_data function
        #so it calls the function and checks if the function returns True (data valid) or False
        #short for if validate_data == True, i.e. if the data is valid

    return sales_data

def validate_data(values):
    """
    Checks that data inputted by user is in correct format and displays error message if not
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
        #if the data is not valid, the function stops here and returns false
        #this makes the previous function request data from the user again

    return True 
    #if the data is valid, it gets to this point and returns True

# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales") 
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated succesfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus for each item type
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(f"Stock row: {stock_row}")
    print(f"Sales row: {sales_row}")

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

# def update_surplus_data(data):

#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus") 
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully\n")

def update_worksheet(data, worksheet):
    """
    Updates worksheets with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated succesfully\n")

def get_last_5_entries_sales():
    """
    Calculates average number of sandwiches sold at the last five markets
    """
    sales = SHEET.worksheet("sales")

    columns = []

    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns

def calculate_stock_data(data):
    """
    Calculate average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(f"Surplus: {new_surplus_data}")
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches Data Automation")
main()