import os
import time
from datetime import timedelta, datetime
import csv
from pandas import DataFrame
import sys
import inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"emoji")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
    
from unicode_conversion import convert_unicode

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def split_line(previous_time, previous_user, input_text):
    date_split = input_text.split(' - ',1)
    if len(date_split) == 1:        
        return previous_time, previous_user, input_text
    time_string = ""
    try :
        time_string = get_date( date_split[0] )
    except ValueError:
            return previous_time, previous_user, input_text
    message_split = date_split[1].split(": ",1)
    if len(message_split) == 1 :
        return time_string, 'WhatsApp', date_split[1]
    return time_string, user_name_map[message_split[0]], message_split[1]
    


user_name_map = {    \
    'Eliza Botts' : 'Eliza', \
    'Cate':'Cate', \
    '\xe2\x80\xaa+44 7807 744465\xe2\x80\xac':'Hannah', \
    'Kritzia':'Krizia', \
    'Wills':'Wills',  \
    'Angela':'Angela',  \
    'Bunn':'Bunn',  \
    '\xe2\x80\xaa+44 7979 853510\xe2\x80\xac':'Chris', \
    'Dave Mendez':'Dave', \
    '\xe2\x80\xaa+44 7794 501335\xe2\x80\xac':'Catrin', \
    '\xe2\x80\xaa+44 7545 989149\xe2\x80\xac':'Dan',  \
    'Teegan':'Tegan', \
    'Mike':'Mike', \
    'Joe Jarman':'Joe', \
    'Alan Wright':'Alan', \
    'p tschismarov':'Phil', \
    'WhatsApp':'WhatsApp', \
    'Henry Franks':'Henry', \
    '\xe2\x80\xaa+61 405 567 873\xe2\x80\xac':'Wagg', \
    'Mateusz Tylicki':'Mateusz', \
    'Marth':'Marth', \
    'Lora Staffenschloten' : 'Lora', \
    'Bongo':'Bongo', \
    '\xe2\x80\xaa+44 7830 332317\xe2\x80\xac':'Simone', \
    'Shaggy Crazy Horse':'Shaggy', \
    '\xe2\x80\xaa+44 7834 379555\xe2\x80\xac':'Vinay', \
    'Owen James':'Owen', \
    'Slam':'Sam', \
    '\xe2\x80\xaa+44 7754 268447\xe2\x80\xac':'Cate', \
    '\xe2\x80\xaa+44 7502 048124\xe2\x80\xac':'Lorna', \
    'Vanessa "Beast" Matthews':'Vanessa', \
    'Adamina Carden':'Adimina', \
    '\xe2\x80\xaa+44 7944 609055\xe2\x80\xac':'Em', \
    '\xe2\x80\xaa+44 7850 688790\xe2\x80\xac':'Sadie'
    }

input_date_format = '%H:%M, %d %b %Y'
output_date_format = '%d %b %H:%M %Y'

def get_date ( input_string ):
    date = None
    try:
        date = time.strptime(input_string,input_date_format)
    except ValueError:
        date = time.strptime(input_string + ' 2014',input_date_format)
    return time.strftime(output_date_format,date)
    
short_time = timedelta(minutes = 5)  
    
def is_short_time(current_time, date_time):
    start_date = datetime.strptime(date_time,output_date_format)
    end_date = datetime.strptime(current_time,output_date_format)
    diff = abs(start_date - end_date)
    return diff < short_time

def process_body(text):
    text =  ''.join([char if ord(char) < 128 else format_non_ascii(char)  for char in unicode(text)])
    return text.replace("<Media omitted>"," [MEDIA] ") \
                .replace('"', '') \
  


def format_non_ascii(char):
    u_escaped = str(char.encode('unicode_escape'))
    try :
        converted_string =  convert_unicode(u_escaped)
        return ' EMOJI[' + converted_string + '] '
    except KeyError :
        return char
        
def format_notification(message):
    for key in user_name_map.keys():
        message = message.replace(key, user_name_map[key])
    if message[0:12] == "Shaggy added":
        message = "USER_ENTERED : " + message[13 :]
    if message[-6:] == "joined":
        message = "USER_ENTERED : " + message[:-7]
    if message[0:14] == "Shaggy removed":
        message = "USER_LEFT : " + message[15 :]
    if message[-4:] == "left":
        message = "USER_LEFT : " + message[:-5]
    if message[-11:] == "was removed":
        message = "USER_LEFT : " + message[:-12]
    return message
                

raw_data =  open(os.path.join(__location__, 'phil_raw.txt'),'r')

##cleaned_data =  open(os.path.join(__location__, 'phil_raw.txt'),'w')

cleaned_df = DataFrame(columns=('date_time', 'user', 'message'))

lines =  raw_data.readlines()

print len(lines)

df_index = 0
count = 0

current_date_time = "date_time"
current_user = "user"
current_message = "message"

unicode_set = set()


for line_raw in lines:
    line= line_raw.rstrip('\n')
    date_time,user,message = split_line(current_date_time, current_user, line)
    if user.__eq__(current_user) and current_user != 'WhatsApp' and is_short_time(current_date_time, date_time):
        current_date_time = date_time
        current_message = current_message + ". " + process_body(message)
        continue
    else:
        if user == 'WhatsApp':    
            message = format_notification(message)            
        cleaned_df.loc[df_index] = [current_date_time, current_user, current_message]
        current_date_time = date_time
        current_user = user
        current_message = process_body(message)
        df_index += 1
    if count % 1000 == 0:
        print count
    count += 1

#print unicode_set


output_path = os.path.join(__location__, 'cleaned_data.csv')
cleaned_df.to_csv(output_path, index = False, quoting = csv.QUOTE_ALL, header = False)
    

