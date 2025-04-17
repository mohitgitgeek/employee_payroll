from flask import Flask, render_template, request, redirect, url_for, flash
import pickle
import os
import pathlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# --- Your Account class (unchanged except for input/output) ---
class Account:
    def __init__(self, accNo=0, name='', des='', add='', ba=0, da=0, ta=0, hra=0, pf=0, esi=0):
        self.accNo = accNo
        self.name = name
        self.des = des
        self.add = add
        self.ba = ba
        self.da = da
        self.ta = ta
        self.hra = hra
        self.gs = ba + da + ta + hra
        self.pf = pf
        self.esi = esi
        self.gd = pf + esi
        self.ns = self.gs - self.gd

    def to_dict(self):
        return self.__dict__

# --- Helper functions for file operations ---
def load_accounts():
    file = pathlib.Path("accounts.data")
    if file.exists():
        with open('accounts.data', 'rb') as infile:
            try:
                return pickle.load(infile)
            except EOFError:
                return []
    return []

def save_accounts(accounts):
    with open('accounts.data', 'wb') as outfile:
        pickle.dump(accounts, outfile)

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accounts')
def list_accounts():
    accounts = load_accounts()
    return render_template('list_accounts.html', accounts=accounts)

@app.route('/add', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        # Get form data
        accNo = int(request.form['accNo'])
        name = request.form['name']
        des = request.form['des']
        add = request.form['add']
        ba = int(request.form['ba'])
        da = int(request.form['da'])
        ta = int(request.form['ta'])
        hra = int(request.form['hra'])
        pf = int(request.form['pf'])
        esi = int(request.form['esi'])
        # Create and save account
        account = Account(accNo, name, des, add, ba, da, ta, hra, pf, esi)
        accounts = load_accounts()
        # Prevent duplicate account numbers
        if any(a.accNo == accNo for a in accounts):
            flash('Account number already exists!', 'danger')
            return redirect(url_for('add_account'))
        accounts.append(account)
        save_accounts(accounts)
        flash('Account created successfully!', 'success')
        return redirect(url_for('list_accounts'))
    return render_template('add_account.html')

@app.route('/delete/<int:accNo>')
def delete_account(accNo):
    accounts = load_accounts()
    accounts = [a for a in accounts if a.accNo != accNo]
    save_accounts(accounts)
    flash(f'Account {accNo} deleted.', 'info')
    return redirect(url_for('list_accounts'))

@app.route('/modify/<int:accNo>', methods=['GET', 'POST'])
def modify_account(accNo):
    accounts = load_accounts()
    account = next((a for a in accounts if a.accNo == accNo), None)
    if not account:
        flash('Account not found.', 'danger')
        return redirect(url_for('list_accounts'))
    if request.method == 'POST':
        # Update account details
        account.name = request.form['name']
        account.des = request.form['des']
        account.add = request.form['add']
        account.ba = int(request.form['ba'])
        account.da = int(request.form['da'])
        account.ta = int(request.form['ta'])
        account.hra = int(request.form['hra'])
        account.pf = int(request.form['pf'])
        account.esi = int(request.form['esi'])
        account.gs = account.ba + account.da + account.ta + account.hra
        account.gd = account.pf + account.esi
        account.ns = account.gs - account.gd
        save_accounts(accounts)
        flash('Account modified.', 'success')
        return redirect(url_for('list_accounts'))
    return render_template('modify_account.html', account=account)

if __name__ == '__main__':
    app.run(debug=True)

#OLD VERSION :
'''import pickle
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
'''
