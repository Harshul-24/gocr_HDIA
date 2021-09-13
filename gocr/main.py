# import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import _json
from pathlib import Path

# path = '/content/drive/MyDrive/sanskrit_poems-pages-14-50.txt'
# To do - iterate over every image file, modularize the word length frequency calculation
# to do - look for optimization

wordCount = dict()  # stores as value the actual words and their corresponding word-lengths.
wordFreq = dict()  # stores only the frequency of each word-length.


def readChars(path):  # reads a page and cleans it to only include sanskrit characters.

    with open(path, encoding="utf-8", errors="ignore") as file:
        txt = file.read()
    txt = txt.replace('\n', '')  # stripping newline character

    for char in txt:
        if ord(char) == 32:  # for space character
            continue
        if ord(char) < 2304 or ord(char) > 2431:  # rdrop non-devanagari characters
            txt = txt.replace(char, '')

    replaceChars = "।१२३४५६७८९॥"  # remove poorna viram and verse numbers
    for char in replaceChars:
        txt = txt.replace(char, '')

    txt = txt.replace('  ', '')
    corpus = list(txt.split(" "))
    return corpus


# corpus = readChars(r'C:\Users\User\Documents\IHDIA_cloud_vision\gocr\result\20.txt')


def charStats(corpus, wordCount, wordFreq):
    for word in corpus:
        length = len(word)
        if length not in wordCount.keys():
            wordCount[length] = []
            wordFreq[length] = 1
        wordCount[length].append(word)
        wordFreq[length] += 1
        # sorted(wordCount.keys())

    return (wordCount, wordFreq)


dir = os.getcwd()  # C:\Users\User\Documents\IHDIA_cloud_vision\gocr
curPath = os.path.join(dir, 'result')


# print(curPath)
# print(dir_list)

def bookIter(curPath, wordCount, wordFreq):
    dir_list = os.listdir(curPath)
    for filename in dir_list:
        fullPath = os.path.join(curPath, filename)
        corpus = readChars(fullPath)
        #print(" the current corpus is: ", corpus)
        wordCount, wordFreq = charStats(corpus, wordCount, wordFreq)

    return (wordCount, wordFreq)


wordCount, wordFreq = bookIter(curPath, wordCount, wordFreq)

x = list(wordFreq.keys())
y = list(wordFreq.values())

print(wordCount[1])
# print(wordFreq)

df = pd.DataFrame(np.transpose([x, y]), columns=['Word Length', 'Frequency'], index=range(len(x)))
df = df.sort_values('Word Length', ascending=False).reset_index().drop(columns=['index'])
df.drop(df.loc[df['Word Length'] == 0].index, inplace=True)
#df.drop(df.loc[df['Word Length'] == 1].index, inplace=True)
print(df)
df.to_json('./Atharva_veda-stats.json')

fig = px.histogram(df, x='Word Length', y='Frequency', nbins=10, histnorm="probability")
# fig.show()

fig2 = px.histogram(df, x='Word Length', y='Frequency', nbins=10)
# fig2.show()

fig3 = px.bar(df, x='Word Length', y='Frequency', hover_name='Frequency',
              title='Kaumudi Book Stats: Bar plot')
fig3.show()
