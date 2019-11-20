import os
import requests
import re
from text_summary import TextSummary
import spacy
import nltk
from io import StringIO
import sys

os.system('cls' if os.name == 'nt' else 'clear')


def entities(list_string):
    nlp = spacy.load('en')
    sentence = ' '.join(list_string)
    doc = nlp(sentence)
    # document level
    ents = [(e.text, e.label_) for e in doc.ents]
    return ents


def get_labels(sentence):
    for sent in nltk.sent_tokenize(sentence):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                print(chunk.label(), ' '.join(c[0] for c in chunk))

# if __name__ == "__main__":
#     url = 'https://www.nytimes.com/2019/10/16/world/asia/hong-kong-protests-carrie-lam.html'
#     #url='https://www.nytimes.com/2019/10/15/world/asia/kashmir-militants.html'
#     respond = requests.get(url)
#     data = respond.text

#     article = TextSummary()
#     text, title = article.get_paragraph_content(data)
#     summary = article.summarize_text(text)
#     clean_title = re.sub('\W+', ' ', title)

#     print('\033[4m' + title + '\033[0m')
#     print(summary)


#     tokenizer = nltk.SpaceTokenizer()
#     sentence=summary
#     #toks = tokenizer.tokenize(sentence)
#     toks=nltk.word_tokenize(sentence)
#     pos = nltk.pos_tag(toks)
#     chunked_nes = nltk.ne_chunk(pos)
#     nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
#     x=" ".join(nes)
#     #x=re.findall(r"[^()0-9-]+", x)
#     words=nltk.word_tokenize(x)
#     print("\n", 'Entities: ', words)
#     print('\n')

#     # Entity dict:
#     #   Keys: entities
#     #   Values: lists of strings
#     #       Each string includes entity + five words before + five words after
#     tokens = nltk.word_tokenize(text)
#     tokenized_text = nltk.Text(tokens)
#     entitydict = {}

#     #extracts the surrounding words
#     for entity in words:
#         old_stdout = sys.stdout
#         mystdout = StringIO()
#         sys.stdout = mystdout
#         tokenized_text.findall("<.*><.*><.*><.*><.*><{}><.*><.*><.*><.*><.*>".format(entity))
#         sys.stdout = old_stdout
#         surrounding_words = mystdout.getvalue()
#         surrounding_words = surrounding_words.replace('\n', ' ')
#         surrounding_words_list = surrounding_words.split('; ')
#         entitydict[entity] = surrounding_words_list

#     print(entitydict)
#     print('\n')
#     words = list(dict.fromkeys(words))
#     ent = entities(words)
#     list_ent=[]
#     for i in ent:
#         if i[1]=='PERSON' or i[1]=='GPE' or i[1]=='ORG':
#             list_ent.append(i)

#     print(list_ent)
#     print('\n')
#     for i in entitydict:
#         print(i,entitydict[i])

def main_func(url='https://www.nytimes.com/2019/10/16/world/asia/hong-kong-protests-carrie-lam.html'):
    # url='https://www.nytimes.com/2019/10/15/world/asia/kashmir-militants.html'
    respond = requests.get(url)
    data = respond.text

    article = TextSummary()
    text, title = article.get_paragraph_content(data)
    summary = article.summarize_text(text)
    clean_title = re.sub('\W+', ' ', title)

    # print('\033[4m' + title + '\033[0m')
    # print(summary)

    tokenizer = nltk.SpaceTokenizer()
    sentence = summary
    #toks = tokenizer.tokenize(sentence)
    toks = nltk.word_tokenize(sentence)
    pos = nltk.pos_tag(toks)
    chunked_nes = nltk.ne_chunk(pos)
    nes = [' '.join(map(lambda x: x[0], ne.leaves()))
           for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
    x = " ".join(nes)
    #x=re.findall(r"[^()0-9-]+", x)
    words = nltk.word_tokenize(x)
    # print("\n", 'Entities: ', words)
    # print('\n')

    # Entity dict:
    #   Keys: entities
    #   Values: lists of strings
    #       Each string includes entity + five words before + five words after
    tokens = nltk.word_tokenize(text)
    tokenized_text = nltk.Text(tokens)
    entitydict = {}

    # extracts the surrounding words
    for entity in words:
        old_stdout = sys.stdout
        mystdout = StringIO()
        sys.stdout = mystdout
        tokenized_text.findall(
            "<.*><.*><.*><.*><.*><{}><.*><.*><.*><.*><.*>".format(entity))
        sys.stdout = old_stdout
        surrounding_words = mystdout.getvalue()
        surrounding_words = surrounding_words.replace('\n', ' ')
        surrounding_words_list = surrounding_words.split('; ')
        entitydict[entity] = surrounding_words_list

    # print(entitydict)
    # print('\n')
    words = list(dict.fromkeys(words))
    ent = entities(words)
    list_ent = []
    for i in ent:
        if i[1] == 'PERSON' or i[1] == 'GPE' or i[1] == 'ORG':
            list_ent.append(i)

    # print(list_ent)
    # print('\n')
    for i in entitydict:
        print(i, entitydict[i])

    return list_ent[0:3]
