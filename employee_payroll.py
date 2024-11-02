import pickle
import os
import pathlib

class Account:
    def __init__(self):
        self.accNo = 0
        self.name = ''
        self.des = ''
        self.add = ''
        self.ba = 0
        self.da = 0
        self.ta = 0
        self.hra = 0
        self.pf = 0
        self.esi = 0
        self.gs = 0
        self.gd = 0
        self.ns = 0
    
    def createAccount(self):
        self.accNo = int(input("Enter the account no : "))
        self.name = input("Enter the employer's name : ")
        self.des = input("Enter the employer's designation: ")
        self.add = input("Enter the employer's address: ")
        self.ba = int(input("Enter basic salary of employee (in rupees): "))
        self.da = int(input("Enter dearness allowance of the employee (in rupees): "))
        self.ta = int(input("Enter travelling allowance of the employee(in rupees): "))
        self.hra = int(input("Enter house rent allowance of the employee (in rupees): "))
        self.gs = self.ba + self.da + self.ta + self.hra
        self.pf = int(input("Enter provident fund of the employee (in rupees): "))
        self.esi = int(input("Enter employee state insurance of the employee(in rupees): "))
        self.gd = self.pf + self.esi
        self.ns = self.gs - self.gd
        print("\n\n\nPayroll information stored.\n")

    def showAccount(self):
        print("Account Number : ", self.accNo)
        print("Account Holder Name : ", self.name)
        print("Designation :", self.des)
        print("Address:", self.add)
        print("Basic Salary: ", self.ba)
        print("Dearness Allowance: ", self.da)
        print("Travelling Allowance: ", self.ta)
        print("House Rent Allowance: ", self.hra)
        print("Gross Salary:", self.gs)
        print("Provident fund: ", self.pf)
        print("Employee state insurance : ", self.esi)
        print("Gross Deduction", self.gd)
        print("Net salary", self.ns)
        
def intro():
    print("\t\t\t\t**************************")
    print("\t\t\t\tPAYROLL MANAGEMENT SYSTEM")
    print("\t\t\t\t**************************")

def writeAccount():
    account = Account()
    account.createAccount()
    writeAccountsFile(account)

def displayAll():
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        try:
            mylist = pickle.load(infile)
            print()
            for item in mylist:
                item.showAccount()
                print("\n----------------------\n")
        except EOFError:
            print("No records to display")
        infile.close()
    else:
        print("No records to display")

def deleteAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        try:
            oldlist = pickle.load(infile)
        except EOFError:
            oldlist = []
        infile.close()
        newlist = [item for item in oldlist if item.accNo != num]
        os.remove('accounts.data')
        with open('accounts.data', 'wb') as outfile:
            pickle.dump(newlist, outfile)
        print(f"Account number {num} has been deleted.")
    else:
        print("No records to delete")

def modifyAccount(num):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        try:
            oldlist = pickle.load(infile)
        except EOFError:
            oldlist = []
        infile.close()
        os.remove('accounts.data')
        for item in oldlist:
            if item.accNo == num:
                print("Modifying account details for account number:", num)
                item.createAccount()  # re-uses the input method to modify details
        with open('accounts.data', 'wb') as outfile:
            pickle.dump(oldlist, outfile)
        print(f"Account number {num} has been modified.")
    else:
        print("No records to modify")

def writeAccountsFile(account):
    file = pathlib.Path("accounts.data")
    if file.exists():
        infile = open('accounts.data', 'rb')
        try:
            oldlist = pickle.load(infile)
        except EOFError:
            oldlist = []
        oldlist.append(account)
        infile.close()
    else:
        oldlist = [account]
    with open('accounts.data', 'wb') as outfile:
        pickle.dump(oldlist, outfile)

# Start of the program
ch = ''
intro()

while ch != '5':
    print("\tMAIN MENU")
    print("\t1. NEW ACCOUNT")
    print("\t2. ALL ACCOUNT HOLDER LIST")
    print("\t3. CLOSE AN ACCOUNT")
    print("\t4. MODIFY AN ACCOUNT")
    print("\t5. EXIT")
    ch = input("\tSelect Your Option (1-5):") 
    
    if ch == '1': 
        writeAccount()
    elif ch == '2':
        displayAll()
    elif ch == '3':
        num = int(input("\tEnter the account No. to delete: "))
        deleteAccount(num)
    elif ch == '4':
        num = int(input("\tEnter the account No. to modify: "))
        modifyAccount(num)
    elif ch == '5':
        print("\tThanks for using Payroll Management System")
        break
    else:
        print("Invalid choice.")
