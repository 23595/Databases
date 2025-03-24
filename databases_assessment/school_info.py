'''Code to show and change information in a database about a class of children.
     Made by Elizabeth Watts on 24/03/25'''

import sqlite3

#Define variables
DATABASE = 'school_info.db'

#Make functions
def print_all_info():
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = ";"
        cursor.execute(sql)
        results = cursor.fetchall()
        for value in results:
            print(value)

#Main loop
while True:
    user_input = input('''What would you like to do?
    1. Veiw information
    2. Edit information
    3. Add/remove information
    4. Exit\n''')
    if user_input == '1':
        print('You have chosen to veiw information')
    elif user_input == '2':
        print('You have chosen to edit information')
    elif user_input == '3':
        print('You have chosen to add/remove information')
    elif user_input == '4':
        break
    else:
        print('That is not a valid imput')