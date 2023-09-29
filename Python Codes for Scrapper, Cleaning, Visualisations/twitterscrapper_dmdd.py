import configparser
import pandas as pd
import tweepy
import datetime


# read configs (config.ini was a seperate file created to avoid sharing keys)
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


keywords = input('Enter keywords to find people profiles: \n')
#keywords = '#news,#India'
limit=20

users = tweepy.Cursor(api.search_users, q=keywords, count=8, tweet_mode='extended').items(limit)


# create DataFrame
columns = ['User ID', 'Name' , 'Followers','Location','Description','Created At','Verified','URL', 'Total Tweets', 'Total tweets in last 24hrs','Latest Status updated by User', 'Witheld In Countries', 'Following', 'Total Likes By Profile']
data = []

columns1 = ['User ID', 'Tweet Created At' , 'Tweet Likes','Retweets','Tweet Description']
data1 = []


#for users fetched this will get username, name, followers, description, creation date, url, total tweets, following, countries the account is withheld from, likes, status
for user in users:
    count = 0
    username = api.get_user(screen_name=user.screen_name)
    name = username.name
    followers_count = username.followers_count    
    location = username.location
    description = username.description
    created_at = username.created_at
    verified = username.verified
    url = username.url
    total_tweets = username.statuses_count
    status_update = username.status
    withheld = username.withheld_in_countries
    following = username.friends_count	
    likes = username.favourites_count
   
    
    tweets = tweepy.Cursor(api.user_timeline, screen_name=user.screen_name, count=20, tweet_mode='extended').items(limit)
    #for tweets made in last 1 day of each user this will fetch created date, favourites count, retweet count, description
    for tweet in tweets:
        tweet_created = tweet.created_at     
        tweet_fav = tweet.favorite_count
        tweet_desc= tweet.full_text
        tweet_retweet = tweet.retweet_count
        
        current_time = datetime.datetime.now()-datetime.timedelta(days=1)
        if(tweet_created.date()>=current_time.date()):
            count = count + 1
            data1.append([user.screen_name,tweet_created,tweet_fav,tweet_retweet,tweet_desc])
    

    data.append([user.screen_name,name,followers_count,location,description,created_at,verified,url,total_tweets, count,status_update,withheld,following,likes])


df = pd.DataFrame(data, columns=columns)
df1 = pd.DataFrame(data1, columns=columns1)

#converting data frame to csv file
df.to_csv('twitter_user.csv')
df1.to_csv('tweets.csv')