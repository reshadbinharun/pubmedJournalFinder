
# Useful YouTube link: https://www.youtube.com/watch?v=6WpnxmmkYys

# import csv of links | abstract 
# technology search term is constant
	# relevance score_1: lemmatize phrase and check what percentage of abstract it consists of 
# application search term is to be lemmatized
	# calculate same percentage

'''
Steps:
1. Import data as csv
2. Sentence processing, but removing all punctuations and stopwords
'''
import nltk
import pandas as pd
import numpy as numpy
import string #to strip punctuations
import re #to use regex parsing to tokenize words
from textblob import TextBlob #to use built-in sentiment analysis trainer

# nltk.download()

#HELPER FUNCTIONS
#returns a body of text with punctuations removed
def strip_punct(text):
	text = "".join([char for char in text if char not in string.punctuation])
	return text

def tokenize(text):
	return re.split('\W+', text) # split at on non-word strings, + == continue until next word hit

def removeStops(text):
	stops = stopwords.words('english') # gettting the list of all stop words in 
	noStops = [word for word in text if word not in stops]
	return noStops

def sentenceProcess(text):
	no_punct = strip_punct(text)
	tokens = tokenize(no_punct)
	no_stops = removeStops(tokens)
	return no_stops

def lemmatizeAbstract(text):
	return [wn.lemmatize(word) for word in text] #entire array parsed, text is entire array, word is an item in list

##FUNCTIONS FOR SENTIMENT ANALYSIS:

def splitIntoSentences(text):
	return [text.split('.')] # return array of sentences

def calcSenti(sentences):
	objAvg = 0.0
	subjAvg = 0.0
	objSum = 0.0
	subjSum = 0.0
	for line in sentences:
		subjSum += TextBlob(line).sentiment.subjectivity
		objSum += TextBlob(line).sentiment.polarity
	objAvg = objSum/len(sentences)
	subjAvg = subjSum/len(sentences)
	return [objAvg, subjAvg]

def clean_text(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords]
    return text
#HELPER FUNCTIONS


from nltk.corpus import stopwords

#importing csv from local directory

# rawData = open('allAbstracts.csv').read()
# print(rawData)
# MAKE DATAFRAME INSTEAD

fullCorpus = pd.read_csv('allAbstracts.csv')
fullCorpus.columns = ['links', 'abstract_text']

#flatten abstract_text column
#https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.flatten.html
a = numpy.array(fullCorpus.abstract_text)
flattened_text_arr = a.flatten()
fullCorpus.abstract_text = flattened_text_arr

#To confirm that the text arrays in abstract_text column have been flattened
# for abstract in fullCorpus.abstract_text:
# 	print(type(abstract))
# 	print(len(abstract))

# stripped_tokens = []
# for abstract in fullCorpus.abstract_text: 
# 	stripped_tokens.append(sentenceProcess(abstract))
# fullCorpus['stripped_tokens'] = stripped_tokens

#using lambda function instead of loops
fullCorpus['no_punct'] = fullCorpus['abstract_text'].apply(lambda x: strip_punct(x))
fullCorpus['all_tokens'] = fullCorpus['no_punct'].apply(lambda x: tokenize(x))
fullCorpus['no_stops'] = fullCorpus['all_tokens'].apply(lambda x: removeStops(x))


#WordNet Lemmatizer is more intelligent than porter
wn = nltk.WordNetLemmatizer()
ps = nltk.PorterStemmer()
fullCorpus['lemmatized_text'] = fullCorpus['no_stops'].apply(lambda x: lemmatizeAbstract(x))

#Sentiment Analysis
allSentiments = []
for abstract in fullCorpus['abstract_text']:
	abs_sen = splitIntoSentences(abstract)
	sentiments = calcSenti(abs_sen[0][0])
	allSentiments.append(sentiments)
# print(allSentiments[0])

# [[0.0, 0.1], ...] -> format for allSentiments; split into subjectivity and objectivity

# fullCorpus['subjectivity'] = allSentiments[1]
# fullCorpus['objectivity'] = allSentiments[0]


print(fullCorpus.head())
#list comprehension to rid of punctuations and stop words

#exporting results as csv
fullCorpus.to_csv('postAnalysis.csv', sep='\t', index=False)

##COMMENT OUT HERE ON DOWNWARDS :


#Apply CountVectorizer to create document-term matrix
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer(analyzer = clean_text)
X_counts = count_vect.fit_transform(fullCorpus['abstract_text'])
print(X_counts.shape)
print(count_vect.get_feature_names())

