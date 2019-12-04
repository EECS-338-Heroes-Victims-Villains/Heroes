import os
import requests
import re
from text_summary import TextSummary
import spacy
import nltk
from io import StringIO
import sys
from textblob import TextBlob

os.system('cls' if os.name == 'nt' else 'clear')

def entities(list_string):
    nlp = spacy.load('en')
    sentence=' '.join(list_string)
    doc = nlp(sentence)
    # document level
    ents = [(e.text, e.label_) for e in doc.ents]
    return ents

def get_labels(sentence):
    for sent in nltk.sent_tokenize(sentence):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                print(chunk.label(), ' '.join(c[0] for c in chunk))


if __name__ == "__main__":
    #url = 'https://www.nytimes.com/2019/10/16/world/asia/hong-kong-protests-carrie-lam.html'
    #url='https://www.nytimes.com/2019/11/18/world/africa/drone-strikes-isis-libya.html?action=click&module=MoreInSection&pgtype=Article&region=Footer&contentCollection=Africa'
    #url='https://www.history.com/topics/21st-century/obama-announces-death-of-osama-bin-laden-video' #WORKING
    #url='https://www.nytimes.com/2019/10/15/world/asia/kashmir-militants.html'   #WORKING
    url='https://www.usatoday.com/story/news/nation/2019/02/23/schlitterbahn-waterslide-charges-dismissed-caleb-schwabs-death-verruckt/2963747002/?fbclid=IwAR20QSRyvNZ-CB1rdbY4jsNrpJ5HGA5vka_YXU0QsGpmTFXlKR79JPoSUTI'  #water slide working
    respond = requests.get(url)
    data = respond.text

    article = TextSummary()
    text, title = article.get_paragraph_content(data)
    summary = article.summarize_text(text)
    clean_title = re.sub('\W+', ' ', title)

    print('\033[4m' + title + '\033[0m')
    print(summary)


    tokenizer = nltk.SpaceTokenizer()
    sentence=summary
    #toks = tokenizer.tokenize(sentence)
    toks=nltk.word_tokenize(sentence)
    pos = nltk.pos_tag(toks)
    chunked_nes = nltk.ne_chunk(pos)
    nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
    x=" ".join(nes)
    #x=re.findall(r"[^()0-9-]+", x)
    words=nltk.word_tokenize(x)
    print("\n", 'Entities: ', words)
    print('\n')

    # Entity dict:
    #   Keys: entities
    #   Values: lists of strings
    #       Each string includes entity + five words before + five words after
    tokens = nltk.word_tokenize(text)
    tokenized_text = nltk.Text(tokens)
    entitydict = {}

    #extracts the surrounding words
    for entity in words:
        old_stdout = sys.stdout
        mystdout = StringIO()
        sys.stdout = mystdout
        tokenized_text.findall("<.*><.*><.*><.*><.*><{}><.*><.*><.*><.*><.*>".format(entity))
        sys.stdout = old_stdout
        surrounding_words = mystdout.getvalue()
        surrounding_words = surrounding_words.replace('\n', ' ')
        surrounding_words_list = surrounding_words.split('; ')
        entitydict[entity] = surrounding_words_list

    #entitites that we want to rank (these are basically nouns/proper nouns
    print(entitydict)
    print('\n')
    words = list(dict.fromkeys(words))
    ent = entities(words)
    list_ent=[]
    for i in ent:
        if i[1]=='PERSON' or i[1]=='GPE' or i[1]=='ORG':
            list_ent.append(i)

    print(list_ent)
    #print('\n')
    #for i in entitydict:
     #   print(i,entitydict[i])
    entity_names=[]
    for i in list_ent:
        entity_names.append(i[0])
    entity_dictionary={key:0 for key in entity_names}
    print(entity_dictionary)
    for i in entitydict:
        score=TextBlob(str(entitydict[i])).sentiment
        #score=sentiment_analyzer_scores(str(entitydict[i]))
        for j in entity_names:
            if j.find(i):
                entity_dictionary[i]=entity_dictionary.get(j)+score[0]
                #entity_dictionary[i]=entity_dictionary.get(j)+score
        print(i,entitydict[i],score[0])  #for textblob
        #print(i,entitydict[i],score)
    print(entity_dictionary)

    '''
    from monkeylearn import MonkeyLearn
    ml = MonkeyLearn('580b39862fa9b8af93a4bf37cd0d256832275a93')
    #data = ["This is a great tool!"]
    database=[]
    model_id = 'cl_pi3C7JiL'
    for i in entitydict:
        try:
            result = ml.classifiers.classify(model_id, entitydict[i])
            r=result.body[0]
            tag=r['classifications'][0]['tag_name']
            print(i,tag)
        except TypeError:
            pass
    '''
    #finding the hero and villain (entitiy with max and lowest score)
    hero_key=max(entity_dictionary.keys(), key=(lambda k: entity_dictionary[k]))
    villain_key=min(entity_dictionary,key=lambda k:entity_dictionary[k])
    print("The Hero is: ", hero_key)
    print("The Villain is: ",villain_key)

