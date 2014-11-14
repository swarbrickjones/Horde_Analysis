import nltk 
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from collections import Counter
from nltk.stem.porter import *
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import string
import re

stop_words = {'im','a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your'}
exclude = set(string.punctuation)

print stopwords

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


corpusdir= os.path.join(__location__, 'nlp/user_messages/')
newcorpus = PlaintextCorpusReader(corpusdir, '.*')

token_dict = {}
stemmer = PorterStemmer()

def replace_punctiation_char(ch):
    if ch in exclude:
        return ' '
    else :
        return ch
  
def remove_websites(text):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)      

def remove_punctiation(s):    
    return ''.join(replace_punctiation_char(ch) for ch in s )
    
def remove_emojis(s):
    return re.sub(r'EMOJI\[[a-z\d]*\]', ' ', s)

def remove_media(s):
    return re.sub(r'MEDIA', ' ', s)
    
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed
   
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems    
    
for infile in sorted(newcorpus.fileids()):
    print infile # The fileids of each file.
    fin =  newcorpus.open(infile)  # Opens the file.
    text =  fin.read().strip() # Prints the content of the file
    just_text = remove_websites(remove_media(remove_emojis(text)).lower())
    no_punctuation = remove_punctiation(just_text)
    token_dict[infile] = no_punctuation
    
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())

print token_dict