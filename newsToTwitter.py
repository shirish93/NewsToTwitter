

from newsMiner import getEkantipurLinks, fetchEkanArticles

unwanted = ['centre','commission',
' bank','nepal ','international','development','.',',','court','US ','UK ' ,'league','agency',
'disaster', 'area', 'committee', 'club', 'municipality', 'commission'
'council', 'nation', 'council', 'division', 'academoy', 'mission',
'lodge', 'peace', 'world', 'stadium', 'state ', 'university', 'ministry', 'assembly', 'secretary', 'office'
,'platform', 'forum', 'tournament', ' academy', ' school', ' college'
,' university', 'union', ' court', 'assembly', ' trust', ' airlines'
,' cup', 'summit', 'union', 'region', 'police', 'army', 'constitution'
, ' party', ' affairs', 'day', 'global ', 'apf ', 'football', 'association', 'the '
, 'north ', 'south ', 'east ', 'west ', 'minister ', 'president ', 'africa '
, 'united ', 'democratic ', ' act', 'project', ' limited', 'rss', 'republica ', ' press'
]
def articleToNames(article):
  tokens=article.split( )
  names=[]
  app = True
  cur=''
  for each in tokens:
    if each and each[0].isupper():
      mode=1
      cur = cur+' '+each
    else:
      if mode==1 and cur.count(' ')>1:
        for mini_each in unwanted:
            app=True
            if mini_each in cur.lower():
                app=False
                break
        if app: names.append(cur)
        cur=''
      mode=0
  return names


def runDaily():
    linksList = getEkantipurLinks()
    articles = fetchEkanArticles(linkList)
    names = [articleToNames(each[2]) for each in articles]
    completeNames = []
    for each in names:
        for name in each:
            completeNames.append(each)
    




def peopleConversion(allTexts):
    f = open('nameToUname.txt', 'r')
    names = [(each.split(':')[0], each.split(':')[1]) for each in f]
    matches=[]
    for person in names:
        for article in allTexts:
            indexOf = article.lower().index(person[0].lower())
            if indexOf!=-1:
                wanted = article[indexOf-50:indexOf+50]
                #do something
                pass
