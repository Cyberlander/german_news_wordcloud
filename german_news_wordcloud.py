import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

urls = [
    'https://www.spiegel.de',
    'http://www.tagesschau.de/'
]





def get_spiegel_text( spiegel_soup ):
    spiegel_text= ''
    article_intro_cointainers = spiegel_soup.findAll( "", { "class":"article-intro"} )
    for container in article_intro_cointainers:
        container_text = container.get_text()
        container_text = re.sub( "\s+", " ", container_text)
        container_text = re.sub( "\[\s+Forum\s+\]", " ", container_text)
        container_text = re.sub( "\[\s+Video\s+\]", " ", container_text)
        container_text = re.sub( "mehr\.\.\.", " ", container_text)
        spiegel_text = spiegel_text + container_text
    return spiegel_text


def get_tagesschau_text( tagesschau_soup ):
    tagesschau_text = ''
    articles_tagesschau = tagesschau_soup.findAll("p", { "class":"teasertext"})
    for article in articles_tagesschau:
        tagesschau_article_text =  article.get_text()
        tagesschau_article_text = re.sub( "\s+", " ", tagesschau_article_text)
        tagesschau_article_text = re.sub( "\s+\|\s+mehr", "", tagesschau_article_text)
        tagesschau_article_text = re.sub( "\s+\|\s+ard-text", "", tagesschau_article_text)
        tagesschau_article_text = re.sub( "\s+\|\s+blog", "", tagesschau_article_text)
        tagesschau_article_text = re.sub( "\s+\|\s+wdr", "", tagesschau_article_text)
        tagesschau_article_text = re.sub( "\s+\|\s+Bildquelle:\s+dpa", "", tagesschau_article_text)
        tagesschau_article_text = re.sub( "\s+\|\s+video", "", tagesschau_article_text)
        tagesschau_text = tagesschau_text + tagesschau_article_text
    return tagesschau_text


def remove_common_words( gesamt_text ):
    common_words = ["Der","Die","Das","Von","Sie","Ein","nicht","Nun","neue",
        "doch","ARD","Sogar","Und","Vor","dabei","Doch","ist","Aber"]
    gesamt_text_words = gesamt_text.split()
    gesamt_text_clean = [ x for x in gesamt_text_words if not x in stops ]
    gesamt_text = ' '.join( gesamt_text_clean)
    for word in common_words:
        gesamt_text = re.sub( word, "", gesamt_text)
    return gesamt_text


if __name__ == "__main__":
    gesamt_text = ''
    stops = set(stopwords.words('german'))
    for i, url in enumerate(urls):
        uClient = urlopen( url )
        page_html = uClient.read()
        page_soup = BeautifulSoup(  page_html, 'html.parser')
        if i == 0:
            gesamt_text = gesamt_text + get_spiegel_text( page_soup )
        if i == 1:
            gesamt_text = gesamt_text + get_tagesschau_text( page_soup )
    gesamt_text = remove_common_words( gesamt_text )
    wordcloud = WordCloud().generate( gesamt_text )
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
