from TwitterAPI import TwitterAPI, TwitterPager
from textblob import TextBlob, Word
from textblob.np_extractors import ConllExtractor
import csv
from candidate import candidate, Tweet
import re

api = TwitterAPI("*** consumer_key ***", 
                 "*** consumer_secret ***",
                 "*** access_token_key ***",
                 "*** access_token_secret ***"
                 )
currentAPI = 'statuses/user_timeline'

# These are the Tweet IDs for approximately the beginning and end of October for the years being examined
# These were necessary because of limitations to Twitters API's. 
# Specifically, there are limits to # of Tweets gathered, and grabbing Tweets from a particular date range
ID_Ranges = {
	'start': {
		'2010': 26124748139,
		'2012': 252990347335049217,
		'2014': 517414424190402560,
		'2016': 782301236079058946,
		'2018': 1046861591029977089
	},
	'end': {
		'2010': 28938037848,
		'2012': 262340009770745857,
		'2014': 526842681151217665,
		'2016': 791769799646912512,
		'2018': 1056230463235387393
	}
}

# Used when writing candidate information to CSV
header = ["Candidate Name", "Year", "District 1", 
"District 2", "District 3", "District 4", 
"District 5", "District 6", "District 7", 
"District 8", "Total Tweets", "Total Favorites", "Total Retweets",
"Average Favorites", "Average Retweets", 
"Average Polarity", "Average Subjectivity"]

# Parts of Speech that will be extracted from Tweet content
pos = ['NN', 'NNS', 'NNP', 'NNPS'] # Noun, plural noun, proper noun, plural proper noun

# These will be collecting the terms extracted from the Tweet
# They will be written to a CSV for each year
importantTerms = {
'2018': {},
'2016': {},
'2014': {},
'2012': {}
}

# These are garbage words from Tweets. This list was used to manually remove some
# of the information that will not be useful
garbageFilter = ['i hope', 'the...', 'weeks', 'victory', 're', 
'is...','days','service','to...','folks','i \'m','life',
'evening','things','th...','thanks','tune','security',
'great time','everything','way','today','and...','great news',
'year','tomorrow','s','week','time','vikings','yesterday',
'race','i  m','day','i \'ve','need','thousands',
'friends','visit','lunch','morning','tune','night',
'support','forum','mn06 http','saturday',
'check','tour','middle','fire','meeting','dailyagendamn',
'lake','tcot','door','rapids','pete','show','rally','people']

# --------------- Data Setup Start --------------- #

extractor = ConllExtractor()
candidateHandles = {} # Dictionary of Twitter Handles
candidateList = [] # List of Candidates
listOfTweets = [] # List of Tweets

