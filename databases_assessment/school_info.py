'''Code to show and change information in a database about a class of children.
     Made by Elizabeth Watts on 24/03/25'''

#Note: All usernames are lowercase. The first letter of all child names is capitalised.
from werkzeug.security import check_password_hash,generate_password_hash
import sqlite3

#Define variables
DATABASE = 'school_info.db'
stop_action = 'cancel'
login_complete = 0
zero = 0
one = 1
two = 2
three = 3
str_zero = '0'
str_one = '1'
str_two = '2'
str_three = '3'
str_four = '4'
str_five = '5'
str_six = '6'

#Make functions:
#Functions to check things
def check_num_values(first_name):
    '''A function to check if there is a child
in the table with the given first name. Returns int'''
    first_name = first_name.title()
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = '''SELECT COUNT(child_id)
FROM children
WHERE first_name = "''' + first_name + '";' #Count the number of rows with the given first name
        cursor.execute(sql)
        results = cursor.fetchall() #Results should be zero if the child does not exist
        for result in results:
            return result[zero]
        
def check_if_valid(username):
    '''A function to check if the inputed username
exists and is valid in the passwords table. Returns 0 or 1'''
    username = username.lower()
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = '''SELECT COUNT(teacher_id)
FROM passwords
WHERE username = "''' + username + '";' #Count the number of rows with the given username
        cursor.execute(sql)
        results = cursor.fetchall() #Results should be either one or zero
        for result in results:
            return result[zero]

def check_password(username, password):
    '''A function to check if the inputed password matches the username.
    Returns True/False'''
    username = username.lower()
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = '''SELECT hashed_pw 
FROM passwords
WHERE username = "''' + username + '";' #Summon the correct password for the username
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            correct = result[zero]
        hashed_pw = correct
        if check_password_hash(hashed_pw, password):
            return True
        else:
            return False

def check_number_teachers():
    '''Counts the number of teachers in the 'passwords' table. Returns int.'''
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = '''SELECT COUNT(teacher_id)
FROM passwords;''' #Count the number of rows in the table
        cursor.execute(sql)
        results = cursor.fetchall()
        for result in results:
            return result[zero]
        
#Functions to print things

def print_info(columns, column_count):
    '''Print information in the "children" table
 of the database in the given columns'''
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "SELECT " + columns + " FROM children;"
        cursor.execute(sql)
        results = cursor.fetchall()
        for value in results:
            if column_count == two:
                print(f"{value[0]:<15}{value[1]}")
            elif column_count == 6:
                


def print_named_info(columns, firstname):
    '''Print one child's info from the "children" table
 of the database in the given columns'''
    firstname = firstname.title()
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "SELECT " + columns + ''' 
        FROM children 
        WHERE first_name = "''' + firstname + '";'
        cursor.execute(sql)
        results = cursor.fetchall()
        num_values = check_num_values(firstname)
        if num_values != zero:
            for value in results:
                try:
                    print(f"{value[zero]} {value[one]}, {value[two]}")
                except:
                    print(f"{value[zero]}\n{value[one]}")
        else:
            print('Child not found')

def print_both_names(firstname, lastname):
    '''Prints the full name and age of a child given both names.'''
    firstname = firstname.title()
    lastname = lastname.title()
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = '''SELECT first_name, second_name, age FROM children WHERE first_name = "'''
        sql = sql + firstname + '''" AND second_name = "''' + lastname + '";'
        cursor.execute(sql)
        results = cursor.fetchall()
        for value in results:
            print(f'{value[0]} {value[1]}, {value[2]}')


#Other functions with SQL

#Remove things:
def remove_teacher(username):
    username = username.lower()
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "DELETE FROM passwords WHERE username = '" + username + "';"
        cursor.execute(sql)
        print('Teacher deleted.')

def remove_child(firstname, lastname):
    firstname = firstname.title()
    if lastname:
        lastname = lastname.title()
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            lastname = lastname.title()
            firstname = firstname.title()
            sql = "DELETE FROM children WHERE first_name = '" + firstname + "' AND second_name = '" + lastname + "';"
            cursor.execute(sql)
    else:
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            firstname = firstname.title()
            sql = "DELETE FROM children WHERE first_name = '" + firstname + "';"
            cursor.execute(sql)
    print('Action Complete.')


#Edit existing things:
def change_child_info(name, column):
    '''Edit the basic info of a child given a name and column to change'''
    name = name.title()
    is_valid = True
    new_value = input(f'''What would you like to change the {column} 
of {name} to?\n''')
    if column == "age" or column == "parent_phone":
        try:
            new_value = int(new_value)
            new_value = str(new_value)
        except ValueError:
            is_valid = False
            print(f"Error. {column} must be an integer.")
    if is_valid == True:
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            sql = '''UPDATE children
            SET ''' + column + ' = '
            if column != "age" and column != "parent_phone":
                sql = sql + '"'
            sql = sql + new_value
            if column != "age" and column != "parent_phone":
                sql = sql + '"'
            sql = sql + ''' 
            WHERE first_name = "''' + name +'";'
            cursor.execute(sql)
            print('Change complete')   

