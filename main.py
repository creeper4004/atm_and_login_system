#!/usr/bin/env python3
import os, getpass, sqlite3, hashlib, time

def main():

    try:
        print("""WELCOME TO THE BEST LOGIN SYSTEM EVER CREATED!
            1 to login account.
            2 to create account.
            3 to delete your account.
            4 to exit or use CTRL+C""")
        option = int(input())
        if option == 1:
            login_account()
        elif option == 2:
            create_account()
        elif option == 3:
            delete_account()
        elif option == 4:
            print("bye")
            exit()
    except KeyboardInterrupt:
        print("bye")


def delete_account():

    try:

        user = input("Enter the user name: ")
        passwd = getpass.getpass(prompt = "Password: ", stream = None)
        crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
        sql_sentence = "SELECT * from cred WHERE username = ? AND password = ?"
        data = (user, crypted_passwd)

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(sql_sentence, data)
        connection.commit()

        print("login...")
        time.sleep(3)

        if cursor.fetchone() is not None:
            option = input("Are you complete sure to delete yout account? y/N: ")
            if option.lower() == "y":
                
                print("Deleting acount...")
                time.sleep(3)

                sql_sentence = "DELETE from cred WHERE username = ? AND password = ?"
                data = (user, crypted_passwd)
                cursor.execute(sql_sentence, data)
                connection.commit()
                print("Acount deleted succefully!")

            elif option.lower() == "n":
                print("Then you are welcome.")
            else: 
                print("I dont know that option.")
                print("Try it again")
                delete_account()
        else:
            print("Login failed")

        cursor.close()
        connection.close()
        
    except KeyboardInterrupt:
        print("bye")

def login_account():
    
    trys = 0
    
    try:
        while trys != 3:
            user = input("Enter the user name: ")
            
            passwd = getpass.getpass(prompt = "Password: ", stream = None)
            crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
            sql_sentence = "SELECT * from cred WHERE username = ? AND password = ?"
            data = (user, crypted_passwd)

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            cursor.execute(sql_sentence, data)
            connection.commit()

            print("login...")
            time.sleep(3)

            if cursor.fetchone() is not None:
                print("Welcome")
                trys = 3
            else:
                print("Login failed!\nTry it again...")
                trys += 1

            cursor.close()
            connection.close()
        
    except KeyboardInterrupt:
        print("bye")
 
def create_account():

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:

            user = input("Enter the user name: ") 
            cursor.execute("SELECT * from cred WHERE username = (?)", (user,))
            connection.commit()
        
            if cursor.fetchone() is not None:
                print("This name is already in use...")
                cursor.close()
                #connection.close()
                #exit()
            else:
                passwd = getpass.getpass(prompt = "Password: ", stream = None)
                retyped_passwd = getpass.getpass(prompt = "Re-type your password: ", stream = None)
                if retyped_passwd == passwd:

                    crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
                    sql_sentence = "INSERT INTO cred(username, password) VALUES(?, ?)"
                    data = (user, crypted_passwd)

                    print("Creating acount...")

                    time.sleep(3)

                    #connection = sqlite3.connect('data.db')
                    #cursor = connection.cursor() 
                    cursor.execute(sql_sentence, data)
                    connection.commit()
                    cursor.close()
                    #connection.close()
                    print("User created successfully")
                else:
                    print("The passwords do not match!")
                    cursor.close()
                    #connection.close()
                    #exit()
        except KeyboardInterrupt:
            print("bye")
            #connection.rollback()
        except:
            connection.rollback()
        #finally:
            #cursor.close()
            #connection.close()

if __name__=='__main__':
    main()
