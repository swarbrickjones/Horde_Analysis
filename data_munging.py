import os
import time
from datetime import timedelta, datetime
import csv
from pandas import DataFrame
import sys
import inspect
reload(sys)
sys.setdefaultencoding("utf-8")


cmd_subfolder = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "emoji")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from unicode_conversion import convert_unicode

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def split_line(previous_time, previous_user, input_text):
    date_split = input_text.split(' - ', 1)
    if len(date_split) == 1:
        return previous_time, previous_user, input_text
    time_string = ""
    try:
        time_string = get_date(date_split[0])
    except ValueError, e:
        return previous_time, previous_user, input_text
    message_split = date_split[1].split(": ", 1)
    if len(message_split) == 1:
        return time_string, 'WhatsApp', date_split[1]

    user_name = user_name_map[sanitise_user_string(message_split[0])]
    return time_string, user_name, message_split[1]


def sanitise_user_string(s):
    return s.replace("\xe2\x80\xaa", "").replace("\xe2\x80\xac", "")


user_name_map = {
    'Sam Trundell': 'Sam T',
    'Sadie': 'Sadie',
    'Steven': 'Steve',
    'Mike Joyce': 'MikeJ',
    'Jimena': 'Jimena',
    '+41 79 402 54 65': 'Jimena',
    'Eliza Botts': 'Eliza',
    'Eliza': 'Eliza',
    'Cate': 'Cate',
    'Z cate fuchter': 'Cate',
    '+44 7754 268447': 'Cate',
    '+44 7807 744465': 'Hannah',
    'Hannah Murphy': 'Hannah',
    'Kritzia': 'Krizia',
    'Krizia': 'Krizia',
    'Wills': 'Wills',
    'Adam Wills': 'Wills',
    'Angela': 'Angela',
    'Bunn': 'Bunn',
    'Alex Bunn': 'Bunn',
    '+44 7979 853510': 'Chris',
    'Chris (Health Unlocked)': 'Chris',
    'Dave Mendez': 'Dave',
    'Dave': 'Dave',
    '+44 7794 501335': 'Catrin',
    '+44 7545 989149': 'Dan',
    'Dan Sluckin': 'Dan',
    'Teegan': 'Tegan',
    'Tegan': 'Tegan',
    'Mike': 'Mike',
    'Mike SJ': 'Mike',
    'Mike Swarbrick Jones': 'Mike',
    'Mal': 'Mal',
    'Luana': 'Luana',
    'Joe Jarman': 'Joe',
    'Alan Wright': 'Alan',
    'Alan': 'Alan',
    'p tschismarov': 'Phil',
    'Phil': 'Phil',
    'WhatsApp': 'WhatsApp',
    'Henry Franks': 'Henry',
    'Henry Dranks': 'Henry',
    '+61 405 567 873': 'Wagg',
    'Mateusz Tylicki': 'Mateusz',
    'Mateusz': 'Mateusz',
    'Marth': 'Marth',
    'Martha': 'Marth',
    'Lora Staffenschloten': 'Lora',
    'Lora': 'Lora',
    'Bongo': 'Bongo',
    '+44 7830 332317': 'Simone',
    'Shaggy Crazy Horse': 'Shaggy',
    'Shaggy': 'Shaggy',
    '+44 7834 379555': 'Vinay',
    'Vinay': 'Vinay',
    'Owen James': 'Owen',
    'Owen': 'Owen',
    'Slam': 'Sam',
    'Sam Roberts': 'Sam',
    '+44 7502 048124': 'Lorna',
    'Lorna': 'Lorna',
    'Vanessa "Beast" Matthews': 'Vanessa',
    'Vanessa': 'Vanessa',
    'Adamina Carden': 'Adimina',
    'Adimina': 'Adimina',
    '+44 7944 609055': 'Em',
    '+44 7850 688790': 'Sadie',
    'Lisa': 'Lisa', 'Loz': 'Loz',
    'Tanya': 'Tanya', 'Pete Morey': 'Pete'
}


