import sys
import logging
import uuid
import mysql.connector
from datetime import date

# Create and configure logger
logging.basicConfig(filename="log_bank_file.log",
                    format=' % (asctime)s: % (levelname)s: % (name)s: % (message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

  
mydb= mysql.connector.connect(
            { "host": "localhost",
              "user": "######",
              "database": "bankingsys",
              "passwd": "######"	})  # use your password here
     

# define the class parent class Person:
class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __str__(self):
        outputs = """
                Person  first name: {}
                Person  address: {}
                """.format(self.first_name, self.address)
        return outputs

    def __repr__(self):
        rep = 'Person(' + self.first_name+','+self.address+')'
        return rep

# define a child class Customer:
class Customer(Person):
    def __init__(self, name, address, cust_num, bal=0):
        Person.__init__(self, name, address)
        self.cust_num = cust_num
        self.bal = bal

    def insert_customer(self):
        # method that creates a new customer.
        try:
            self.name = input("Enter the account holder name:" )
            self.address = input("Enter the account holder address: ")
            self.cust_num = uuid.uuid1()
            self.bal = input("Enter opening balance: ")

            sql = "INSERT INTO customer(name, address,cust_num ,bal) VALUES \
                    (%s, %s, %s, %s);"
        
            mydb.execute(sql, (self.name, self.address, self.cust_num, self.bal))
            print('New customer added successfully!\n\n')
        
        except TypeError as err:
            print(" invalid input")
            logger.error("Invalid input. An error message: {}".format(err))
        except ValueError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error(
                "Invalid input. An error message: {} in create_account()".format(err))
            # Back to main menu
            main_menu()
        except mysql.connector.errors.DataError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(
                "Invalid input. A debug message: {} from create_account()".format(err))
            # Back to main menu
            main_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(
                "Invalid input. A debug message: {} from create_account()".format(err))
            # Back to main menu
            main_menu()

    def show_details(self, cust_num):
        """
        method that returns account status and balance
        """

        try:
            acc_num = cust_num
            sql = "SELECT name, bal FROM customer WHERE cust_num = %s;" % self.cust_num
            mydb.execute(sql)
            self._result = mydb.fetchone()
            return self._result
        except SyntaxError:
            print("\n*************\nInvalid input! \nPlease Try Again!\n*************\n\n")
            # Log
            logger.error(f'An error message: SyntaxError in account_status()')
            main_menu()
        except ValueError:
            print("\n*************\nInvalid input! \nPlease Try Again! \n*************\n\n")
            # Log
            logger.error(f'An error message: ValueError in account_status()')
            main_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(f'A debug message: {err} from account_status()')
            main_menu()



#other child class Employee
class Employee(Person):
    #define a constant numberran
    MIN_SALARY = 30000
    # define the constructor
    def __init__(self, name, salary=MIN_SALARY):
        Person.__init__(self, name)
        if salary >= Employee.MIN_SALARY:
            self.salary = salary
        else:
            self.salary = Employee.MIN_SALARY


class BankAccount:
    # MODIFY to initialize a number attribute
    def __init__(self, number=0, balance=0):
        self.balance = balance
        self.number = number

    def withdraw(self, amount):
        if self.balance<amount:
            print("Please try again")
            logger.error("Invalid input: for the amount: '{}' . \
                        ".format(amount))
        else:
            self.balance -= amount
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

            

#other child class
class SavingsAccount(BankAccount):
    def __init__(self,number,balance,interest_rate=2):
        BankAccount.__init__(self, number, balance)
        self.interest_rate = interest_rate

    def compute_interest(self,n_periods=1):
        return self.balance*((1+self.interest_rate)**n_periods-1)


class CheckingAccount(BankAccount):
    def __init__(self, number, balance, limit=100):
        BankAccount.__init__(self, number, balance)
        self.limit = limit

    #customizing withdraw function from the parent class
    def withdraw(self, amount, fee=0):
        if fee<=self.limit:
            BankAccount.withdraw(self,amount-fee)
        else:
            BankAccount.withdraw(self,amount-self.limit)

class Services(BankAccount):
    def __init__(self, amount,apply_loan=True,apply_creditcard=False):
        self.amount = amount
        


def main_menu():
    while True:
        print("\n----- MAIN MENU ----- ")
        print("\n1.  Create Account")
        print("\n2.  Account Details")
        print('\n3.  Transaction Menu')
        print('\n4.  Close application')
        print('\n\n')
        try:
            option = int(input('Enter your option ...: '))

            if option == 1:
                Customer.insert_customer()
            elif option == 2:
                Customer.show_details()
            elif option == 3:
                transaction_menu()
            elif option == 4:
                print(
                    "\n*****************\nSee You Next Time!\n*****************\n")
                sys.exit(0)

        except TypeError as err:
            print(
                "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                # Log
            logger.error(
                "Invalid input: '{}' - ValueError message: {} from main_menu() at".format(option, err))
                # Back to main menu
            main_menu()
        except ValueError as err:
            print(
                "\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error(
                "Invalid input: '{}' - ValueError message: {} from main_menu() at".format(option, err))
            # Back to main menu
            main_menu()

def transaction_menu(self):
    """
    method that shows all the transactional options
    """

    while True:
        print("\n ----- TRANSACTION MENU ----- ")
        print("\n1.  Deposit Amount into Saving Account")
        print("\n2.  Deposit Amount into Checking Account")
        print('\n3.  Withdraw Amount into Saving Account')
        print('\n4.  Withdraw Amount into Checking Account')
        print('\n5.  Back to Main Menu')
        print('\n\n')
        try:
            option2 = int(input('Enter your option ...: '))
            if option2 == 1:
                try:
                    cust_num = input("Enter Account Number: ")
                    amount = input("Enter Amount: ")
                    today = date.today()
                    bal=SavingsAccount.deposit(amount)
                    sql1 = " UPDATE customer SET bal =%s \
                        WHERE cust_num = %s ;" % (bal, cust_num)
                    sql2 = " INSERT INTO transaction(date,amount,acc_type,type,cust_num) \
                        VALUES (%s, %s,'Saving','deposit', %s) ; "
                    mydb.execute(sql1)
                    mydb.execute(sql2, (today, amount, cust_num))
                    print("\n\nAmount Deposited!")

                except ValueError as err:
                    print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in deposit_amount()".format(self.amount, self.acc_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except TypeError as err:
                    print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in deposit_amount()".format(self.amount, self.acc_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except mysql.connector.errors.DataError as err:
                    print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
                    # Log
                    logger.debug(
                        "Invalid input. A debug message: {} from create_account()".format(err))
                    # Back to main menu
                    transaction_menu()


            elif option2 == 2:
                try:
                    cust_num = input("Enter Account Number: ")
                    amount = input("Enter Amount: ")
                    today = date.today()
                    bal = CheckingAccount.deposit(amount)
                    sql1 = " UPDATE customer SET bal =%s \
                        WHERE cust_num = %s ;" % (bal, cust_num)
                    sql2 = " INSERT INTO transaction(date,amount,acc_type,type,cust_num) \
                        VALUES (%s, %s,'Checking','deposit', %s) ; "
                    mydb.execute(sql1)
                    mydb.execute(sql2, (today, amount, cust_num))
                    print("\n\nAmount Deposited!")

                except ValueError as err:
                    print(
                        "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in deposit_amount()".format(self.amount, self.acc_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except TypeError as err:
                    print(
                        "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in deposit_amount()".format(amount, cust_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except mysql.connector.errors.DataError as err:
                    print(
                        "\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
                    # Log
                    logger.debug(
                        "Invalid input. A debug message: {} from create_account()".format(err))
                    # Back to main menu
                    transaction_menu()
            elif option2 == 3:
                try:
                    cust_num = input("Enter Account Number: ")
                    amount = input("Enter Amount: ")
                    today = date.today()
                    bal = SavingsAccount.withdraw(amount)
                    sql1 = " UPDATE customer SET bal =%s \
                        WHERE cust_num = %s ;" % (bal, cust_num)
                    sql2 = " INSERT INTO transaction(date,amount,acc_type,type,cust_num) \
                        VALUES (%s, %s,'Saving','withdraw', %s) ; "
                    mydb.execute(sql1)
                    mydb.execute(sql2, (today, amount, cust_num))
                    print("\n\nAmount Withdraw!")

                except ValueError as err:
                    print(
                        "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in withdraw_amount()".format(amount, cust_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except TypeError as err:
                    print(
                        "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in withdraw_amount()".format(amount, cust_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except mysql.connector.errors.DataError as err:
                    print(
                        "\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
                    # Log
                    logger.debug(
                        "Invalid input. A debug message: {} from create_account()".format(err))
                    # Back to main menu
                    transaction_menu()

            elif option2 == 4:
                try:
                    cust_num = input("Enter Account Number: ")
                    amount = input("Enter Amount: ")
                    today = date.today()
                    bal = CheckingAccount.withdraw(amount)
                    sql1 = " UPDATE customer SET bal =%s \
                        WHERE cust_num = %s ;" % (bal, cust_num)
                    sql2 = " INSERT INTO transaction(date,amount,acc_type,type,cust_num) \
                        VALUES (%s, %s,'Checking','withdraw', %s) ; "
                    mydb.execute(sql1)
                    mydb.execute(sql2, (today, amount, cust_num))
                    print("\n\nAmount Withdraw!")

                except ValueError as err:
                    print(
                        "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in withdraw_amount()".format(amount, cust_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except TypeError as err:
                    print(
                        "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                    # Log
                    logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in withdraw_amount()".format(amount, cust_num, err))
                    # Back to transaction menu
                    transaction_menu()
                except mysql.connector.errors.DataError as err:
                    print(
                        "\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
                    # Log
                    logger.debug(
                        "Invalid input. A debug message: {} from create_account()".format(err))
                    # Back to main menu
                    transaction_menu()

            elif option2 == 5:
                main_menu()

                    

        except TypeError as err:
            print(
                 "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                # Log
            logger.error(
                 "Invalid input: '{}' - ValueError message: {} from transaction_menu()".format(option2, err))
                # Back to transaction menu
            transaction_menu()
        except ValueError as err:
            print(
                    "\n*************\nInvalid input!\n*************\nPlease try again!\n")
                # Log
            logger.error(
                    "Invalid input: '{}' - ValueError message: {} from transaction_menu()".format(option2, err))
                # Back to transaction menu
            transaction_menu()

    """
    user=input("Please Enter your Name:")
    print("Welcome {} in our Bank Site".format(user))
    type_account=input("Press 1 to open Savings Account, Press 2 to open Checking Account:")

    if int(type_account)==1:
        new_saving=SavingsAccount(1,100)

    elif int(type_account)==2:
        new_checking=CheckingAccount()

    else:
        print("this is not right value")

    while True:
        type_proccess=input("Press 1 to deposit money, Press 2 to withdraw money, Press 3 to show balance:")
        if int(type_proccess)==1 and int(type_account)==1:
            amount=int(input('Enter the amount to deposit:'))
            new_saving.deposit(amount)

        elif int(type_proccess)==2 and int(type_account)==1:
            amount=int(input('Enter the amount to withdraw:'))
            new_saving.withdraw(amount)

        elif int(type_proccess)==1 and int(type_account)==2:
            amount=int(input('Enter the amount to deposit:'))
            new_checking.deposit(amount)

        elif int(type_proccess)==2 and int(type_account)==2:
            amount=int(input('Enter the amount to deposit:'))
            new_checking.withdraw(amount)

        elif int(type_proccess)==3 :
            print(new_saving.balance)

        elif int(type_proccess)==4 :
            sys.exit()

        else:
            print("this is not right value")
            

        end_proccess=input("Press 1 to go back to the main menu, Press 2 to exit:")
        if int(end_proccess)==1:
            continue
        elif int(end_proccess)==2:
            sys.exit()
        else:
            print("this is not right value")
    """

if __name__ == "__main__":
    main_menu()
