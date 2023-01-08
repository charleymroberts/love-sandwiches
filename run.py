# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales") 
    sales_worksheet.append_row(data)
    print("Sales worksheet updated succesfully.\n")

data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)