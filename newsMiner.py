import time
from bs4 import BeautifulSoup
import requests
republica_base='http://www.myrepublica.com/portal/index.php?action=news_details&news_id='

def getRepublicaLinks():
    page = requests.get('http://myrepublica.com/portal/')
    soup = BeautifulSoup(page.text)
    wantedLinks = [each.get('href') for each in links
                   if each.get('href') and
                   'news_details' in each.get('href')]
    ids = [int(each.split('id=')[1]) for each in wantedLinks]
    maxID = max(ids)
    return [republica_base+str(each) for each in ids if maxID-each<110]


def getRepublicaArticles(linkList):
    toReturn=[]
    for link in linkList:
        page = requests.get(link)
        soup = BeautifulSoup(page.text)
        header = soup.find_all('span', {'class': 'bodynewsheading'})[0].text
        article = soup.find_all('div', {'class': 'mainbody'})[0].text
        parts = article.split('-->')
        meat = parts[1].split('Main Page')[0].strip()
        author = meat[0:meat.index('\n')]
        toReturn.append((header, author, meat))
        time.sleep(.2)
    return toReturn

'''
Cannot figure out Kantipur unicode issues:
content won't print, even after the decoding of
text. Will fix the issue at leisure later. -Shirish

def getKantipurLinks():
	lastDate = time.time()
	fmt='%Y/%m/%d'
	wanted=time.strftime(fmt, time.localtime(lastDate))
	URL="http://www.ekantipur.com/kantipur/archive.php"
	g = requests.post(URL, data = {'news_date': wanted})
	a = BeautifulSoup(g.text)
	links = a.find_all('a')
	wanted= [each.get('href') for each in links if 'full-story' in each.get('href')]
	return wanted
'''
def getEkantipurLinks():
	lastDate = time.time()
	fmt='%Y/%m/%d'
	wanted=time.strftime(fmt, time.localtime(lastDate))
	URL="http://www.ekantipur.com/the-kathmandu-post/archive/"
	g = requests.post(URL, data = {'news_date': wanted})
	a = BeautifulSoup(g.text)
	links = a.find_all('a')
	prevDate=lastDate-24*3600
	prevTime=time.strftime(fmt, time.localtime(prevDate))
	wanted= [each.get('href') for each in links if prevTime in each.get('href')]
	return wanted

def fetchEkanArticles(linkList):
	articles=[]
	for each in linkList:
		URL=each
		page = requests.get(URL)
		a = BeautifulSoup(page.text)
		title=a.find_all('h2')[0].text if len(a.find_all('h2'))>0 else ''
		author=a.find_all('div', {'class':'news-tool'})
		if len(author)>0:
			author=author[0].text.strip()
		else:
			author=''
		article=a.find_all('span', {'id':'detail-news'})
		if len(article)>0:
			article=article[0].text
		else:
			article=''
		if article!='':
			articles.append((title, author, article))
		time.sleep(.1)
	return articles

