#!/usr/bin/env python3
from main import *

#This is the main menu from the ATM system
def atm(username, user_id):
    try:
        os.system("clear")
        #printing the main menu
        tprint("ATM")
        print("Welcome {} to the best ATM ever created!".format(username))
        print("""
            1 to deposit money
            2 to withdraw money
            3 to see how much money you have
            4 to deposit money to other client
            5 to quit or use CTRL+C
            """)
        #asking for the operation to do
        option = get_choice(["1","2","3","4","5"])
        option = int(option)
        #option = int(input("Write your option: "))
        if option == 1:
            deposit_money(username, user_id)
        elif option == 2:
            take_money_out(user_id)
        elif option == 3:
            actual_money = show_money(user_id)
            print("Your money is: ${}".format(actual_money))
            time.sleep(3)
            while True:

                option = input("You want to perform another operation in the best ATM ever created? y/N: ")
                if option.lower() == 'y':
                    time.sleep(3)
                    atm(username, user_id)
                elif option.lower() == 'n':
                    print("I'll see you later then!")
                    time.sleep(3)
                    exit()
                else:
                    print("i dont know that option")
                    time.sleep(3)
        elif option == 4:
            deposit_to_other_client(user_id, username)
        elif option == 5:
            print("\nbye\n")
            exit()
    except KeyboardInterrupt:
        print("\nbye\n")
    #waiting for errors
    except Exception as e:
        print(e)

#This function adds money to the user's account statement
def deposit_money(username, user_id):
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #create a cursor
        cursor = connection.cursor()
        try:
            #asking for the amount to add
            #and checking if is digit or not
            input_money = input("How much money do you want to deposit: ")
            if(input_money.isdigit()):
                input_money = int(input_money)
                #get to the actual amount of money in the account statement; using the show_money function
                actual_money = show_money(user_id)
                #then add the acual money and the input money to upload to the database
                input_money = input_money + actual_money

                #upload money using the input money and the username
                sql_sentence = "UPDATE users SET money = (?) where username = (?)"
                data = (input_money, username)

                print("Prosessing...") 
                time.sleep(3)

                cursor.execute(sql_sentence, data)
                connection.commit()
                print("Transaction has bee completed successfully!")
                time.sleep(2)
                while True:
                    option = input("You want to perform another operation in the best ATM ever created? y/N: ")
                    if option.lower() == 'y':
                        atm(username, user_id)
                    elif option.lower() == 'n':
                        print("I'll see you later then!")
                        time.sleep(3)
                        exit()
                    else:
                        print("I dont know that option!")
                        time.sleep(3)
            else:
                print("Here we're supposed to write an amount!")
                print("Try it again...")
                deposit_money(username, user_id)
            
        #waiting for errors
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        #waiting for errors from the database
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

#This function remains money from the database
def withdraw_money(user_id):
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #create a cursor
        cursor = connection.cursor()
        try:
            #asking to user how much money want to reamins
            #and checking if is digit or not
            output_money = input("How much money do you wish to withdraw?: ")
            if(output_money.isdigit()):
                output_money = int(output_money)
                #get to the actual amount of money in the account statement; using the show_money function
                actual_money = show_money(user_id)

                print("Prosessing...")
                time.sleep(3)
                #just checking that the user has enough money in the database.
                if actual_money < output_money:
                    print("You dont have enough money!")
                    exit()
                else:

                    #checking that the user has enough money in the database
                    actual_money = actual_money - output_money

                    #and then upload the data
                    sql_sentence = "UPDATE users SET money = (?)  where id = (?)"
                    data = (actual_money, user_id)
                    cursor.execute(sql_sentence, data)
                    connection.commit()
                    print("Your money now is: {}".format(actual_money))
            else:
                print("Here we're supposed to write an amount!")
                print("Try it again...")
                withdraw_money(user_id)
        #waiting for errors
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        #waiting for errors from the database
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