print user_name_map.keys()
input_date_format_0 = '%d %b %Y %H:%M'
input_date_format_1 = '%H:%M, %d %b %Y'
input_date_format_2 = '%d %b %H:%M %Y'
input_date_format_3 = '%d/%m/%Y, %H:%M'
output_date_format = '%d %b %H:%M %Y'


def get_date(input_string):

    date = None
    try:
        date = time.strptime(input_string, input_date_format_0)
    except ValueError:
        try:
            date = time.strptime(input_string, input_date_format_1)
        except ValueError:
            try:
                date = time.strptime(input_string + ' 2014', input_date_format_1)
            except ValueError:
                try:
                    date = time.strptime(input_string + ' 2015', input_date_format_2)
                except ValueError:
                    date = time.strptime(input_string, input_date_format_3)
                    # print date
    # print date
    return time.strftime(output_date_format, date)

short_time = timedelta(minutes=5)


def is_short_time(current_time, date_time):
    start_date = datetime.strptime(date_time, output_date_format)
    end_date = datetime.strptime(current_time, output_date_format)
    diff = abs(start_date - end_date)
    return diff < short_time


def process_body(text):
    text, emojis = process_unicode(text)
    return text.replace("<Media omitted>", " [MEDIA] ") \
        .replace('"', ''), emojis \



def process_unicode(string):
    str_list = []
    emojis = list()
    new_char = ""
    for char in unicode(string):
        if ord(char) < 128:
            new_char = char
        else:
            new_char = format_non_ascii(char, emojis)
        str_list.append(new_char)
    return "".join(str_list), emojis


def format_non_ascii(char, emojis):
    u_escaped = str(char.encode('unicode_escape'))
    try:
        converted_string = convert_unicode(u_escaped)
        if len(converted_string) == 4 or len(converted_string) > 6:
            raise KeyError
        if converted_string == '1f1f2':
            converted_string = '1f1fd'
        emojis.append(converted_string)
        return ' EMOJI[' + converted_string + '] '
    except KeyError:
        return char


def format_notification(message):

    message = sanitise_user_string(message)

    for key in user_name_map.keys():
        message = message.replace(key, user_name_map[key])
    if message[0:12] == "Shaggy added":
        message = "USER_ENTERED : " + message[13:]
    if message[-6:] == "joined":
        message = "USER_ENTERED : " + message[:-7]
    if message[0:14] == "Shaggy removed":
        print message
        message = "USER_BANNED : " + message[15:]
    if message[-4:] == "left":
        message = "USER_LEFT : " + message[:-5]
    if message[-11:] == "was removed":
        message = "USER_LEFT : " + message[:-12]
    return message


def process_emoji_set(emoji_set):
    return "".join([str(i) + ',' for i in emoji_set])[:-1]

raw_data = open(os.path.join(__location__, 'data/updated_paste.txt'), 'r')

#cleaned_df = DataFrame(columns=('date_time', 'user', 'message'))

lines = raw_data.readlines()

print len(lines)

df_index = 0
count = 0

current_date_time = "date_time"
current_user = "user"
current_message = "message"
current_emoji = list()

unicode_set = list()

pandas_dicts = {}

for line_raw in lines:
    line = line_raw.rstrip('\n')
    date_time, user, message = split_line(current_date_time, current_user, line)
    if user.__eq__(current_user) and current_user != 'WhatsApp' and is_short_time(current_date_time, date_time):
        current_date_time = date_time
        text, emojis = process_body(message)
        current_message = current_message + ". " + text
        current_emoji += emojis
        continue
    else:
        if user == 'WhatsApp':
            message = format_notification(message)
        emoji_str = process_emoji_set(current_emoji)
        new_dict = {'date_time': current_date_time,
                    'user': current_user,
                    'message': current_message,
                    'emoji': emoji_str
                    }
        pandas_dicts[df_index] = new_dict
        current_date_time = date_time
        current_user = user
        current_message, current_emoji = process_body(message)
        df_index += 1
    # if count % 1000 == 0:
    #    print count
    count += 1


cleaned_df = DataFrame.from_dict(pandas_dicts, orient='index')

output_path = os.path.join(__location__, 'data/cleaned_data.csv')
cleaned_df[1:].to_csv(output_path, index=False, quoting=csv.QUOTE_ALL)
