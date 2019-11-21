import os
import requests
import re
from text_summary import TextSummary
import spacy
import nltk
from io import StringIO
import sys
from io import StringIO
import sys
from Entity import Entity
from textblob import TextBlob


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
def main_func(url):
    #url = 'https://www.nytimes.com/2019/10/16/world/asia/hong-kong-protests-carrie-lam.html'
    # url='https://www.nytimes.com/2019/10/15/world/asia/kashmir-militants.html'
    respond = requests.get(url)
    data = respond.text

    article = TextSummary()
    text, title = article.get_paragraph_content(data)
    summary = article.summarize_text(text)
    clean_title = re.sub('\W+', ' ', title)

    print('\033[4m' + title + '\033[0m')
    print(summary)

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
    print("\n", 'Entities: ', words)
    print('\n')

    words = list(dict.fromkeys(words))
    ent = entities(words)
    list_ent = []
    for i in ent:
        if i[1] == 'PERSON' or i[1] == 'GPE' or i[1] == 'ORG':
            list_ent.append(i)

    print(list_ent)

    tokens = nltk.word_tokenize(text)
    tokenized_text = nltk.Text(tokens)

    # Extracts the surrounding words
    tokens = nltk.word_tokenize(text)
    tokenized_text = nltk.text.Text(tokens)
    entitydict = {}
    all_entities = []

    for pair in list_ent:
        # Create object
        entity = pair[0]
        new_entity_object = Entity(entity)

        # Find surrounding words
        entity_name = entity.replace(' ', '><')
        old_stdout = sys.stdout
        mystdout = StringIO()
        sys.stdout = mystdout
        tokenized_text.findall(
            "<.*><.*><.*><.*><.*><{}><.*><.*><.*><.*><.*>".format(entity_name))
        sys.stdout = old_stdout
        surrounding_words = mystdout.getvalue()
        surrounding_words = surrounding_words.replace('\n', ' ')
        surrounding_words_list = surrounding_words.split('; ')

        # Find connotations
        connotations = []
        for phrase in surrounding_words_list:
            score = TextBlob(phrase).sentiment.polarity
            connotations.append(score)

        new_entity_object.surrounding_words = surrounding_words_list
        new_entity_object.surrounding_words_connotations = connotations
        all_entities.append(new_entity_object)

    print('\n')
    vil, vic, her = ["", 0], ["", 0], ["", 0]
    for i in all_entities:
        print(i.entity_name, i.surrounding_words,
              i.surrounding_words_connotations)
        print('\n')
        for num in i.surrounding_words_connotations:
            if num < vil[1]:
                vil[0] = i.entity_name
                vil[1] = num
            elif num > her[1]:
                her[0] = i.entity_name
                her[1] = num
            elif num == 0:
                if i.surrounding_words_connotations.count(0)/len(i.surrounding_words_connotations) > vic[1]:
                    vic[0] = i.entity_name
                    vic[1] = num
    return [her[0], vic[0], vil[0]]
