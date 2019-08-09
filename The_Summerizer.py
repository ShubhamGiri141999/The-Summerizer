#!/usr/bin/env python
# coding: utf-8

# In[2]:


import bs4
import requests
import re
import heapq
import nltk
import PySimpleGUI as sg

print("Enter the topic: ")
topic = input()

url = "https://en.wikipedia.org/wiki/"+topic
extracted_data = requests.get(url)

data = ''

if extracted_data is not None:
    organized_data = bs4.BeautifulSoup(extracted_data.text,'html.parser')

    title = organized_data.select("#firstHeading")[0].text
    paragraphs = organized_data.select("p")
    for paragraph in paragraphs:
        data= data+(paragraph.text)
        
formatted_data = re.sub(r'\[.*\]', '', data)
formatted_data = re.sub(r'\(.*\)', '', formatted_data)
formatted_data = re.sub(r'\s+', ' ', formatted_data)   

sentence_list = nltk.sent_tokenize(formatted_data)
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}

for word in nltk.word_tokenize(formatted_data):                  
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values()) 

for word in word_frequencies.keys():                                        
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    
sentence_scores = {}

for sentence in sentence_list:                                                                       
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word_frequencies.keys():
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

                    
summary_sentences = heapq.nlargest(15, sentence_scores, key=sentence_scores.get)     

summary = ' '.join(summary_sentences)  
print(summary)  



# In[ ]:




