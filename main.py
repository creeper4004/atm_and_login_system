#!/usr/bin/env python3
import os, getpass, sqlite3, hashlib, time
from atm import *
from art import *

#This is the main function, whats print the main menu and ask for the operation to do
def main():

    try:
        os.system("clear")
        #printing the main menu
        tprint("Login  system")
        print("Welcome to the best login system ever created!")
        print("""
            1 to login account.
            2 to create account.
            3 to delete your account.
            4 to exit or use CTRL+C
            """)
        #asking for the operation to do
        option = get_choice(["1","2","3","4"])
        option = int(option)
        #option = int(input("Write your option: "))
        if option == 1:
            login_account()
        elif option == 2:
            create_account()
        elif option == 3:
            delete_account()
        elif option == 4:
            print("\nbye\n")
            exit()
    except KeyboardInterrupt:
        print("\nbye\n")
    #waiting for errors
    except Exception as e:
        print(e)

#This function just receives and treats values correctly
def get_choice(choices):
  
    choice = input("Choose one of [%s]:" % ", ".join(choices))
    if not choice in choices:
        print('I dont know that option!')
        return get_choice(choices)
    return choice

#This function check that the user exists and then delete it, if so desired.
def delete_account():
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #creating a cursor
        cursor = connection.cursor()
        try:
            #getting for the username and password
            user = input("Enter the user name: ")
            passwd = getpass.getpass(prompt = "Password: ", stream = None)
            #encrypting and encoding password to save en the database
            crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
            sql_sentence = "SELECT * from users WHERE username = (?) AND password = (?)"
            data = (user, crypted_passwd)

            cursor.execute(sql_sentence, data)
            connection.commit()

            print("login...")
            time.sleep(3)

            #check if that account exist
            if cursor.fetchone() is not None:
                option = input("Are you complete sure to delete your account? y/N: ")
                if option.lower() == "y":

                    print("Deleting acount...")
                    time.sleep(3)

                    #delete account code
                    sql_sentence = "DELETE from users WHERE username = (?) AND password = (?)"
                    data = (user, crypted_passwd)
                    cursor.execute(sql_sentence, data)
                    connection.commit()
                    print("Acount deleted succefully!")

                elif option.lower() == "n":
                    print("I'll see you later then!")
                    exit()
                else:
                    print("I dont know that option.")
                    print("Try it again")
                    delete_account()
            else:
                print("Login failed")
        #waiting for errors
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        #waiting for errors from the database
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

#This function just receive the username and password to return the user id
def get_user_id(username, password):
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #creating a cursor
        cursor = connection.cursor()
        try:
            sql_sentence = "SELECT id from users WHERE username = (?) AND password = (?)"
            data = (username, password)
            cursor.execute(sql_sentence, data)
            connection.commit()

            user_id = cursor.fetchone()
            #user_id it is received in the form of tuple and then becomes to int
            user_id = int(user_id[0])
            #and then returns it
            return user_id
        except Exception as e:
            print(e)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
#This function just This function check that the user exists and then login into the ATM system
def login_account():
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #creating a cursor
        cursor = connection.cursor()
        MAX_ATTEMPTS = 3

        try:
            for attempts in range(MAX_ATTEMPTS):
                #getting for the username and password
                username = input("Enter the user name: ")
                passwd = getpass.getpass(prompt = "Password: ", stream = None)
                #encrypting and encoding password to save en the database
                crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
                #login code
                sql_sentence = "SELECT * from users WHERE username = (?) AND password = (?)"
                data = (username, crypted_passwd)

                cursor.execute(sql_sentence, data)
                connection.commit()
                print("login...")
                time.sleep(3)

                #check if that account exist
                if cursor.fetchone() is not None:
                    user_id = get_user_id(username, crypted_passwd)
                    attempts = MAX_ATTEMPTS
                    #put the attempts to the max attempts and then call to the atm function
                    atm(username, user_id)
                    break
                else:
                    print("Login failed!\nTry it again...")
        #waiting for errors
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        #waiting for errors from the database
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

#This function just create account
def create_account():
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #create a cursor
        cursor = connection.cursor()
        try:
            #getting for the username
            username = input("Enter the user name: ")
            cursor.execute("SELECT * from users WHERE username = (?)", (username,))
            connection.commit()

            #ask to the database if that username its already in use
            if cursor.fetchone() is not None:
                print("This name is already in use...")
                exit()
            else:
                #getting for the password 2 times to check if one of the passwords its wrong
                passwd = getpass.getpass(prompt = "Password: ", stream = None)
                retyped_passwd = getpass.getpass(prompt = "Re-type your password: ", stream = None)
                money = 0
                #checking the passwords match
                if retyped_passwd == passwd:
                    #encrypting and encoding password to save en the database
                    crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
                    sql_sentence = "INSERT INTO users(username, password, money) VALUES(?, ?, ?)"
                    data = (username, crypted_passwd, money)

                    print("Creating acount...")

                    time.sleep(3)
                    cursor.execute(sql_sentence, data)
                    connection.commit()
                    print("User created successfully")
                    #asking the user if he wants to enter the ATM, very obvious
                    option = input("Do you need to enter into the ATM? y/N:")
                    if option.lower() == 'y':
                        print("login...")
                        time.sleep(3)
                        #get to the user id using the get_user_id function
                        user_id = get_user_id(username, crypted_passwd)
                        atm(username, user_id)
                    elif option.lower() == 'n':
                        print("I'll see you later then!")
                        exit()
                    else:
                        print("I dont know that option!")
                        create_account()
                else:
                    print("The passwords do not match!")
                    print("Try it again! ")
                    create_account()
        #waiting for errors
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        #waiting for errors from the database
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])


if __name__=='__main__':
    main()
