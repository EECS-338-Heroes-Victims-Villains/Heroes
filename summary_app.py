import os
import requests
import re
from text_summary import TextSummary
from nltk import *
from nltk.tokenize import SpaceTokenizer
import nltk


os.system('cls' if os.name == 'nt' else 'clear')


#basically extracts the entities 
def get_entities(args):
    qry = args
    tokens = nltk.tokenize.word_tokenize(qry)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    print(sentt)
    person = []
    for subtree in sentt.subtrees(filter=lambda t: t.node == 'PERSON'):
        for leave in subtree.leaves():
            person.append(leave)
    print("person=", person)

if __name__ == "__main__":
    url = 'https://www.nytimes.com/2019/10/16/world/asia/hong-kong-protests-carrie-lam.html'
    #url='https://www.nytimes.com/2019/10/15/world/asia/kashmir-militants.html'
    respond = requests.get(url)
    data = respond.text

    article = TextSummary()
    text, title = article.get_paragraph_content(data)
    summary = article.summarize_text(text)
    clean_title = re.sub('\W+', ' ', title)

    print('\033[4m' + title + '\033[0m')
    print(summary)

    # if you want to save the summary into a text file:
    # uncomment the following:
    with open("sample_output/{}.txt".format(clean_title[:20].replace(" ", "_")), "w") as f:
        f.writelines(title + '\n')
        f.writelines('\n')
        f.writelines(summary)


    tokenizer = SpaceTokenizer()
    sentence=summary
    toks = tokenizer.tokenize(sentence)
    pos = pos_tag(toks)
    chunked_nes = ne_chunk(pos)
    nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
    x=" ".join(nes)
    #x=re.findall(r"[^()0-9-]+", x)
    words=nltk.word_tokenize(x)
    words = list(dict.fromkeys(words))
    print("\n",words)
