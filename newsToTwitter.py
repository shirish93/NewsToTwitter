

from newsMiner import getEkantipurLinks, fetchEkanArticles, getRepublicaLinks,getRepublicaArticles

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

path = ''
#path = '/h/spokha01/runningBots/newsToTwitter/'
def articleToNames(article):
  '''Takes an article, and extracts as many person names as possible,
  returns a list of names. For a proper noun to be a 'name', it
  must be more than one word.
  '''
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


def getPeople():
    '''Returns the name-> twitter ID mapping of popular people.

    '''
    f = open(path+'nameToUname.txt', 'r')
    names = [(each.split(':')[0], each.split(':')[1]) for each in f]
    f.close()
    return names

def peopleConversion(allTexts):
    '''Taaes a list of articles, and then returns a list of sentences
    that mention the people we have in our database.

    '''
    matches=[]
    names = getPeople()
    for person in names:
        for article in allTexts:
            try:
                indexOf = article.lower().index(person[0].lower())
                if indexOf!=-1:
                    wanted = article[indexOf-70:indexOf+70]
                    if '.' in wanted and wanted.index('.')<wanted.lower().index(person[0].lower()):
                        wanted = wanted[wanted.index('.')+1:wanted.rindex(' ')]
                    else:
                        wanted = wanted[wanted.index(' '):wanted.rindex(' ')]
                    matches.append(' '.join( wanted.split())  )
            except:
                pass
    return list(set(matches))
import pdb



    
def worker(grabsLinks, fetchesArticles):
    '''Takes to functions: one that returns a list of wanted page URL's, and another
    that turns those links into articles. Returns a list of sentences
    with the names of people in the database replaced by their user names
    '''
    linksList = grabsLinks()
    articles = fetchesArticles(linksList)

    ###Below is commented out because we want 'smart' recognition of people's names
    ### and try to search the names online, see if the person matches the person
    ### in twitter, and then link those two. However, the name 'detector' is not
    ### working very well...
    '''names = [articleToNames(each[2]) for each in articles]
    completeNames = []
    for each in names:
        for name in each:
            completeNames.append(each)
    '''
    texts = [each[2] for each in articles]
    connected = peopleConversion(texts)
    # Now that we have unique lines, we just replace them with people's names
    #Since one can have more than one person, we need peopleList.
    names = getPeople()
    modded=[]
    for sent in connected:
        toGO=sent
        for name in names:
            if name[0] in sent:
                toGO=toGO.replace(name[0], name[1])
        modded.append(' '.join(toGO.split()))
    return modded

def writeToBuffer(tweets,mode='a'):
    f = open("buffer.txt", mode)
    for each in tweets:
        toWrite=str(each)+'\n'
        if len(toWrite.split())>0:
            f.write(toWrite)
    f.close()

def stealFromBuffer():
    try:
        f = open("buffer.txt", "r")
    except:
        f.close()
        return []
    tweets = [each for each in f]
    f.close()

    if tweets:
        writeToBuffer(tweets[1:],mode='w')
        return tweets[0]
    return []


import time
def postMessage(inputs):
    print inputs+'\n'

def runDaily():
    '''The driver function that 'runs' the entire thing.

    '''    
    TKP_sources = worker(getEkantipurLinks, fetchEkanArticles)
    Repub_sources = worker(getRepublicaLinks, getRepublicaArticles)
    TKP_sources.extend(Repub_sources)
    writeToBuffer(TKP_sources)
    toTweet = stealFromBuffer()
    while toTweet:
        postMessage(toTweet)
        time.sleep(60)
        toTweet = stealFromBuffer()
    


runDaily()



