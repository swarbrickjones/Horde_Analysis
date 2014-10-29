import os
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime, timedelta, date
import time

font = {'family' : 'sans-serif',
        'weight' : 'bold',
        'size'   : 10}

matplotlib.rc('font', **font)

__location__ = os.path.realpath((os.getcwd()))

raw_data = pd.read_csv(os.path.join(__location__, 'cleaned_data.csv'))
raw_data['date_time']  = pd.to_datetime(raw_data['date_time'])



print time.strptime('2014/01/01')


#
##user_messages = raw_data[raw_data['user']!='WhatsApp']
#notifications = raw_data[raw_data['user']=='WhatsApp']
#
#
#min_day = raw_data['date_time'].min()
#max_day = raw_data['date_time'].max()
#
#
#print(dt.timedelta(seconds=hms.seconds%resolution.seconds))
#
#
#def add_notification_to_dict(dictionary, table, chars_to_skip):
#    for row in table.iterrows():
#        user = row[1].get_value('message')[chars_to_skip:]
#        date = row[1].get_value('date_time')
#        if not dictionary.has_key(user):
#            dictionary[user]=list()  
#        dictionary[user].append(date)
#
#add_notification_to_dict(joined_dict, join_notifications, 15)
#add_notification_to_dict(left_dict, left_notifications, 12)
#
#user_date_ranges = {}
#  
#for user in joined_dict.keys():
#    if not left_dict.has_key(user):
#        left_dict[user] = [max_day]
#    joined_list = joined_dict[user]  
#    left_list = left_dict[user]
#    if len(joined_list) > len(left_list):
#        left_list.append(max_day)
#    user_date_ranges[user]=[]
#    for index in range(len(joined_list)):
#        dr = pd.date_range(joined_list[index], left_list[index])
#        user_date_ranges[user].append(dr)
#
#days = []
#user_counts = []
##
##for day in pd.date_range(start=min_day,end = max_day - pd.DateOffset(days =1),freq='3H'):
##    days.append(day)
##    count = 0
##    for user in user_date_ranges.keys():
##        for date_range in user_date_ranges[user]:
##            if day > date_range.min() and day <= date_range.max():
##                count += 1
##    user_counts.append(count)
##    
##
##fig1 = plt.plot(days, user_counts)
##plt.show(fig1)
#
#
#
#    
#
#
