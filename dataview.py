import requests
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

mydb = mysql.connector.connect(host='localhost', user='root', password='Newdelhi2002', database='stocktracking')
mycursor = mydb.cursor()

mycursor.execute('''SELECT ticker_id, compound_score, subjectivity_score, closing_price 
                        FROM master_data
                            WHERE stock_token = 'AMZN'
                                ORDER BY ticker_id ASC;''')

table_rows = mycursor.fetchall()


df = pd.DataFrame(table_rows, columns=mycursor.column_names)
print(df)
df['compound_score'].plot(x='ticker_id',y='compound_score').set_ylabel('Compound Score')

df['closing_price'].plot(x='ticker_id',y='closing_price',secondary_y=True, style='g').set_ylabel('Closing Price')

plt.show()
plt.close()