#!/usr/bin/env python3
import os, getpass, sqlite3, hashlib, time

def main():

    try:
        print("""Welcom to the best login system ever created!
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
        else:
            print("I dont know that option!")
            exit()
    except KeyboardInterrupt:
        print("bye")


def delete_account():

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:

            user = input("Enter the user name: ")
            passwd = getpass.getpass(prompt = "Password: ", stream = None)
            crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
            sql_sentence = "SELECT * from users WHERE username = ? AND password = ?"
            data = (user, crypted_passwd)

            #connection = sqlite3.connect('data.db')
            #cursor = connection.cursor()
            cursor.execute(sql_sentence, data)
            connection.commit()

            print("login...")
            time.sleep(3)

            if cursor.fetchone() is not None:
                option = input("Are you complete sure to delete yout account? y/N: ")
                if option.lower() == "y":

                    print("Deleting acount...")
                    time.sleep(3)

                    sql_sentence = "DELETE from users WHERE username = ? AND password = ?"
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
        except:
            connection.rollback()
def get_user_id(user, password):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        sql_sentence = "SELECT id from users WHERE username = ? AND password = ?"
        data = (user, password)
        cursor.execute(sql_sentence, data)
        connection.commit()
        user_id = cursor.fetchone()
        return user_id

def login_account():

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        MAX_ATTEMPTS = 3

        try:
            #print("is this shit happen?")
            #while attempts >= 3:
            for attempts in range(MAX_ATTEMPTS):
                user = input("Enter the user name: ")

                passwd = getpass.getpass(prompt = "Password: ", stream = None)
                crypted_passwd = hashlib.sha256(passwd.encode('utf-8')).hexdigest()
                #cursor.execute("SELECT id from users where ucursor.execute("SELECT money from users WHERE username = (?)", (username_to,))sername = ? AND password = ?", (user, crypted_passwd))
                #user_id = cursor.fetchone()
                #print(user_id)
                sql_sentence = "SELECT * from users WHERE username = ? AND password = ?"
                data = (user, crypted_passwd)

                cursor.execute(sql_sentence, data)
                connection.commit()
                print("login...")
                #time.sleep(3)

                if cursor.fetchone() is not None:
                    print("Welcome")
                    user_id = get_user_id(user, crypted_passwd)
                    #print(user_id)
                    attempts = MAX_ATTEMPTS
                    atm(user, user_id)
                    break
                else:
                    print("Login failed!\nTry it again...")
                    #attempts += 1

                #cursor.close()
                #connection.close()

        except KeyboardInterrupt:
            print("bye")
        except:
            connection.rollback()
        finally:
            pass
            #cursor.close()
            #connection.close()

def create_account():

    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:

            user = input("Enter the user name: ")
            cursor.execute("SELECT * from users WHERE username = (?)", (user,))
            connection.commit()

            if cursor.fetchone() is not None:
                print("This name is already in use...")
                cursor.close()
                #connection.close()
                #exit()
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
                    #connection.close()
                    print("User created successfully")
                else:
                    print("The passwords do not match!")
                    cursor.close()
                    #connection.close()
                    #exit()
        except KeyboardInterrupt:
            print("bye")
        except:
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

def atm(username, user_id):
    try:
        os.system("clear")
        print("Welcome {} to the best ATM ever created!".format(username))
        print("""
            1 to deposit money
            2 to to take money out
            3 to see how much money you have
            4 to deposit money to other client
            5 to quit or use CTRL+C
            """)
        option = int(input())
        if option == 1:
            deposit_money(username, user_id)
        elif option == 2:cursor.execute("SELECT money from users WHERE username = (?)", (username_to,))
            get_money(user_id)
        elif option == 3:
            show_money(user_id)
        elif option == 4:
            deposit_to_other_client(user_id, username)
        elif option == 5:
            print("bye")
            exit()
    except KeyboardInterrupt:
        print("\nbye\n")

def deposit_money(username, user_id):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:
            input_money = int(input("Who many money you go to deposit: "))

            cursor.execute("SELECT money from users where id = (?)", user_id)
            connection.commit()
            actual_money = cursor.fetchone()
            actual_money = int(actual_money[0])

            input_money = input_money + actual_money

            sql_sentence = "UPDATE users SET money = ? where username = ?"
            data = (input_money, username)

            print("Prosessing...")
            time.sleep(3)

            cursor.execute(sql_sentence, data)
            connection.commit()
            #cursor.close()

            print("Transaction has bee completed succefully!")
        except KeyboardInterrupt:
            print("\nbye\n")
        except:
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

def get_money(user_id):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        #user_id = _user_id[0]
        try:
            output_money = int(input("Who many money yo go to extract: "))
            sql_sentence = "SELECT money from users where id = (?)"
            data = user_id
            #print(user_id)
            cursor.execute(sql_sentence, data)
            connection.commit()
            actual_money = cursor.fetchone()
            actual_money = int(actual_money[0])
            user_id = int(user_id[0])
            #actual_money = _actual_money[0]
            #print(actual_money)
            print("Prosessing...")
            time.sleep(3)
            if actual_money < output_money:
                print("You dont have enough money!")
                exit()
            else:

                #print("some")
                actual_money = actual_money - output_money

                #print(actual_money[0])
                sql_sentence = "UPDATE users SET money = (?)  where id = (?)"
                data = (actual_money, user_id)

                cursor.execute(sql_sentence, data)
                connection.commit()
                print("Your money now is: {}".format(actual_money))


        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except:
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

def show_money(user_id):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:
            sql_sentence = "SELECT money from users where id = (?)"
            data = user_id
            cursor.execute(sql_sentence, data)
            connection.commit()
            actual_money = cursor.fetchone()
            actual_money = int(actual_money[0])
            print("Your money is: {}".format(actual_money))
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except:
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

def deposit_to_other_client(user_id, username):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:
            username_to = input("What is the username you want to transfer to?: ")
            cursor.execute("SELECT * from users WHERE username = (?)", (username_to,))
            connection.commit()

            if cursor.fetchone() is not None:
                money_to = int(input("How much money you want to transfer?: "))
                sql_sentence = "SELECT money from users where id = (?)"
                data = user_id
                cursor.execute(sql_sentence, data)
                connection.commit()
                actual_money = cursor.fetchone()
                actual_money = int(actual_money[0])

                if actual_money < money_to:
                    print("You dont have enough money to realize this operation!")
                    exit()
                else:
                    option = input("Are you complete sure to transfer {} to {} y/N: ".format(money_to, username_to))
                    if option.lower() == "y":
                        print("Prosessing...")
                        time.sleep(3)
                        cursor.execute("SELECT money from users WHERE username = (?)", (username_to,))
                        connection.commit()
                        username_to_actual_money = cursor.fetchone()
                        username_to_actual_money = int(username_to_actual_money[0])
                        actual_money = actual_money - money_to
                        money_to = money_to + username_to_actual_money

                        cursor.execute("UPDATE users SET money = ? where username = ?", (money_to, username_to))
                        connection.commit()
                        cursor.execute("UPDATE users SET money = ? where username = ?", (actual_money, username))
                        connection.commit()

                    else:
                        exit()
            else:
                print("That user do not exist!")
                exit()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except:
            connection.rollback()
        finally:
            cursor.close()
            connection.close()


if __name__=='__main__':
    main()
