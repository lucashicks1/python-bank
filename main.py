# Import Library
import sqlite3
import time
import random
import datetime
import os


# DB variables
logindb = sqlite3.connect("login.db")
lgconn = logindb.cursor()
bankdb = sqlite3.connect("bank.db")
bankconn = bankdb.cursor()
transdb = sqlite3.connect("transactions.db")
transconn = transdb.cursor()
transferdb = sqlite3.connect("transfers.db")
transferconn = transferdb.cursor()


# DB Functions - This could be shortened down a lot, especially the create table commands
def logindbcreate():
    lgconn.execute(
        "CREATE TABLE LOGINDB(ID INTEGER PRIMARY KEY AUTOINCREMENT, USERNAME varchar(12) NOT NULL, PASSWORD varchar(25) NOT NULL)")


def logincreateentry(username, password):
    lgconn.execute(
        "INSERT INTO LOGINDB(USERNAME,PASSWORD) VALUES (?,?)", (username, password))
    logindb.commit()


def bankdbcreate():
    bankconn.execute(
        "CREATE TABLE BANKDB(ID INTEGER PRIMARY KEY,FNAME varchar(20),LNAME varchar(20),DOB TEXT,ACNUM varchar(8),EXDATE TEXT,BALANCE INTEGER,NICKNAME TEXT)")


def bankcreateentry(fname, lname, dob, acnum, exdate, nickname):
    bankconn.execute("INSERT INTO BANKDB(ID,FNAME,LNAME,DOB,ACNUM,EXDATE,BALANCE,NICKNAME) VALUES(?,?,?,?,?,?,?,?)",
                     (account.id, fname, lname, dob, acnum, exdate, 0, nickname))
    bankdb.commit()


def transactionsdbcreate():
    transconn.execute(
        "CREATE TABLE TRANSDB(ID INTEGER PRIMARY KEY AUTOINCREMENT,ACNUM,TDATE TEXT,TYPE TEXT,AMOUNT INTEGER)")


def transcreateentry(type, amount):
    now = datetime.datetime.now()
    transconn.execute("INSERT INTO TRANSDB(ACNUM,TDATE,TYPE,AMOUNT) VALUES(?,?,?,?)",
                      (account.acnum, currentdate(), type, amount))
    transdb.commit()


def transferdbcreate():
    transferconn.execute(
        "CREATE TABLE TRANSFERDB(ID INTEGER PRIMARY KEY AUTOINCREMENT,SENDER TEXT,RECEIVER TEXT,TDATE TEXT,STATUS TEXT,AMOUNT INTEGER,UNIQUEID INTEGER)")


def transfercreateentry(receiver, status, amount):
    now = datetime.datetime.now()
    transferconn.execute("INSERT INTO TRANSFERDB(SENDER,RECEIVER,TDATE,STATUS,AMOUNT,UNIQUEID) VALUES(?,?,?,?,?,?)",
                         (account.acnum, receiver, currentdate(), status, amount, uniqueid()))
    transferdb.commit()


# Initialisation functions
def dbcheck():
    try:
        bankdbcreate()
    except:
        pass
    try:
        logindbcreate()
    except:
        pass
    try:
        transactionsdbcreate()
    except:
        pass
    try:
        transferdbcreate()
    except:
        pass


dbcheck()

# Main Class


class account:
    def __init__(self):
        self.id = 0
        self.username = ''
        self.password = ''
        self.loggedin = 0
        self.fname = ''
        self.lname = ''
        self.nickname = ''
        self.dob = ''
        self.acnum = 0
        self.exdate = ''
        self.balance = 0

    # Refresh Class Method - Refreshes all details in the user's class - Used at the start of the program
    def refresh(self):
        bankconn.execute('SELECT * FROM BANKDB WHERE ID ="%s"' % (account.id))
        details = bankconn.fetchone()
        self.fname = details[1]
        self.lname = details[2]
        self.dob = details[3]
        self.acnum = details[4]
        self.exdate = details[5]
        self.balance = int(details[6])

    # Update Balance Method - Updates the user's balance - Used after transactions and transfers
    def upbalance(self, amount):
        self.balance += amount
        bankconn.execute('UPDATE BANKDB SET BALANCE = "%s" WHERE ACNUM = "%s"' % (
            account.balance, account.acnum))
        bankdb.commit()


