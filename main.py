#!/usr/bin/env python3
import os, getpass, sqlite3, hashlib, time
from atm import *

def main():

    try:
        #os.system("clear")
        print("""Welcom to the best login system ever created!
            1 to login account.
            2 to create account.
            3 to delete your account.
            4 to exit or use CTRL+C""")
        option = int(input("Write your option: "))
        if option == 1:
            login_account()
        elif option == 2:
            create_account()
        elif option == 3:
            delete_account()
        elif option == 4:
            print("\nbye\n")
            exit()
        else:
            print("I dont know that option!")
            exit()
    except KeyboardInterrupt:
        print("\nbye\n")
    except Exception as e:
        print(e)


def delete_account():

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:

            user = input("Enter the user name: ")
            passwd = getpass.getpass(prompt = "Password: ", stream = None)
            crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
            sql_sentence = "SELECT * from users WHERE username = (?) AND password = (?)"
            data = (user, crypted_passwd)

            #connection = sqlite3.connect('data.db')
            #cursor = connection.cursor()
            cursor.execute(sql_sentence, data)
            connection.commit()

            print("login...")
            time.sleep(3)

            if cursor.fetchone() is not None:
                option = input("Are you complete sure to delete your account? y/N: ")
                if option.lower() == "y":

                    print("Deleting acount...")
                    time.sleep(3)

                    sql_sentence = "DELETE from users WHERE username = (?) AND password = (?)"
                    data = (user, crypted_passwd)
                    cursor.execute(sql_sentence, data)
                    connection.commit()
                    print("Acount deleted succefully!")
                    #connection.close()

                elif option.lower() == "n":
                    print("Then you are welcome.")
                    #connection.close()
                else:
                    print("I dont know that option.")
                    print("Try it again")
                    delete_account()
                    #connection.close()
            else:
                print("Login failed")
                #connection.close()

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

def get_user_id(username, password):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:
            sql_sentence = "SELECT id from users WHERE username = (?) AND password = (?)"
            data = (username, password)
            cursor.execute(sql_sentence, data)
            connection.commit()

            user_id = cursor.fetchone()
            user_id = int(user_id[0])
            #print(user_id)
            #connection.close()
            return user_id
        except Exception as e:
            print(e)
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

def login_account():

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        MAX_ATTEMPTS = 3

        try:
            #print("is this shit happen?")
            #while attempts >= 3:
            for attempts in range(MAX_ATTEMPTS):
                username = input("Enter the user name: ")

                passwd = getpass.getpass(prompt = "Password: ", stream = None)
                crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
                #cursor.execute("SELECT id from users where ucursor.execute("SELECT money from users WHERE username = (?)", (username_to,))sername = ? AND password = ?", (user, crypted_passwd))
                #user_id = cursor.fetchone()
                #print(user_id)
                sql_sentence = "SELECT * from users WHERE username = (?) AND password = (?)"
                data = (username, crypted_passwd)

                cursor.execute(sql_sentence, data)
                connection.commit()
                print("login...")
                time.sleep(3)

                if cursor.fetchone() is not None:
                    #print("Welcome")
                    user_id = get_user_id(username, crypted_passwd)
                    #print(user_id)
                    attempts = MAX_ATTEMPTS
                    #connection.close()
                    atm(username, user_id)
                    break
                else:
                    print("Login failed!\nTry it again...")

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

def create_account():

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:

            user = input("Enter the user name: ")
            cursor.execute("SELECT * from users WHERE username = (?)", (user,))
            connection.commit()

            if cursor.fetchone() is not None:
                print("This name is already in use...")
                #cursor.close()
                #connection.close()
                exit()
            else:
                passwd = getpass.getpass(prompt = "Password: ", stream = None)
                retyped_passwd = getpass.getpass(prompt = "Re-type your password: ", stream = None)
                money = 0
                if retyped_passwd == passwd:

                    crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
                    sql_sentence = "INSERT INTO users(username, password, money) VALUES(?, ?, ?)"
                    data = (user, crypted_passwd, money)

                    print("Creating acount...")

                    time.sleep(3)

                    #connection = sqlite3.connect('data.db')
                    #cursor = connection.cursor()
                    cursor.execute(sql_sentence, data)
                    connection.commit()
                    #cursor.close()
                    print("User created successfully")
                    #connection.close()
                else:
                    print("The passwords do not match!")
                    #cursor.close()
                    #connection.close()
                    #exit()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])


if __name__=='__main__':
    main()
