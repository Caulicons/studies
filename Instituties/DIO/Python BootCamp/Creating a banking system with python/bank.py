import datetime
menu = '''
  ====================================
      Welcome to the banking system
  ====================================
  [1] Deposit
  [2] Withdraw
  [3] Balance
  [4] Extract 
  [5] Create user
  [6] Create account

  [0] Exit
'''

balance = 0;
withdraw_limit = 500;
extract = '''
====================================
              Extract
====================================
'''
withdraw_number = 0;
withdrawal_limits_per_day = 3;
users = {
  '123.456.789-10': {
    'name': 'John',} 
}
agency = '0001'
accounts = []
def find_user(cpf: str):
  return users.get(cpf)

def create_user(users):
  cpf = input('Enter your CPF: ')

  if find_user(cpf):
    print('User already exists')
    return users
  
  name = input('Enter your name: ')
  birthdate = input('Enter your birthdate: ')
  address = input('Enter your address: ')

  users[cpf] = {
    'name': name,
    'birthdate': birthdate,
    'address': address
  }

  return users
  

def create_account():
  global agency, accounts
  cpf = input('Enter your CPF: ')
  account_number = len(accounts) + 1
  if find_user(cpf):

    account = {
      'agency': agency,
      'account': account_number,
      'cpf': cpf
    }

    return print('Account created', account)
  
  print('User not found')
  

def add_info_extract(value: float):
  global extract
  now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

  extract += f'''
------------------------------------
Date: {now}
Value: R${value:.2f}
'''


def deposit(balance, /):

  deposit = float(input('How much do you want to deposit? R$'))
  while(deposit <= 0):
    print('The value must be greater than 0')
    deposit = float(input('How much do you want to deposit? R$'))
  
  add_info_extract(deposit)
  balance += deposit
  print(balance)
  print(f'You deposited R${deposit:.2f} and your new balance is R${balance:.2f}')
  return balance

def withdraw(*, balance, withdraw_limit, withdrawal_limits_per_day, withdraw_number):

  if(withdraw_number >= withdrawal_limits_per_day):
    print('You have reached the limit of withdrawals per day, please come back tomorrow.')
    return  balance, withdraw_limit, withdrawal_limits_per_day, withdraw_number
  
  message = 'How much do you want to withdraw? R$'
  withdraw = float(input(message))
  while(withdraw > balance):
    print(f'The value must be less than your balance, your balance is R${balance:.2f}.')
    withdraw = float(input(message))
  while(withdraw > withdraw_limit):
    print(f'The value must be less than your withdraw limit, your withdraw limit is R${withdraw_limit:.2f}.')
    withdraw = float(input(message))

  add_info_extract(-withdraw)
  balance -= withdraw
  withdraw_number += 1

  print(f'You withdrew {withdraw} and your new balance is {balance}')

  return balance, withdraw_limit, withdrawal_limits_per_day, withdraw_number

while True: 
  print(menu)
  option = int(input('Choose an option: '))

  if option == 1:
    balance = deposit(balance)

  elif option == 2:
   balance, withdraw_limit, withdrawal_limits_per_day, withdraw_number  = withdraw(balance=balance, withdraw_limit=withdraw_limit, withdrawal_limits_per_day=withdrawal_limits_per_day, withdraw_number=withdraw_number)

  elif option == 3:
    print(f'Your balance is R${balance:.2f}')

  elif option == 4:
    print(extract)

  elif option == 5:
    users = create_user(users)

  elif option == 6:
    account = create_account()

  elif option == 0:
    break

  else:
    print('Invalid option')