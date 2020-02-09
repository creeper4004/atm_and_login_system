#!/usr/bin/env python3
from main import *

def atm(username, user_id):
    try:
        os.system("clear")
        tprint("ATM")
        print("Welcome {} to the best ATM ever created!".format(username))
        print("""
            1 to deposit money
            2 to to take money out
            3 to see how much money you have
            4 to deposit money to other client
            5 to quit or use CTRL+C
            """)
        option = int(input("Write your option: "))
        if option == 1:
            deposit_money(username, user_id)
        elif option == 2:
            take_money_out(user_id)
        elif option == 3:
            actual_money = show_money(user_id)
            print("Your money is: {}".format(actual_money))
        elif option == 4:
            deposit_to_other_client(user_id, username)
        elif option == 5:
            print("\nbye\n")
            exit()
    except KeyboardInterrupt:
        print("\nbye\n")
    except Exception as e:
        print(e)

def deposit_money(username, user_id):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:
            input_money = int(input("Who much money do you want to deposit: "))

            actual_money = show_money(user_id)

            input_money = input_money + actual_money

            sql_sentence = "UPDATE users SET money = (?) where username = (?)"
            data = (input_money, username)

            print("Prosessing...")
            time.sleep(3)

            cursor.execute(sql_sentence, data)
            connection.commit()
            #cursor.close()
            print("Transaction has bee completed successfully!")
            #connection.close()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

def take_money_out(user_id):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        user_id = int(user_id[0])
        try:
            output_money = int(input("How much money do you want to get: "))
            actual_money = show_money(user_id)

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
                #connection.close()

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

def show_money(user_id):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:
            sql_sentence = "SELECT money from users where id = (?)"
            data = (user_id, )
            cursor.execute(sql_sentence, data)
            connection.commit()
            actual_money = cursor.fetchone()
            actual_money = int(actual_money[0])
            #connection.close()
            return actual_money
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

def deposit_to_other_client(user_id, username):
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        try:
            username_to = input("What is the username you want to transfer to?: ")
            cursor.execute("SELECT * from users WHERE username = (?)", (username_to,))
            #connection.commit()

            if cursor.fetchone() is not None:
                money_to = int(input("How much money you want to transfer?: "))
                actual_money = show_money(user_id)

                if actual_money < money_to:
                    print("You dont have enough money to realize this operation!")
                    #connection.close()
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

                        cursor.execute("UPDATE users SET money = (?) where username = (?)", (money_to, username_to))
                        connection.commit()
                        cursor.execute("UPDATE users SET money = (?) where username = (?)", (actual_money, username))
                        connection.commit()
                        #connection.close()
                        print("Transaction has bee completed successfully!")
                        print("Your money is now: {}".format(actual_money))

                    else:
                        #connection.close()
                        exit()
            else:
                print("That user do not exist!")
                #connection.close()
                exit()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
