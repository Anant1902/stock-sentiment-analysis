import tweepy as tw
import webbrowser
import time

consumer_key = 'fmmFZBEoDovXmQEESrzmniAEl'
consumer_secret = 'X4eXfw3H0Vl3e5xrLA3a6gw186XWudR9wV52yiBPhzOpp3Ap3m'

callback_url = 'oob'

auth = tw.AppAuthHandler(consumer_key, consumer_secret)

#redirect_url = auth.get_authorization_url()
#webbrowser.open(redirect_url)

#user_pin_input = input("User pin ? ")

#auth.get_access_token(user_pin_input)

api = tw.API(auth)

query = 'amazon stock'

for i,status in enumerate(tw.Cursor(api.search, q=query).items(50)):
    print(i,status.text,status.author.screen_name)
