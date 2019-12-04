from gensim.summarization import summarize
from bs4 import BeautifulSoup
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class TextSummary:
    def __init__(self):
        return

    def get_paragraph_content(self, data):
        soup = BeautifulSoup(data, 'html.parser')
        title = soup.find('title').string
        paragraph = [p.getText() for p in soup.find_all('p')]
        whole_text = ' '.join(paragraph)
        return whole_text, title

    def summarize_text(self, text):
        return summarize(text,ratio=1,split=False)


#r=[{'text': 'This is a great tool!', 'external_id': None, 'error': False, 'classifications': [{'tag_name': 'Positive', 'tag_id': 60333048, 'confidence': 0.998}]}]
#re=r[0]
#print(re['classifications'][0]['tag_name'])

analyser = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print((str(score)))  #{'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}   (an example of what score contains)
    key=max(score.keys(), key=(lambda k: score[k]))
    val=max(score.values())
    if key=='neg':
        val=val*-1
    elif key=='neu':
        val=0   #just neutral
    elif key=='pos':
        pass
    return key,val


x=sentiment_analyzer_scores("the police kill")
print(x)