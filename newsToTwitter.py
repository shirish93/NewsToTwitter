


for person in people:
	for article in allTexts:
		if person.lower() in article.lower():
			counter+=1
			print person+ " was found in"



unwanted = ['centre',
'commission',
' bank',
'nepal ',
'international',
'development',
'.',
',',
'court',
'US ',
'UK ' ,
'league',
'agency'
]
unwanted.extend(['disaster', 'area', 'committee', 'club', 'municipality', 'commission'
                    'council', 'nation', 'council', 'division', 'academoy', 'mission',
                    'lodge', 'peace', 'world', 'stadium', 'state ', 'university', 'ministry', 'assembly', 'secretary', 'office'
                    ,'platform', 'forum', 'tournament', ' academy', ' school', ' college'
                    ,' university', 'union', ' court', 'assembly', ' trust', ' airlines'
                    ,' cup', 'summit', 'union', 'region', 'police', 'army', 'constitution'
                    , ' party', ' affairs', 'day'])

people=[]
for each in peoples:
	put  =True
	for un in unwant:
		if un.lower() in each.lower():
			put=False
			break
	if put: people.append(each)
