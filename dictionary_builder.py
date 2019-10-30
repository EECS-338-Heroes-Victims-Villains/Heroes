import json
import csv
import requests
import random
import sys

URL = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
KEY = "e3bb7ff3-587b-4fab-92a0-789dc76c0d22"


def dict_build(word):
    ret = []
    req = requests.get(URL+word+"?key="+KEY)
    data = req.json()
    for group in data[0]["meta"]["syns"]:
        ret.extend(group)
    return ret


if __name__ == "__main__":
    dictionary = sys.argv[1]+"_dictionary.csv"
    temp_dict = []
    more_words = []
    with open(dictionary, mode='r') as csv_file:
        csv_read = csv.DictReader(csv_file)
        for row in csv_read:
            temp_dict.append(row["Word"])
    n = 50
    choices=[]
    choice=random.choice(temp_dict)
    while n:
        while choice in choices:
            choice = random.choice(more_words)
        more_words.extend(dict_build(choice))
        choices.append(choice)
        n -= 1
    with open(dictionary, mode='a') as csv_file:
        csv_write = csv.writer(csv_file)
        for word in more_words:
            if word not in temp_dict:
                temp_dict.append(word)
                csv_write.writerow([word])