# Declaring the user's class - Using account instead of self
account = account()

# General Use Functions
# ---------------------

# Checks if password has letter and number


def checklgd(s):
    l_flag = False
    n_flag = False
    for i in s:
        if i.isalpha():
            l_flag = True
        if i.isdigit():
            n_flag = True
    return l_flag and n_flag

# Generates an expiry date


def exgen():
    now = datetime.datetime.now()
    a = str(int(now.year+4))
    b = str(a+"-")
    c = str(b+str(now.month))
    if now.day < 10:
        day = str("0"+str(now.day))
    else:
        day = str(now.day)
    d = str(c+"-"+day)
    return d

# Gets the current date - Format - YYYY-MM-DD


def currentdate():
    now = datetime.datetime.now()
    a = str(now.year)+"-"+str(now.month)+"-"+str(now.day)
    # +"-"+str(now.hour)+"-"+str(now.minute) # Add this if you want YYYY-MM-DD-HH-MM instead of YYYY-MM-DD
    return a

# Generates a unique transfer ID(*****)


def uniqueid():
    while True:
        a = random.randint(00000, 99999)
        transferconn.execute(
            "SELECT * FROM TRANSFERDB WHERE UNIQUEID = '%s'" % (a))
        if transferconn.fetchone() is None:
            break
        else:
            pass
    return a

# Generates an account number - Also checks if number is already chosen


def ranacnum():
    while True:
        a = random.randint(000000, 999999)
        bankconn.execute('SELECT ACNUM FROM BANKDB WHERE ACNUM = "%s"' % (a))
        if lgconn.fetchone() is None:
            break
        else:
            pass
    return a

# Function that calculates the amount of spaces to organise data in a table


def spacer(num):
    result = ""
    for i in range(num):
        result = str(result) + " "
    return result

# This function confirms a money transfer


def confirm(id):
    transferconn.execute(
        'UPDATE TRANSFERDB SET STATUS = "%s" WHERE UNIQUEID = "%s"' % ("CONFIRMED", id))
    transferdb.commit()

# This function declines a money transfer


def declinechange(id):
    transferconn.execute(
        'UPDATE TRANSFERDB SET STATUS = "%s" WHERE UNIQUEID = "%s"' % ("DECLINED", id))
    transferdb.commit()

# Program functions
# ---------------------

# Login Function - Checks the login table for the entered data


def login():
    print("\nLogin to account\nType exit to leave")
    while True:
        try:
            username = input("Username:  ").lower()
            break
        except:
            print("Please enter correct values\n")
    if username == "exit":
        start()
    while True:
        try:
            password = input("Password:  ")
            break
        except:
            print("Please enter correct values\n")
    if password == "exit":
        start()
    lgconn.execute(
        'SELECT * FROM LOGINDB WHERE USERNAME ="%s" AND PASSWORD = "%s" ' % (username, password))
    if lgconn.fetchone() is not None:
        print("You are logged in!\n\nWelcome to Horizon Banking")
        account.loggedin = 1
        lgconn.execute(
            'SELECT * FROM LOGINDB WHERE USERNAME ="%s" AND PASSWORD = "%s" ' % (username, password))
        account.id = lgconn.fetchone()[0]
        switcher()
    else:
        print("Login Failed")
        login()

# Creates an entry into the login Database


