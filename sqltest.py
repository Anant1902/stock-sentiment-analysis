import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', password='Newdelhi2002', database='stocktracking')
mycursor = mydb.cursor()

mycursor.execute("""CREATE TABLE stockdata(
                        stock_id VARCHAR(20),
                        stock_token VARCHAR(20),
                        date DATE,
                        opening_price FLOAT, 
                        closing_price FLOAT,
                        volume FLOAT,
                        adjusted_close FLOAT,
                        adjusted_open FLOAT,
                        adjusted_high FLOAT,
                        adjusted_low FLOAT,
                        adjusted_volume FLOAT,
                        PRIMARY KEY(stock_id)
                        );
                        """)

mydb.commit()