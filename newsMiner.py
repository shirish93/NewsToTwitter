import time
from bs4 import BeautifulSoup
import requests

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