def create():
    print("\nCreate an account")
    print("Type ? for more information or type exit to leave")
    help = "Username must be inbetween 5 and 12 characters\nPassword must be a mix of numbers and letters and inbetween 10 and 25 characters"
    while True:
        while True:
            while True:
                try:
                    username = input("Username:  ").lower()
                    break
                except:
                    print("Please enter correct values\n")
            lgconn.execute(
                'SELECT * FROM LOGINDB WHERE USERNAME ="%s"' % (username))
            if lgconn.fetchone() is None:
                break
            else:
                print("That username is already in use, please pick another one")
        if username != "?" and username != "exit":
            break
        elif username == "?":
            print(help)
        elif username == "exit":
            break
            start()
    while True:
        while True:
            while True:
                try:
                    password = input("Password:  ")
                    break
                except:
                    print("Please enter correct values\n")
            if password != "?" and password != "exit":
                break
            elif password == "?":
                print(help)
            elif password == "exit":
                start()

        if len(username) > 12 or len(username) < 5:
            print("Username must be at least 5 characters but not over 12!")
        elif len(password) > 25 or len(password) < 8 or checklgd(password) is False:
            print(
                "Password must be at least 8 characters but not over 25 and must contain a letter and number")
        else:
            break

    logincreateentry(username, password)
    print("\nYour account was successfully created!")
    start()

# Main Initialisation Interface - Used as a start to the program - Gives users options


def start():
    print("\nLogin Interface\n1)Login\n2)Create Account\n3)Exit")
    while True:
        try:
            choice = int(input("Menu Number:  "))
            break
        except:
            print("\nPlease enter correct number!\n")
    if choice == 1:
        login()
    elif choice == 2:
        create()
    elif choice == 3:
        pass
        print("\nGoodbye")
    else:
        print("That is not a menu number!\n")
        start()

# Asks the user for more information when they log-in to their account - Use this so the user can make multiple accounts easier


def begin():
    welcomestart = lgconn.execute(
        'SELECT * FROM LOGINDB WHERE ID ="%s"' % (account.id))
    print("Welcome", welcomestart.fetchone()[
          1]+",", "please give us some details to get started.")
    while True:
        try:
            fname = input("First Name:  ").strip()
            lname = input("Last Name:  ").strip()
            break
        except:
            print("Please enter correct values!\n")
    while True:
        if len(fname+lname) > 16:
            print("Since your name is too long, give us a 12 or less character nickname:")
            while True:
                nickname = input("Nickname:  ").strip()
                if len(nickname) < 12:
                    i = 1
                    break
                else:
                    print("Your nickname is too long\n")
            if i == 1:
                break
        else:
            nickname = ''
            break
    while True:
        while True:
            try:
                dob = input("Date of Birth(YYYY-MM-DD):  ").strip()
                datetime.datetime.strptime(dob, '%Y-%m-%d')
                break
            except:
                print("That is not a correct date")
        now = datetime.datetime.now()
        if (int(now.year) - int(dob[0:4])) >= 13:
            break
        else:
            print("You are not old enough! to make an account!\n")
    exdate = exgen()
    acnum = ranacnum()
    bankcreateentry(fname, lname, dob, acnum, exdate, nickname)
    account.refresh()
    print("\nWelcome to Horizon Banking!")
    program()

# Deposits money into the user's account - Also checks if the user has the required money


def deposit():
    print("\nDeposit Money")
    print("Type exit to leave")
    while True:
        while True:
            try:
                famount = input("Deposit Amount(AUSD)  $")
                break
            except:
                print("Please enter a correct value\n")
        try:
            amount = float(famount)
            break
        except:
            print("Please enter a correct value\n")
            pass
    if famount == "exit":
        program()
    if amount < 0:
        print("Amount must not be a negative number.")
        deposit()
    transcreateentry("Deposit", amount)
    account.upbalance(amount)
    print("\nYour money was deposited successfully")
    program()

# Function that is used to edit a user's information - Can be used in the view account section


