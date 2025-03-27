'''Code to show and change information in a database about a class of children.
     Made by Elizabeth Watts on 24/03/25'''

import sqlite3

#Define variables
DATABASE = 'school_info.db'

#Make functions
def print_info(columns):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "SELECT " + columns + " FROM children;"
        cursor.execute(sql)
        results = cursor.fetchall()
        for value in results:
            print(value)

def print_named_info(columns, firstname):
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "SELECT " + columns + ''' 
        FROM children 
        WHERE first_name = ''' + firstname.title() + ';'
        cursor.execute(sql)
        results = cursor.fetchall()
        for value in results:
            print(value)

def veiw_info():
    while:
        user_input = input('''What would you like to veiw?
    1. All information
    2. All Children's names
    3. All parent contact info
    4. Information by child
    5. Parent information by child
    6. Back\n''')
        if user_input == "1":
            print_info("*")
        elif user_input == "2":
            print_info("child_id, first_name, second_name")
        elif user_input == "3":
            print_info("parent_phone, parent_email")
        elif user_input == "4":
            user_input = input("Please enter the child's first name:\n")
            print_named_info("child_id, first_name, second_name, age", user_input)
        elif user_input == "5":
            user_input = input("Please enter the child's first name:\n")
            print_named_info("child_id, parent_phone, parent_email", user_input)
        elif user_input == "6":
            break
        else:
            print('Invalid input. Please try again')

def edit_info():
    while True:
        user_input = input('''What child would you like to edit?''')

#Main loop
while True:
    user_input = input('''What would you like to do?
    1. Veiw information
    2. Edit information
    3. Add/remove information
    4. Exit\n''')
    if user_input == '1':
        print('You have chosen to veiw information.')
        veiw_info()
    elif user_input == '2':
        print('You have chosen to edit information')
    elif user_input == '3':
        print('You have chosen to add/remove information')
    elif user_input == '4':
        break
    else:
        print('That is not a valid input')