# Reads in file of candidates, their district, and the election year
def getCandidates():
	with open('Candidates.csv', mode='rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		line_count = 0
		for row in reader:
			if line_count == 0: # skip header row
				line_count += 1
			else:
				name = row[0][:-4] # This removes the last 4 characters from their name.. i.e. (R) or (D)
				party = row[0][len(name)+1:]
				if party == '(I)': continue # We are priarily looking at the two major parties

				cand = candidate()
				cand.setProps(name, row[1], row[2])
				line_count += 1
				candidateList.append(cand)
	print('Finished reading in candidates.\n')


# Creates dictionary of candidates and their Twitter handles
def createDictionary():
	with open('CandidateTwitters.csv', mode='rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		line_count = 0
		for row in reader:
			if line_count == 0:
				line_count += 1
			else:
				candidateHandles[row[0]] = row[1]
	print('Finished creating dictionary.\n')


# Nice section divider for cleaning up console output
def sectionDivider(beginEnd):
	print '\n--------------- ',beginEnd,' ---------------\n'


# Used for printing Tweet fields
def printTypes(item):
	for i in item:
		print (i)

# --------------- Data Setup End --------------- #



# --------------- Data Gathering Start --------------- #

# NLP for breaking apart Tweets for various parts of speech
def getContent(tweet):
	txt = TextBlob(tweet['text'].split('https', 1)[0], np_extractor=extractor)
	txt = txt.lower()
	NP = txt.noun_phrases
	Subj = txt.pos_tags
	sentiment = txt.sentiment

	# Convert Noun Phrases from unicode to str before adding
	npToAdd = list()
	for np in NP:
		np = np.encode('ascii','ignore')
		npToAdd.append(np)

	# Filter words for greater importance (nouns, proper nouns, etc.)
	SubjToAdd = list()
	for word in Subj:
		# print word
		if word[1] in pos: # Looking for nouns, or subject (i.e. movie, music, color)
			SubjToAdd.append(word)	

	# Create new Tweet objects
	twt = Tweet()
	twt.addNew(tweet, npToAdd, SubjToAdd, sentiment)
	listOfTweets.append(twt)


# Used for gathering Tweets
def getTweets(handle, year, num):
	print 'Getting some Tweets for you...'
	pager = TwitterPager(api, 
                     currentAPI, 
                     {'screen_name': handle, 
                     'count': num, 
                     'include_rts': False,
                     'exclude_replies': True,
                     '' 
                     'since_id': ID_Ranges['start'][year], 
                     'max_id': ID_Ranges['end'][year]
                     })
	count = 0
	for item in pager.get_iterator(wait=3.5):
		if count >= num: 
			break # limit the number of tweets for the moment
		if 'text' in item:
			getContent(item)
			count = count + 1
		elif 'message' in item:
			print (item['message'])
			break
	# Add ListofTweets[] to specific candidate
	try:
		for c in candidateList:
			if (c.name == listOfTweets[0].author) and (c.electionYear == year):
				c.addTweets(listOfTweets)
				break
	except:
		print 'Error: Could not Find Candidate'


def isDistrict(num, dist):
	if num == dist:
		return 1
	else: return 0


def Average(x, y):
	return x / y


def writeCSV():
	# Handles a full list of candidates
	# can = listOfCandidates # 1 single candidate for test

	with open('Candidate_Test.csv', mode='w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(header)

		for c in candidateList:
			toAdd = []
			toAdd.append(c.name)
			toAdd.append(c.electionYear)
			# Loop fills in District numbers.
			# 0 means not from district, 1 means they are from district
			for i in range(1,9):
				toAdd.append(isDistrict(int(c.district),i))
			
			num = c.tweetNum()
			if num == 0:
				print 'No Tweets for',c.name
				continue
			try:
				totalFav = 0
				totalRt = 0
				totalPol = 0
				totalSubj = 0
				for tw in c.tweets:
					totalFav += tw.favorites
					totalRt += tw.retweets
					totalPol += tw.sentiment[0]
					totalSubj += tw.sentiment[1]

				toAdd.append(num)
				toAdd.append(totalFav)
				toAdd.append(totalRt)
				toAdd.append(Average(totalFav,num))
				toAdd.append(Average(totalRt,num))
				toAdd.append(Average(totalPol,num))
				toAdd.append(Average(totalSubj,num))

			except:
				print 'Could not get metrics for ',c.name

			writer.writerow(toAdd)

def writeWords(year):
	filename = str(year)+'Words.csv'
	with open (filename, mode='w') as csv_file:
		writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(['Term', 'Count'])

		for c in candidateList:
			if len(c.tweets) == 0:
				continue
			try:
				if c.electionYear == year:
					for t in c.tweets:
						for w in t.partsOfSpeech:
							try:
								if str(w) in garbageFilter: continue
								w = re.sub('[!@#$].','', w)
								w = re.sub('http','',w)
								w = w.strip()
								if len(w) < 3: # Should filter some words such 'the', and the like
									continue
								if w in importantTerms[year]:
									importantTerms[year][w] += 1
								else:
									importantTerms[year][w] = 1
							except: continue
						for w in t.nounPhrases:
							try:
								if str(w) in garbageFilter: continue
								w = re.sub('[!@#$].','',w)
								w = re.sub('http','',w)
								w = w.strip()
								if w in importantTerms[year]:
									importantTerms[year][w] += 1
								else:
									importantTerms[year][w] = 1
							except: continue
			except:
				print 'Error: Could not complete writing terms.'

		# Actually write to CSV now
		for key in importantTerms[year].keys():
			if importantTerms[year][key] > 13:
				writer.writerow([key.encode("utf-8"),importantTerms[year][key]])
		

# --------------- Data Gathering End --------------- #



# ---------------  MAIN  --------------- #

def getOne():
	printCand = raw_input('Print List of Candidates? (y/n): ')
	if printCand == 'y':
		print("Printing Candidate List: ")
		for c in candidateList:
			c.printBasicInfo()
	elif printCand == 'n': print('Sounds good.')
	
	print '\nTime to go get some tweets. Please wait...'

	# Create dictionary of candidate Twitter Handles
	if not candidateHandles:
		createDictionary()

	choice = True
	while choice:
		who = raw_input('Who would you like to get tweets from? ')
		if candidateHandles[who] == 'NA':
			print 'Candidate has no twitter'
			continue
		else: choice = False

	year = raw_input('What year are you interested in? ')

	many = raw_input('How many Tweets would you like? ')
	numTweets = int(many)

	getTweets(candidateHandles[who], year, numTweets)

	print 'Got some Tweets for you.'
	prnt = raw_input('Would you like to print the tweets? (y/n): ')
	if prnt == 'y':
		for tw in listOfTweets:
			sectionDivider('Begin Tweet')
			tw.printTweet()
			sectionDivider('End Tweet')

	for c in candidateList:
		if c.name == who:
			if c.electionYear == year:
				c.printFullCandidate()
				break

	wri = raw_input('Would you like to write out data to CSV? (y/n): ')
	if wri == 'y':
		for c in candidateList:
			if c.name == who:
				writeCSV()
				break


def getAll():
	numTweets = 300
	print 'I am going to get all Tweets.'
	print 'This may take a while. Starting loop...'
	for c in candidateList:
		del listOfTweets[:]
		who = c.name
		if candidateHandles[who] == 'NA':
			print 'Candidate has no twitter'
			continue
		year = c.electionYear
		if c.name not in candidateHandles:
			print(c.name,' is not in candidateHandles')
			continue
		getTweets(candidateHandles[who], c.electionYear, numTweets)
		c.printFullCandidate()

	write = True
	while write:
		io = raw_input('Do you want to write a CSV of data? (y/n): ')
		if io == 'y':
			print 'Writing CSV..'
			writeCSV()
			print 'Done.'
		elif io == 'n':
			write = False

	terms = raw_input('Do you want to produce terms? (y/n): ')
	if terms == 'y':
		writeWords('2018')
		writeWords('2016')
		writeWords('2014')
		writeWords('2012')
		print 'Done.'



def main():
	many = raw_input('How many candidates would you like? (one or all): ')
	getCandidates()
	createDictionary()
	menu = True
	while menu:
		if many == 'one':
			getOne()
			menu = False
		elif many == 'all':
			getAll()
			menu = False
		else:
			menu = True
			continue

main()