def edit_password(username, password):
    username = username.lower()
    hashed_pw = generate_password_hash(password)
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "UPDATE passwords SET hashed_pw = '" + hashed_pw
        sql = sql + "' WHERE username = '" + username + "';"
        cursor.execute(sql)
        print('Password changed.')


#Add new things (SQL bits):
def add_child(firstname, lastname, age, parentphone, parentemail):
    firstname = firstname.title()
    lastname = lastname.title()
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = f'INSERT INTO children (' 
        if firstname:
            sql = sql + "first_name"
        if lastname:
            sql = sql + ", second_name"
        if age:
            sql = sql + ", age"
        if parentphone:
            sql = sql + ", parent_phone"
        if parentemail:
            sql = sql + ", parent_email"
        sql = sql + ') VALUES ('
        if firstname:
            sql = sql + '"' + firstname + '"'
        if lastname:
            sql = sql + ', "' + lastname + '"'
        if age:
            sql = sql + ', ' + age
        if parentphone:
            sql = sql + ", " + parentphone
        if parentemail:
            sql = sql + ', "' + parentemail + '"'
        sql = sql + ');'
        cursor.execute(sql)
        print('Addition successful')

def create_teacher(username, password):
    username = username.lower()
    hashed_pw = generate_password_hash(password)
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = "INSERT INTO passwords (username, hashed_pw)"
        sql = sql + " VALUES ('" + username + "', '" + hashed_pw + "');"
        cursor.execute(sql)



#Other functions without SQL:

def add_teacher():
    user_input = input('Please enter the username of the new teacher. Enter "cancel" to go back.\n')
    if check_if_valid(user_input) != zero:
        print('This username is already taken.')
    elif user_input == '':
        print('Error: Please enter a username.')
    elif user_input == stop_action:
        pass
    else:
        username = user_input
        user_input = str_one
        password = str_zero
        while user_input != password:
            password = input('Please enter the password for the new teacher. Enter "cancel" to go back.\n')
            if password == stop_action:
                break
            elif password == '':
                print('Error: please enter a password.')
            else:
                user_input = input('Re-enter password to confirm.\n')
                if user_input != password:
                    print('Inputs do not match. Please try again.')
                else:
                    print('Password confirmed.')
                    create_teacher(username, password)
                    print('Teacher added successfully.')

def delete_teacher():
    '''Function to check if a teacher exists, ask for password, and delete.'''
    user_input = input('Please enter the username of the teacher you wish to delete. Enter "cancel" to go back.\n')
    if user_input == stop_action:
        pass
    else:
        exists = check_if_valid(user_input)
        if exists == zero:
            print('Teacher not found.')
        else:
            username = user_input
            user_input = input("Teacher found. Please enter the teacher's password to delete. Enter 'cancel' to go back.\n")
            if user_input == stop_action:
                pass
            else:
                if check_number_teachers() == one:
                    print('No other teachers remaining. Cancelling action.')
                else:
                    if check_password(username, user_input):
                        print('Password correct. Deleting teacher.')
                        remove_teacher(username)
                    else:
                        print('Password incorrect. Please try again.')

def change_password():
    '''Function to change the password of an existing teacher.'''
    user_input = input('''Please enter the username of the teacher whose password you want to change.
Enter "cancel" to go back.\n''')
    if user_input == stop_action:
        pass
    else:
        exists = check_if_valid(user_input)
        if exists == zero:
            print('Teacher not found.')
        else:
            username = user_input.lower()
            user_input = input(f'''Teacher found. Please enter {username}'s existing password.
Enter "cancel" to go back.\n''')
            if user_input == stop_action:
                pass
            else:
                if check_password(username, user_input):
                    password = input('Password correct. Please enter new password.\n')
                    user_input = input('Re-enter password to confirm.\n')
                    if user_input == password:
                        print('Changing password.')
                        edit_password(username, password)
                    else:
                        print('Passwords do not match. Please try again.')
                else:
                    print('Password incorrect. Please try again.')


        

    
#Main 4 functions
def veiw_info():
    while True:
        user_input = input('''What would you like to view?
    1. All information
    2. All Children's names
    3. All parent contact info
    4. Information by child
    5. Parent information by child
    6. Back\n''')
        if user_input == str_one:
            print_info("*", 6)
        elif user_input == str_two:
            print_info("first_name, second_name", 2)
        elif user_input == str_three:
            print_info("parent_phone, parent_email", 2)
        elif user_input == str_four:
            user_input = input("Please enter the child's first name:\n")
            print_named_info("first_name, second_name, age", user_input)
        elif user_input == "5":
            user_input = input("Please enter the child's first name:\n")
            print_named_info("parent_phone, parent_email", user_input)
        elif user_input == "6":
            break
        else:
            print('Invalid input. Please try again')

