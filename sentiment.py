import os
import pandas as pd
import matplotlib
from textblob import TextBlob
import numpy as np
import csv

font = {'family' : 'sans-serif',
        'weight' : 'bold',
        'size'   : 10}

matplotlib.rc('font', **font)


__location__ = os.path.realpath((os.getcwd()))

raw_data = pd.read_csv(os.path.join(__location__, 'data/cleaned_data.csv'))
raw_data['date_time']  = pd.to_datetime(raw_data['date_time2'])

user_messages = raw_data[raw_data['user']!='WhatsApp']
notifications = raw_data[raw_data['user']=='WhatsApp']

print 'loaded',len(user_messages),'user messages and',len(notifications),'WhatsApp notifications from file'

user_names = set(user_messages['user'])
print user_names

def sentiment(message):
    text = TextBlob(message)
    response = {'polarity' : text.polarity , 'subjectivity' : text.subjectivity}
    return response
    

user_messages['polarity'] = [sentiment(message)['polarity'] for message in user_messages.message]
user_messages['subjectivity'] = [sentiment(message)['subjectivity'] for message in user_messages.message]
print user_messages.groupby('user').agg({'polarity': np.mean}).sort('polarity',ascending = False)
print user_messages.groupby('user').agg({'subjectivity': np.mean}).sort('subjectivity',ascending=False)

user_messages[['message','polarity','subjectivity']].to_csv(os.path.join(__location__, 'data/sentiment.csv'), index = False, quoting = csv.QUOTE_ALL)