def editinfo():
    print("Change your information\n\nPlease choose what information to change\n1)First Name\n2)Last Name\n3)DOB")
    while True:
        while True:
            i = 0
            while True:
                while True:
                    try:
                        choice = int(input("Please choose an index number:  "))
                        break
                    except:
                        print("That is not a number\n")
                if choice == 1:
                    while True:
                        try:
                            fname = input("First Name:  ").strip()
                            break
                        except:
                            print("That is not a correct answer\n")
                    if len(fname+account.lname) > 16:
                        while True:
                            print(
                                "Since your name is too long, give us a 12 or less character nickname:")
                            while True:
                                nickname = input("Nickname:  ").strip()
                                if len(nickname) < 12:
                                    i = 1
                                    break
                                else:
                                    print("Your nickname is too long\n")
                            if i == 1:
                                break
                        bankconn.execute(
                            "UPDATE BANKDB SET NICKNAME = '%s' WHERE ID = '%s'" % (nickname, account.id))
                        bankdb.commit()
                    bankconn.execute(
                        "UPDATE BANKDB SET FNAME = '%s' WHERE ID = '%s'" % (fname, account.id))
                    bankdb.commit()
                    break
                elif choice == 2:
                    while True:
                        try:
                            lname = input("Last Name:  ").strip()
                            break
                        except:
                            print("That is not a correct answer\n")
                    if len(lname+account.fname) > 16:
                        while True:
                            print(
                                "Since your name is too long, give us a 12 or less character nickname:")
                            while True:
                                nickname = input("Nickname:  ").strip()
                                if len(nickname) < 12:
                                    i = 1
                                    break
                                else:
                                    print("Your nickname is too long\n")
                            if i == 1:
                                break
                        bankconn.execute(
                            "UPDATE BANKDB SET NICKNAME = '%s' WHERE ID = '%s'" % (nickname, account.id))
                        bankdb.commit()
                    bankconn.execute(
                        "UPDATE BANKDB SET LNAME = '%s' WHERE ID = '%s'" % (lname, account.id))
                    bankdb.commit()
                    break
                elif choice == 3:
                    while True:
                        while True:
                            try:
                                dob = input(
                                    "Date of Birth(YYYY-MM-DD):  ").strip()
                                datetime.datetime.strptime(dob, '%Y-%m-%d')
                                break
                            except:
                                print("That is not a correct date")
                        now = datetime.datetime.now()
                        if (int(now.year) - int(dob[0:4])) >= 13:
                            break
                        else:
                            print("You are not old enough! to make an account!\n")
                    bankconn.execute(
                        "UPDATE BANKDB SET DOB = '%s' WHERE ID = '%s'" % (dob, account.id))
                    bankdb.commit()
                    break
                else:
                    print("That is not an option\n")
                account.refresh()
            while True:
                again = input(
                    "Do you want to change another thing? (yes or no):  ")
                if again == "no" or "n":
                    i = 1
                    break
                elif again == "yes" or "y":
                    pass
                else:
                    print("That is not an option")
            if i == 1:
                break
        if i == 1:
            break
    account.refresh()
    program()


# View account information function - Shows the full name, DOB, account number and current balance
def viewinfo():
    print("\n---- PERSONAL INFORMATION ----\n")
    print("Name:", account.fname, account.lname, "\nDate Of Birth:", account.dob,
          "\nAccount Number:", account.acnum, "\nBalance: $"+str(account.balance), "\n")
    while True:
        while True:
            try:
                choice = input(
                    ("Would you like to edit your information? (yes or no): ")).lower()
                break
            except:
                print("Your answer was incorrect\n")
        if choice == "yes" or choice == "y":
            editinfo()
            break
        elif choice == "n" or choice == "no":
            program()
            break
        else:
            print("You did not decide what you wanted to do!\n")

# Function that withdraws money from the user's account


def withdraw():
    print("\nWithdraw Money")
    print("Type exit to leave")
    while True:
        while True:
            while True:
                try:
                    famount = input("Deposit Amount(AUSD)  $")
                    break
                except:
                    print("Please enter a correct value\n")
            try:
                amount = float(famount)
                break
            except:
                print("Please enter a correct value\n")
                pass
        if amount > account.balance:
            print("You can't withdraw more money than you have in your account\n")
        else:
            break
    if famount == "exit":
        program()
    if amount < 0:
        print("Amount must not be a negative number.")
        deposit()
    transcreateentry("Withdraw", amount)
    account.upbalance(int(amount * (-1)))
    print("\nYour money was withdrawed successfully\n")
    program()

# Prints out all the previous transactions


