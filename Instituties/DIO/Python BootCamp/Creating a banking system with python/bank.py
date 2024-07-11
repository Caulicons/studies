import datetime
from abc import ABC, abstractmethod

class Client:
  def __init__(self, address): 
    self.address = address
    self.accounts = []

  def perform_transaction(self, account, transaction):
    transaction.register(account)

  def add_account(self, account):
    self.accounts.append(account)

class PF(Client):
  def __init__(self, cpf, name, birthdate, address):
    super().__init__(address)
    self.cpf = cpf
    self.name = name
    self.birthdate = birthdate

class Extract: 
  def __init__(self):
    self._transactions = []

  @property
  def transactions(self):
    return self._transactions
    
  def add_transaction(self, transaction):
    self._transactions.append(
      # FIXME: transaction
      {
        'type': transaction.__class__.__name__,
        'value': transaction.value,
        'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
      }
    )

class Account: 
  # Maybe later the 'Number account' can auto increment
  def __init__(self, client, number):
    self._balance = 0
    self._number = number
    self._agency = '0001'
    self.client = client
    self._extract = Extract()
  
  @classmethod
  def new_account(cls, client, number):
    return cls(client, number)
  
  @property
  def balance(self): 
    return self._balance
  
  @property
  def number(self):
     return self._number
  
  @property
  def agency(self):
    return self._agency
  
  @property
  def extract(self):
    return self._extract
  
  def deposit(self, value): 
    if value <= 0: 
      print('\n ⛔The value must be greater than 0')
      return False
    
    self._balance += value
    print(f'You deposited R${value:.2f} and your new balance is R${self._balance:.2f}')
    return True
  
  def withdraw(self, value):
    if value > self._balance: 
      print('\n ⛔The value must be less than your balance')
      return False
    
    
    self._balance -= value
    print(f'You withdrew R${value:.2f} and your new balance is R${self._balance:.2f}')
    return True

class CurrentAccount(Account):
  def __init__(self, client, number, withdraw_limit=500, withdrawal_limits_per_day=3):
    super().__init__(client, number)
    self._withdraw_limit = withdraw_limit
    self._withdrawal_limits_per_day = withdrawal_limits_per_day

  def withdraw(self, value):
    withdraw_numbers = len([
      transaction for transaction in self.extract.transactions
      if transaction['type'] == 'Withdraw'
    ])

    if value > self._withdraw_limit:
      print('\n ⛔The value must be less than your withdraw limit')
    
    elif withdraw_numbers >= self._withdrawal_limits_per_day:
      print('\n ⛔You have reached the limit of withdrawals per day, please come back tomorrow.')
    
    else: 
      return super().withdraw(value)
    
    return False
  
  def __srt__(self):
    return f"""\
    Number: {self.number}
    Agency: {self.agency}
    Holder: {self.client.name}
    """

class Transaction(ABC):
  
  @property
  @abstractmethod
  def value(self):
    pass

  @classmethod
  @abstractmethod
  def register(self, account):
    pass

class Deposit(Transaction):
  def __init__(self, value):
    self._value = value
  
  @property
  def value(self):
    return self._value

  def register(self, account):
    success_transaction = account.deposit(self.value)

    if(success_transaction):
      account.extract.add_transaction(self)

class Withdraw(Transaction):
  def __init__(self, value):
    self._value = value
  
  @property
  def value(self):
    return self._value

  def register(self, account):
    success_transaction = account.withdraw(self.value)

    if(success_transaction):
      account.extract.add_transaction(self)


def find_user(cpf: str, clients: list):
  user = [client for client in clients if client.cpf == cpf]
  return user[0] if user else None

def create_user(clients):
  cpf = input('Enter your CPF: ')

  if find_user(cpf, clients):
    print('User already exists')
    return
  
  name = input('Enter your name: ')
  birthdate = input('Enter your birthdate: ')
  address = input('Enter your address: ')

  new_client = PF(cpf, name, birthdate, address)
  print(new_client.cpf)
  clients.append(new_client)
  print(clients)

  print(f'User {new_client.name} created')
  
def create_account(account_number, users, accounts):
  cpf = input('Enter your CPF: ')
  client = find_user(cpf, users)

  if not client:
    print('User not found')
    return
  
  account = CurrentAccount.new_account(client, account_number)
  accounts.append(account)
  client.add_account(account)

  print(f'Account {account.number} created')


  
def add_info_extract(value: float):
  global extract
  now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

  extract += f'''
------------------------------------
Date: {now}
Value: R${value:.2f}
'''

def catch_account(client):
  if not client.accounts:
    print('Client does not have an account')
    return 
  
  return client.accounts[0]

def deposit(users):
  cpf = input('Enter your CPF: ')
  client = find_user(cpf, users)

  if not client:
    print('User not found')
    return
  
  value = float(input('How much do you want to deposit? R$'))
  transaction = Deposit(value)

  account = catch_account(client)
  if not account:
    return
  
  client.perform_transaction(account, transaction)


def withdraw(users):
  cpf = input('Enter your CPF: ')
  client = find_user(cpf, users)

  if not client:
    print('User not found')
    return
  
  value = float(input('How much do you want to withdraw? R$'))
  transaction = Withdraw(value)

  account = catch_account(client)
  if not account:
    return
  
  client.perform_transaction(account, transaction)

def show_extract(users):
  cpf = input('Enter your CPF: ')
  client = find_user(cpf, users)

  if not client:
    print('User not found')
    return
  
  account = catch_account(client)
  if not account:
    return
  
  print("\n================ EXTRACT ================")
  transactions=   account.extract.transactions()

  extract = ""
  if not transactions:
    print("No transactions yet")
  else:
    for transaction in transactions:
      extract += f'''
      Date: {transaction['date']}
      Type: {transaction['type']}
      Value: R${transaction['value']}
      '''
    print(extract)
    print(f"\Balance:\n\tR$ {account.balance:.2f}")
    print("==========================================")


def main():
    clients = []
    accounts = []

    while True: 

      menu = '''
      ====================================
          Welcome to the banking system
      ====================================
      [1] Deposit
      [2] Withdraw
      [3] Show extract
      [4] Create user
      [5] Create account

      [0] Exit
    '''

      option = int(input(menu))

      if option == 1:
        deposit(clients)

      elif option == 2:
        withdraw(clients)
      elif option == 3:
        show_extract(clients)

      elif option == 4:
        create_user(clients)

      elif option == 5:
        account_number = len(clients) + 1
        create_account(account_number, clients, accounts)

      elif option == 0:
        break

      else:
        print('Invalid option')


main()