#This function just receive the user id to return the actual money from that user id
def show_money(user_id):
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #creating a cursor
        cursor = connection.cursor()
        try:
            sql_sentence = "SELECT money from users where id = (?)"
            data = (user_id, )
            cursor.execute(sql_sentence, data)
            connection.commit()
            actual_money = cursor.fetchone()
            #actual_money it is received in the form of tuple and then becomes to int
            actual_money = int(actual_money[0])
            return actual_money
        #waiting for errors
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        #waiting for errors from the database
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])

#This function remains to the user and then add that money to the specified user
def deposit_to_other_client(user_id, username):
    #connecting with the database sqlite
    with sqlite3.connect('data.db') as connection:
        #creating a cursor
        cursor = connection.cursor()
        try:
            #getting the username to transfer
            username_to = input("What is the username you want to transfer to?: ")
            cursor.execute("SELECT * from users WHERE username = (?)", (username_to,))

            #check if that user exist
            if cursor.fetchone() is not None:
                #ask how much money wants to remains
                #and checking if is digit or not
                money_to = input("How much money you want to transfer?: ")
                if(money_to.isdigit()):
                    money_to = int(money_to)
                    #get to the actual amount of money in the account statement; using the show_money function
                    actual_money = show_money(user_id)

                    #just checking that the user has enough money in the database.
                    if actual_money < money_to:
                        print("You dont have enough money to realize this operation!")
                        option = input("You want to retry this operation? y/N:")
                        if option.lower() == 'y':
                            deposit_to_other_client(user_id, username)
                        elif option.lower() == 'n':
                                print("I'll see you later then!")
                                exit()
                        else:
                            print("I dont know that option!")
                            deposit_to_other_client(user_id, username)
                    #if the user have enough money
                    else:
                        #last warning before transfer
                        #as if it were real money lol
                        while True:
                            option = input("Are you complete sure to transfer {} to {} y/N: ".format(money_to, username_to))
                            if option.lower() == "y":
                                print("Prosessing...")
                                time.sleep(3)
                                #getting the actual money from the usere to transfer
                                cursor.execute("SELECT money from users WHERE username = (?)", (username_to,))
                                connection.commit()
                                username_to_actual_money = cursor.fetchone()
                                #username_to_actual_money it is received in the form of tuple and then becomes to int
                                username_to_actual_money = int(username_to_actual_money[0])
                                #here remains the actual_money to the money to transfer
                                actual_money = actual_money - money_to
                                #here add the money to transfer to the user money to transfer
                                money_to = money_to + username_to_actual_money

                                #then updata the database using the new data
                                cursor.execute("UPDATE users SET money = (?) where username = (?)", (money_to, username_to))
                                connection.commit()
                                cursor.execute("UPDATE users SET money = (?) where username = (?)", (actual_money, username))
                                connection.commit()
                                print("Transaction has bee completed successfully!")
                                print("Your money is now: ${}".format(actual_money))
                            
                                while True: 
                                    option = input("You want to perform another operation in the best ATM ever created? y/N: ")
                                    if option.lower() == 'y':
                                        atm(username, user_id)
                                    elif option.lower() == 'n':
                                        print("I'll see you later then!")
                                        time.sleep(3)
                                        exit()
                                    else:
                                        print("I dont know that option!")
                                        time.sleep(3)

                            elif option.lower() == 'n':
                                #asking the user if he wants to enter the ATM, very obvious
                                print("Operation cancelled")
                                while True:

                                    option = input("Do you need to enter into the ATM again? y/N:")
                                    if option.lower() == 'y':
                                        atm(username, user_id)
                                    elif option.lower() == 'n':
                                        print("I'll see you later then!")
                                        exit()
                                    else:
                                        print("I dont know that option!")
                                        time.sleep(3)
                            else:
                                print("I dont know that option!")
                                time.sleep(3)
                else:
                    print("Here we're supposed to write an amount!")
                    print("Try it again...")
                    deposit_to_other_client(user_id, username)
            else:
                print("That user do not exist!")
                deposit_to_other_client(user_id, username)
        #waiting for errors
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("\nbye\n")
        #waiting for errors from the database
        except sqlite3.Error as e:
            print("An error occurred:", e.args[0])
