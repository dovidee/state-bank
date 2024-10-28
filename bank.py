from dataclasses import dataclass
import uuid
import threading
import re

@dataclass
class CashAccount:
    id: str  
    balance: float

@dataclass
class CardAccount:
    id: str  
    balance: float

@dataclass
class Customer:
    name: str
    cash_acct: CashAccount
    card_acct: CardAccount

def generate_uuid():
    global random_uuid
    while True:
        random_uuid = str(uuid.uuid4())

def is_valid_uuid(uuid_str):
    uuid_regex = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$')
    return bool(uuid_regex.match(uuid_str))

uuid_thread = threading.Thread(target=generate_uuid, daemon=True)
uuid_thread.start()

def create_cash_acct(init_bal: float) -> CashAccount:
    global random_uuid
    new_acct = CashAccount(random_uuid, init_bal)
    return new_acct

def create_card_acct(init_bal: float) -> CardAccount:
    global random_uuid
    new_acct = CardAccount(random_uuid, init_bal)
    return new_acct

def create_cus(name: str, cash_acct: CashAccount, card_acct: CardAccount) -> Customer:
    new_cust = Customer(name, cash_acct, card_acct)
    return new_cust

def bank_help():
    print("State-Bank")
    print("\n0. Help")
    print("\n1. Create new account")
    print("2. Delete account")
    print("3. Show all accounts")
    print("4. Transfer money between card accounts")
    print("5. Deposit cash to card")
    print("6. Withdraw cash from card")

beginner = True
cus_list = []

def find_account_by_uuid(uuid_str):
    for user in cus_list:
        if user.cash_acct.id == uuid_str or user.card_acct.id == uuid_str:
            return user
    return None

def transfer_money(from_uuid, to_uuid, amount):
    from_user = find_account_by_uuid(from_uuid)
    to_user = find_account_by_uuid(to_uuid)
    
    if from_user and to_user and isinstance(from_user.card_acct, CardAccount) and isinstance(to_user.card_acct, CardAccount):
        if from_user.card_acct.balance >= amount:
            from_user.card_acct.balance -= amount
            to_user.card_acct.balance += amount
            print(f"Transferred ${amount:.2f} from {from_user.name}'s card to {to_user.name}'s card.")
        else:
            print("Insufficient funds in card account.")
    else:
        print("One or both accounts not found or not card accounts.")

def deposit_cash_to_card(customer, amount):
    if customer.cash_acct.balance >= amount:
        customer.cash_acct.balance -= amount
        customer.card_acct.balance += amount
        print(f"Deposited ${amount:.2f} from cash to {customer.name}'s card.")
    else:
        print("Insufficient funds in cash account.")

def withdraw_cash_from_card(customer, amount):
    if customer.card_acct.balance >= amount:
        customer.card_acct.balance -= amount
        customer.cash_acct.balance += amount
        print(f"Withdrew ${amount:.2f} from {customer.name}'s card to cash.")
    else:
        print("Insufficient funds in card account.")

def bank():
    global beginner
    while True:
        statebank = input("> ")
        if statebank == str(0):
            bank_help()
        elif statebank == str(1):
            if beginner:
                cash_acc = create_cash_acct(1000)
                card_acc = create_card_acct(0)
                beginner = False
            else:
                cash_acc = create_cash_acct(0)
                card_acc = create_card_acct(0)
            username = input("Username: ")
            ff = create_cus(username, cash_acc, card_acc)
            cus_list.append(ff)
        elif statebank == str(2):
            try:
                get_uuid = input("UUID: ")
                if is_valid_uuid(get_uuid):
                    user_to_remove = find_account_by_uuid(get_uuid)
                    if user_to_remove:
                        cus_list.remove(user_to_remove)
                        print(f"Account {user_to_remove.name} deleted.")
                    else:
                        print("Account not found.")
            except Exception as e:
                print(f"Error: {e}")
        elif statebank == str(3):
            try:
                for user in cus_list:
                    print(f"Name: {user.name}, Cash Account UUID: {user.cash_acct.id}, Cash Balance: ${user.cash_acct.balance:.2f}, "
                          f"Card Account UUID: {user.card_acct.id}, Card Balance: ${user.card_acct.balance:.2f}")
            except Exception as e:
                print(f"Error: {e}")
        elif statebank == str(4):
            from_uuid = input("From Card UUID: ")
            to_uuid = input("To Card UUID: ")
            amount_input = input("Amount to transfer: ")

            try:
                amount = float(amount_input)
                if amount <= 0:
                    print("Amount must be greater than zero.")
                else:
                    transfer_money(from_uuid, to_uuid, amount)
            except ValueError:
                print("Invalid amount. Please enter a numeric value.")
        elif statebank == str(5):
            uuid_str = input("Customer UUID: ")
            amount_input = input("Amount to deposit to card: ")
            customer = find_account_by_uuid(uuid_str)
            if customer:
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        print("Amount must be greater than zero.")
                    else:
                        deposit_cash_to_card(customer, amount)
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            else:
                print("Account not found.")
        elif statebank == str(6):
            uuid_str = input("Customer UUID: ")
            amount_input = input("Amount to withdraw from card: ")
            customer = find_account_by_uuid(uuid_str)
            if customer:
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        print("Amount must be greater than zero.")
                    else:
                        withdraw_cash_from_card(customer, amount)
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            else:
                print("Account not found.")

bank()
