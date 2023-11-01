# Main Project Idea - Web Scrapping relevant financial securities(REITS/Stocks) and using APIs to track them on a daily basis
# To also store this information on a database using SQL, and search for corelation

#Tiingo  ---  APIs to get stock information
#Example of Stock API ---  https://api.tiingo.com/tiingo/daily/<ticker>/prices?token=a5fde2b15537deb452667e9df002f43d033e53a8

import requests
import mysql.connector
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import tweepy as tw


#Automating retreival of stock info from API, and addition to mySQL Stock Tracking Database
mydb = mysql.connector.connect(host='localhost', user='root', password='Newdelhi2002', database='stocktracking')
mycursor = mydb.cursor()

stockportfolio = ['JNJ', 'UNH', 'PFE', 'MRK', 'ABT', 'TMO', 'ABBV', 'AMZN', 'HD', 'MCD','NKE', 'LOW', 'SBUX', 'TGT', 'BABA', 'TCEHY', 'MPNGF', 'JD', 'PDD', 'BEKE', 'BIDU']

def split(word):
    return [ch for ch in word]

def twitter_data_collection(stockportfolio):

    consumer_key = 'fmmFZBEoDovXmQEESrzmniAEl'
    consumer_secret = 'X4eXfw3H0Vl3e5xrLA3a6gw186XWudR9wV52yiBPhzOpp3Ap3m'
    auth = tw.AppAuthHandler(consumer_key, consumer_secret)
    api = tw.API(auth)


    for stock in stockportfolio:
        try:            
            query = stock + ' stock'

            for status in tw.Cursor(api.search, q=query).items(1000):
                #   print(status.text,status.author.screen_name)
                    twitter_id = status.id_str
                    date = list(str(status.created_at).split())[0]
                    time = list(str(status.created_at).split())[1]
                    user_id = status.author.screen_name
                    tweet = status.text
                    stock_token = stock
                    ticker_id = stock + date    
                    
                    new_tweet = []
                    for ch in split(tweet):  
                        if ch == '"':
                            new_ch = '\"'
                        elif ch == "'":
                            new_ch = "\'"
                        else:
                            new_ch = ch
                        new_tweet.append(new_ch)
                    improvised_tweet = ''.join(new_tweet)

                    try:
                        mycursor.execute(f"""INSERT INTO stockportfolio VALUES
                                ('{ticker_id}','{stock_token}','{stock}','{date}'); """)
                        mydb.commit()
                    except mysql.connector.errors.IntegrityError:
                        pass
                    
                    try:
                        mycursor.execute(f"""INSERT INTO twitterdata(twitter_id,date,time,user_id,stock_token,ticker_id) VALUES
                                ('{twitter_id}','{date}','{time}','{user_id}','{stock_token}','{ticker_id}'); """)
                        mydb.commit()
                    except mysql.connector.errors.IntegrityError:
                        pass
                    else:
                        try:
                            mycursor.execute(f"""UPDATE twitterdata
                                    SET text = "{improvised_tweet}"
                                    WHERE twitter_id = "{twitter_id}" ; """)
                            mydb.commit()
                        except mysql.connector.errors.ProgrammingError:
                            pass

                        tb_analyzer = TextBlob(improvised_tweet)
                        vs_analyzer = SentimentIntensityAnalyzer()
                        positive_score = vs_analyzer.polarity_scores(improvised_tweet)['pos']
                        negative_score = vs_analyzer.polarity_scores(improvised_tweet)['neg']
                        neutral_score = vs_analyzer.polarity_scores(improvised_tweet)['neu']
                        compound_score = vs_analyzer.polarity_scores(improvised_tweet)['compound']
                        subjectivity_score = tb_analyzer.sentiment.subjectivity

                        mycursor.execute(f"""INSERT INTO master_data(ticker_id,positive_score,negative_score,neutral_score,compound_score, subjectivity_score, stock_token) VALUES
                                ('{ticker_id}','{positive_score}','{negative_score}','{neutral_score}','{compound_score}',
                                '{subjectivity_score}','{stock}'); """)
                        mydb.commit()

                        mycursor.execute(f"""INSERT INTO sentiment_analysis VALUES
                                ('{twitter_id}','{positive_score}','{negative_score}','{neutral_score}','{compound_score}',
                                '{subjectivity_score}','{twitter_id}','{ticker_id}'); """)
                        mydb.commit()

                    

        except IndexError:
            pass

def stock_data_collection(stockportfolio):

    for stock in stockportfolio:
        stockAPI = "https://api.tiingo.com/tiingo/daily/" + stock + "/prices?startDate=2020-11-01&token=a5fde2b15537deb452667e9df002f43d033e53a8"
        response = requests.get(stockAPI)
        info = response.json()

        for num in range(len(info)):
            closeprice      = float(info[num]['close'])
            openprice       = float(info[num]['open'])
            highestprice    = float(info[num]['high'])
            lowestprice     = float(info[num]['low'])
            volume          = float(info[num]['volume'])
            adjusted_close  = float(info[num]['adjClose'])
            adjusted_open   = float(info[num]['adjOpen'])
            adjusted_high   = float(info[num]['adjHigh'])
            adjusted_low    = float(info[num]['adjLow'])
            adjusted_volume = float(info[num]['adjVolume'])
            divCash         = float(info[num]['divCash'])
            splitfactor     = float(info[num]['splitFactor'])

            
            datetime_list = list(info[num]['date'])
            date_list = []
            for num in range(10):
                date_list.append(datetime_list[num])
            date = ''.join(date_list)


            try:
                mycursor.execute(f"""INSERT INTO stockportfolio VALUES
                        ('{stock}{date}','{stock}','{stock}','{date}'); """)
                mydb.commit()
                
            except mysql.connector.errors.IntegrityError:
                pass
        
            mycursor.execute(f"""INSERT INTO stockdata VALUES
                ('{stock}{date}','{stock}','{date}','{openprice}','{closeprice}','{volume}', '{highestprice}','{lowestprice}',
                '{adjusted_close}','{adjusted_open}','{adjusted_high}','{adjusted_low}','{adjusted_volume}','{stock}{date}'); """)
            mydb.commit()
            print('Executed')
            try:
                mycursor.execute(f"""UPDATE master_data
                                            SET closing_price = "{closeprice}"
                                                WHERE ticker_id = "{stock}{date}"; """)
                mydb.commit()
            except mysql.connector.errors.IntegrityError:
                pass
            
twitter_data_collection(stockportfolio)
stock_data_collection(stockportfolio)