def edit_info():
    while True:
        child_name = input('''Enter the first name of the child whose
information you would like to edit.
Enter 'cancel' to go back.\n''')
        if child_name == stop_action:
            break
        else:
            num_values = check_num_values(child_name)
            if num_values == zero:
                print('Child not found. Please try again')
            else:
                user_input = input('''What value do you want to change?
    1. First name
    2. Second name
    3. Age
    4. Parent phone number
    5. Parent email
    6. Back\n''')
                if user_input == str_one:
                    change_child_info(child_name, "first_name")
                elif user_input == str_two:
                    change_child_info(child_name, "second_name")
                elif user_input == str_three:
                    change_child_info(child_name, "age")
                elif user_input == str_four:
                    change_child_info(child_name, "parent_phone")
                elif user_input == str_five:
                    change_child_info(child_name, "parent_email")
                elif user_input == str_six:
                    break
                else:
                    print('Please enter a number 1-6.')

def new_child():
    while True:
        num_blank = 0
        user_input = input('''Enter the first name of the new child.
Enter "cancel" at any point to go back, or leave blank if unknown.\n''')
        if user_input.lower() == stop_action:
            break
        else:
            if user_input == '':
                num_blank += 1
            first_name = user_input.title()
        user_input = input('Enter the last name:\n')
        if user_input.lower() == stop_action:
            break
        else:
            if user_input == '':
                num_blank += 1
            last_name = user_input.title()
        user_input = input('Enter the age:\n')
        if user_input.lower() == stop_action:
            break
        else:
            if user_input == '':
                num_blank += 1
            else:
                try:
                    user_input = int(user_input)
                    user_input = str(user_input)
                except ValueError:
                    print('Error. Input must be an integer.')
                    break
            age = user_input
        user_input = input("Enter the parent's phone number:\n")
        if user_input.lower() == stop_action:
            break
        else:
            if user_input == '':
                num_blank += 1
            else:
                try:
                    user_input = int(user_input)
                    user_input = str(user_input)
                except ValueError:
                    print('Error. Input must be an integer.')
                    break
            parent_phone = user_input
        user_input = input("Enter the parent's email address:\n")
        if user_input.lower() == stop_action:
            break
        else:
            if user_input == '':
                num_blank += 1
            parent_email = user_input
        if num_blank == 5:
            print('At least one value must be entered. Try again.')
        else:
            add_child(first_name, last_name, age, parent_phone, parent_email)

def delete_child():
    while True:
        first_name = input('Please enter the first name of the child you wish to remove. Enter "cancel" to go back.\n')
        if first_name.lower() == stop_action:
            break
        else:
            results = check_num_values(first_name.title())
            if results == zero:
                print('Child not found. Please check spelling and try again.')
            elif results == one:
                print_named_info("first_name, second_name, age", first_name.title())
                user_input = input('Is this the child you want to remove? (Y/N)\n')
                if user_input.lower() == 'y':
                    remove_child(first_name, '')
                elif user_input.lower() == 'n':
                    break
            elif results >= two:
                print('Multiple results found.')
                last_name = input("Please enter the child's last name.\n")
                print('Is this the child you wish to delete? (Y/N)')
                print_both_names(first_name.title(), last_name.title())
                user_input = input()
                if user_input.lower() == 'y':
                    remove_child(first_name, last_name)
                

#Extra (admin) functions

def login():
    login_complete = False
    login_attempts = three
    while login_complete == False:
        username = input('Please enter username.\n')
        username = username.lower()
        if check_if_valid(username) == zero:
            print('Invalid username. Check spelling and try again')
        else:
            while login_complete != True:
                if login_attempts == zero:
                    print('All attempts used. Try again later.')
                    login_complete = True
                    return False
                user_input = input('Please enter password.\n')
                if check_password(username, user_input):
                    print('Password correct.')
                    login_complete = True
                    return True
                else:
                    print('Password incorrect.')
                    login_attempts -= 1
                    print(f'You have {login_attempts} attempt(s) remaining')

def admin_options():
    user_input = zero
    while user_input != str_four:
        user_input = input('''What would you like to do?
        1. Add new administrator
        2. Remove administrator from system
        3. Change an administrator password
        4. Back\n''')
        if user_input == str_one:
            add_teacher()
        elif user_input == str_two:
            delete_teacher()
        elif user_input == str_three:
            change_password()
        elif user_input != str_four:
            print('Please try again.')

    


#MAIN LOOP
if __name__ == "__main__":
    login_complete = True #login()
    if login_complete == True:
        print('.\n.\n.\n.')
        while True:
            user_input = input('''What would you like to do?
            1. Veiw information
            2. Edit information
            3. Add a child
            4. Remove a child
            5. Admin options
            6. Exit\n''')
            if user_input == str_one:
                print('You have chosen to veiw information.')
                veiw_info()
            elif user_input == str_two:
                print('You have chosen to edit information')
                edit_info()
            elif user_input == str_three:
                print('You have chosen to add a child')
                new_child()
            elif user_input == str_four:
                print('You have chosen to remove a child')
                delete_child()
            elif user_input == str_five:
                print('You have chosen to edit admin information.')
                admin_options()
            elif user_input == str_six:
                break
            else:
                print('That is not a valid input')
    else:
        pass
