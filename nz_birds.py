import sqlite3

#Variable declarations
DATABASE = 'nz_birds.db'
user_input = "1"
statement1 = 'SELECT * FROM Birds;'
statement2 = 'SELECT common_name FROM Birds ORDER BY common_name;'
statement3 = 'SELECT scientific_name, common_name FROM Birds ORDER BY scientific_name;'
statement4 = 'SELECT common_name, max_run_speed FROM Birds ORDER BY max_run_speed;'
statement5 = 'SELECT common_name, status FROM Birds;'
statement6 = "SELECT common_name, status FROM Birds WHERE status = 'Endangered';"

#Define functions
def print_information(statement):
    '''Prints information using the SQL statement entered'''
    with sqlite3.connect(DATABASE) as db:
        cursor = db.cursor()
        sql = statement
        cursor.execute(sql)
        results = cursor.fetchall()
        #print the results
        for bird in results:
            print(bird)

while True:
    user_input = input("\nWhat would you like to see? Input a number.\n1.All data\n2.Common names\n3.Common & Scientific names\n4.Run speeds\n5.Status\n6.Endangered birds\n7.Exit\n")
    if user_input == "1":
        print_information(statement1)
    elif user_input == "2":
        print_information(statement2)
    elif user_input == "3":
        print_information(statement3)
    elif user_input == "4":
        print_information(statement4)
    elif user_input == "5":
        print_information(statement5)
    elif user_input == "6":
        print_information(statement6)
    elif user_input == "7":
        break