def transactions():
    transconn.execute(
        'SELECT * FROM TRANSDB WHERE ACNUM = "%s"' % (account.acnum))
    details = transconn.fetchall()
    # print("Transaction Date\tType\tAmount")
    print("\n|DATE            |TYPE      |AMOUNT  |")
    for item in details:
        # print(i[2],"\t",i[3],"\t",i[4])
        print("|"+str(item[2])+spacer(16-len(item[2]))+"|"+item[3]+spacer(10 -
                                                                          len(item[3]))+"|$"+str(item[4])+spacer(7-len(str(item[4])))+"|")
    program()


# Allows the user to make a money transfer to another account - Only if the user knows the other's account number (6 digits long)
def transfer():
    print("\nMoney Transfer Page\n")
    i = 0
    while True:
        while True:
            while True:
                receiver = input(
                    "Enter the account number(Type 0 to exit) (******):  ")
                if receiver == "0":
                    i = 1
                    break
                else:
                    if len(receiver) != 6:
                        print("That is not 6 characters long!\n")
                    else:
                        if receiver == str(account.acnum):
                            print("You can't send money to yourself\n")
                        else:
                            break
            if i == 1:
                break
            else:
                bankconn.execute(
                    "SELECT * FROM BANKDB WHERE ACNUM = '%s' " % (receiver))
                data = bankconn.fetchall()
                if len(data) == 0:
                    print("That is not a valid account number!\n")
                else:
                    break
        if i == 1:
            break
        while True:
            while True:
                try:
                    amount = int(
                        input("What amount of money would you like to transfer: (Type 0 to exit) $"))
                    break
                except:
                    print("That is not a number!\n")
            if amount > account.balance:
                print("You don't have that amount of money to transfer\n")
            if amount == 0:
                program()
                break
            else:
                if amount > 9999999:
                    print("You can't send over 10 million dollars\n")
                else:
                    break
        print("\nYour money has been successfully transferred")
        transfercreateentry(receiver, "PENDING", amount)
        account.upbalance(int(amount * (-1)))
        program()
        break
    if i == 1:
        program()


def approve():
    while True:
        while True:
            try:
                chosenid = int(
                    input("Please enter the unique ID of the transfer (Type 0 to exit):  "))
                break
            except:
                print("That is not a number!\n")
        if chosenid == 0:
            program()
            break
        transferconn.execute(
            "SELECT * FROM TRANSFERDB WHERE UNIQUEID = '%s' AND RECEIVER = '%s'" % (chosenid, account.acnum))
        details = transferconn.fetchone()
        if len(details) == 0:
            print("That is not a number!")
        else:
            id = details[6]
            confirm(id)
            account.upbalance(details[5])
            print("\n$"+str(details[5]), 'has been added to your account.')
            program()


def decline():
    while True:
        while True:
            try:
                chosenid = int(
                    input("Please enter the unique ID of the transfer (Type 0 to exit):  "))
                break
            except:
                print("That is not a number!\n")
        if chosenid == 0:
            break
        transferconn.execute(
            "SELECT * FROM TRANSFERDB WHERE UNIQUEID = '%s' AND RECEIVER = '%s'" % (chosenid, account.acnum))
        details = transferconn.fetchone()
        if len(details) == 0:
            print("That is not a number!")
        else:
            id = details[6]
            declinechange(id)
            bankconn.execute(
                "SELECT * FROM BANKDB WHERE ACNUM = '%s'" % (details[1]))
            sender = bankconn.fetchone()
            balance = int(sender[6])+int(details[5])
            bankconn.execute(
                'UPDATE BANKDB SET BALANCE = "%s" WHERE ACNUM = "%s"' % (balance, sender[4]))
            bankdb.commit()
            print("\nThe money transfer has been declined")
            program()


def chose():
    while True:
        choice = input(
            "\nDo you want to approve or decline transfers (approve/decline)").lower()
        if choice == "approve":
            approve()
            break
        elif choice == "decline":
            decline()
            break
        else:
            print("That is not an option")


