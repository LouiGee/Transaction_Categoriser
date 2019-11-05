import pandas as pd
import numpy as np
from datetime import datetime


def pullandcat(inputstatement, outputstatement, inputdate):
    trans = pd.read_csv('/Users/luisgoate/Desktop/Budget/{0}.csv'.format(inputstatement), header = None)

    trans.columns = ['Date', 'Vendor', 'Amount']
 
    date = datetime.strptime(inputdate, '%d/%m/%Y')
#Format date
    trans['Date'] = pd.to_datetime(trans['Date'], format='%d/%m/%Y')

#Choose relevant dates
    trans = trans[trans['Date'] >= date ]

#Only include rows that have '-' to capture expenditures
    trans = trans[trans.Amount.str.contains("-")]

#Format amounts
    trans['Amount'] = trans['Amount'].str[1:]
    trans['Amount'] = trans['Amount'].astype(float)

#Categrorise data
    conditions = [
    #Groceries
    (trans['Vendor'].str.contains('TESCO') == True),
    (trans['Vendor'].str.contains('GATHER') == True),
    (trans['Vendor'].str.contains('SAINS') == True),
    (trans['Vendor'].str.contains('M&S') == True),
    (trans['Vendor'].str.contains('MANGER') == True),
    (trans['Vendor'].str.contains('DELIVEROO') == True),
    
    #Socialising
    (trans['Vendor'].str.contains('CAFE') == True),
    (trans['Vendor'].str.contains('PUB') == True),

    #Travel
    (trans['Vendor'].str.contains('TFL') == True),
    (trans['Vendor'].str.contains('UBER') == True),
    (trans['Vendor'].str.contains('LUL') == True),

    #Rent
    (trans['Vendor'].str.contains('8BFORDAM') == True),

    #Gym
    (trans['Vendor'].str.contains('PURE') == True),

    #Mobile
    (trans['Vendor'].str.contains('MOBILE') == True)]
   

    choices = ['Groceries', 'Groceries', 'Groceries', 'Groceries', 'Groceries', 'Groceries',
           'Socialising', 'Socialising',
           'Travel', 'Travel', 'Travel',
           'Rent',
           'Gym',
           'Mobile']

    trans['Category'] = np.select(conditions, choices, default='Other')

#Pivot
    columns = ['Date', 'Vendor', 'Category']
    excel_dump = pd.pivot_table(trans, values = 'Amount' , index = columns,
    aggfunc = np.sum)

 
 #Export 
    excel_dump.to_excel('/Users/luisgoate/Desktop/Budget/{0}.xlsx'.format(outputstatement))


pullandcat('TransHist','TransHist', '28/10/2019')




