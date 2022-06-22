import json

import requests
import sqlite3
import datetime

def persist_data_db(eurValue, dollarValue):
  try:
    sqliteConnection = sqlite3.connect(r'C:\Users\hfbraga\PycharmProjects\pythonProject\cotacoes.db')
    cursor = sqliteConnection.cursor()
    current_time = datetime.datetime.now()

    sqlite_insert_query = f"""INSERT INTO COTACAO
                              (DOLLAR, EURO, HORARIOCONSULTA) 
                               VALUES 
                              ('{dollarValue}','{eurValue}','{current_time}')"""

    cursor.execute(sqlite_insert_query)
    sqliteConnection.commit()
    print("Cotação persistida no banco de dados com sucesso")
    cursor.close()


  except sqlite3.Error as error:
    print('Erro: ', error)

  finally:

    if sqliteConnection:
      sqliteConnection.close()

def convert_currencies(value, price):
  return value * price

url = 'https://api.hgbrasil.com/finance'
response = requests.get(url)

if response.status_code == 200 :
  listCurrencies = response.json()['results']['currencies']
  usd_price = listCurrencies['USD']['buy']
  eur_price = listCurrencies['EUR']['buy']

  brl_input = float(input('Informe em BRL o valor a ser convertido: ',))

  conversion = usd_price * brl_input
  print('Valor convertido em Dolar: ', convert_currencies(brl_input, usd_price))
  print('Valor convertido em Euro: ', convert_currencies(brl_input, eur_price))
  persist_data_db(eur_price,usd_price)