# Prints out all the current money transfers - Allows the user to accept money transfers from other users
def view():
    print("\nView and accept money transfers\n")
    transferconn.execute(
        "SELECT * FROM TRANSFERDB WHERE RECEIVER = '%s' AND STATUS = '%s'" % (account.acnum, "PENDING"))
    details = transferconn.fetchall()
    if len(details) == 0:
        print("You have no current money transfers")
        program()
    else:
        print("|ID      |NAME            |DATE            |AMOUNT  |")
        for item in details:
            bankconn.execute(
                "SELECT FNAME,LNAME,NICKNAME FROM BANKDB WHERE ACNUM = '%s'" % (item[1]))
            name = bankconn.fetchone()
            strname = name[0]+" "+name[1]
            if len(strname) > 16:
                strname = name[2]
            # print(i[6],"\t",strname,"\t",i[3],"\t","$"+str(i[5]))
            print("|"+str(item[6])+spacer(8-len(str(item[6])))+"|"+strname+spacer(16-len(
                strname))+"|"+item[3]+spacer(6)+"|$"+str(item[5])+spacer(7-len(str(item[5])))+"|")
        while True:
            choice = input(
                "\nDo you want to approve or decline any of these transactions? (yes or no): ").lower()
            if choice == "yes" or choice == "y":
                chose()
                break
            elif choice == "n" or choice == "no":
                program()
                break
            else:
                print("You did not decide what you wanted to do!\n")

# Switcher to check if the user has fully registered - If not it sends them to the begin function


def switcher():
    bankconn.execute('SELECT * FROM BANKDB WHERE ID = "%s" ' % (account.id))
    data = bankconn.fetchall()
    if len(data) == 0:
        begin()
    else:
        account.refresh()
        program()

# fail


def tfhistory():
    print("\nMoney Transfer History\n")
    transferconn.execute(
        "SELECT * FROM TRANSFERDB WHERE RECEIVER = '%s' AND NOT STATUS = '%s'" % (account.acnum, "PENDING"))
    details = transferconn.fetchall()
    if len(details) == 0:
        print("You have no current money transfers")
        program()
    else:
        print("|ID      |NAME            |DATE            |AMOUNT  |STATUS   |")
        for item in details:
            bankconn.execute(
                "SELECT FNAME,LNAME,NICKNAME FROM BANKDB WHERE ACNUM = '%s'" % (item[1]))
            name = bankconn.fetchone()
            strname = name[0]+" "+name[1]
            if len(strname) > 16:
                strname = name[2]
            # print(i[6],"\t",strname,"\t",i[3],"\t","$"+str(i[5]))
            print("|"+str(item[6])+spacer(8-len(str(item[6])))+"|"+strname+spacer(16-len(strname))+"|"+item[3] +
                  spacer(6)+"|$"+str(item[5])+spacer(7-len(str(item[5])))+"|"+item[4]+spacer(9-len(item[4]))+"|")
        while True:
            choice = input(
                "\nDo you want to approve any of these transactions? (yes or no): ").lower()
            if choice == "yes" or choice == "y":
                approve()
                break
            elif choice == "n" or choice == "no":
                program()
                break
            else:
                print("You did not decide what you wanted to do!\n")

# Simple menu system that allows the user to navigate through the program


def program():
    print("\n1)Deposit\n2)Withdraw\n3)View Cash Transactions\n4)Make a money transfer\n5)View or Approve pending transfers\n6)View Transfer History\n7)View Account Information\n8)Log-Out")
    while True:
        while True:
            try:
                choice = int(input("Menu Number:  "))
                break
            except:
                print("That is not a number!\n")
        if choice == 1:
            deposit()
            break
        elif choice == 2:
            withdraw()
            break
        elif choice == 3:
            transactions()
            break
        elif choice == 4:
            transfer()
            break
        elif choice == 5:
            view()
            break
        elif choice == 6:
            tfhistory()
            break
        elif choice == 7:
            viewinfo()
            break
        elif choice == 8:
            print("You are logged out   ")
            start()
            break
        else:
            print("That is not a menu number!\n")


# Code that runs when the program starts - Welcome is excluded from main program to remove unwanted clutter and to only welcome them at key points
print("Welcome to Horizon Banking")
start()
