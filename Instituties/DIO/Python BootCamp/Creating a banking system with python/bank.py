import datetime
menu = '''
  ====================================
      Welcome to the banking system
  ====================================
  [1] Deposit
  [2] Withdraw
  [3] Balance
  [4] Extract 
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

def add_info_extract(value: float):
  global extract
  now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

  signal = '-' if value < 0 else '+'
  extract += f'''
------------------------------------
Date: {now}
Value: {signal}R${value:.2f}
'''

def deposit():
  global balance
  deposit = float(input('How much do you want to deposit? R$'))
  while(deposit <= 0):
    print('The value must be greater than 0')
    deposit = float(input('How much do you want to deposit? R$'))
  
  add_info_extract(deposit)
  balance += deposit
  
  print(f'You deposited R${deposit:.2f} and your new balance is R${balance:.2f}')

def withdraw():
  global balance 
  global withdraw_number
  global withdraw_limit
  global withdrawal_limits_per_day

  if(withdraw_number >= withdrawal_limits_per_day):
    print('You have reached the limit of withdrawals per day, please come back tomorrow.')
    return
  
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

while True: 
  print(menu)
  option = int(input('Choose an option: '))

  if option == 1:
    deposit()

  elif option == 2:
    withdraw()

  elif option == 3:
    print(f'Your balance is R${balance:.2f}')

  elif option == 4:
    print(extract)

  elif option == 0:
    break

  else:
    print('Invalid option')