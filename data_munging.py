import os
import time
import pandas as pd
import csv
from pandas import DataFrame

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def split_line(previous_time, previous_user, input_text):
    date_split = input_text.split(' - ',1)
    if len(date_split) == 1:
        return previous_time, previous_user, input_text
    time_string = get_date( date_split[0] )
    message_split = date_split[1].split(": ",1)
    if len(message_split) == 1 :
        return time_string, "WHATSAPP", date_split[1]
    return time_string, message_split[0], message_split[1]
    
def get_date ( input_string ):
    date = None
    try:
        date = time.strptime(input_string,'%d %b %Y %H:%M')
    except ValueError:
        date = time.strptime(input_string + ' 2014','%d %b %H:%M %Y')
    return time.strftime('%d %b %H:%M %Y',date)
        
def process_body(line):
    return  line.replace("<Media omitted>","[MEDIA]") \
                .replace('"', '')

    
def get_cleaned_line(date_time, user, body):
    return date_time + ":::" + user + ":::" + process_body(body) + "\n"
    
    

raw_data =  open(os.path.join(__location__, 'raw_data.txt'),'r')

cleaned_data =  open(os.path.join(__location__, 'cleaned_data.txt'),'w')

cleaned_df = DataFrame(columns=('date_time', 'user', 'message'))

lines =  raw_data.readlines()

print len(lines)

df_index = 0
count = 0

current_date_time = "--"
current_user = "--"
current_message = "--"

for line_raw in lines:
    line= line_raw.rstrip('\n')
    date_time,user,message = split_line(current_date_time, current_user, line)
    if user.__eq__(current_user):
        current_message = current_message + " \\ " +message
    else:
        cleaned_df.loc[df_index] = [current_date_time, current_user, current_message]
        current_date_time = date_time
        current_user = user
        current_message = message
        df_index += 1
    if count % 100 == 0:
        print count
    count += 1
   
output_path = os.path.join(__location__, 'cleaned_data.txt')   
cleaned_df.to_csv(output_path, index = False, quoting = csv.QUOTE_ALL)
    


cleaned_data.close()
    

