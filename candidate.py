
# Some utility functions will go here. 
# These will mostly be for printing stuff

# Prints lists.. pretty straight forward
def printList(lst):
	if not lst: 
		print ('No list to print here...')
	else:
		for i in lst:
			print i,',',

# Simple function for finding the average value two numbers
def Average(x, y):
	return x / y



# This is a Candidate class
# This class will represent each candidate (multi-year candidates will be stored as separate objects)
# Eventually, these will be read into a csv file and exported for further analysis
class candidate:
	def _init_(self, name, dist, year):
		self.name = name
		self.electionYear = year
		self.district = dist
		self.tweets = []

	def setProps(self, n, d, y):
		self.name = n
		self.electionYear = y
		self.district = d
		self.tweets = []

	def addTweets(self, Tweets):
		# print 'Adding Tweets to candidate Tweet List'
		for t in Tweets:
			self.tweets.append(t)

	def printBasicInfo(self):
		print '\n',self.name
		print 'District: ' + str(self.district)
		print 'Year: ' + str(self.electionYear)

	def tweetNum(self):
		return len(self.tweets)

	# printFullCandidate will print every aspect of a candidate
	def printFullCandidate(self):
		self.printBasicInfo()
		num = self.tweetNum()
		if num == 0:
			print 'Candidate has no Tweets'
			return
		totalFav = 0
		totalRt = 0
		totalPol = 0
		totalSubj = 0
		for tw in self.tweets:
			totalFav += tw.favorites
			totalRt += tw.retweets
			totalPol += tw.sentiment[0]
			totalSubj += tw.sentiment[1]

		print '\nNumber of Tweets: ',num
		print 'Favorites and Retweets:'
		print '\tAverage Favorites: ',Average(totalFav,num)
		print '\tAverage Retweets: ',Average(totalRt,num)
		print 'Sentiment:'
		print '\tPolarity: ',Average(totalPol,num)
		print '\tSubjectivity: ',Average(totalSubj,num)

	# Nearly the same as printFullCandidate(), just returns info instead
	def getMetrics(self):
		toReturn = [] # Information to return

		num = self.tweetNum()
		totalFav = 0
		totalRt = 0
		totalPol = 0
		totalSubj = 0
		for tw in self.tweets:
			totalFav += tw.favorites
			totalRt += tw.retweets
			totalPol += tw.sentiment[0]
			totalSubj += tw.sentiment[1]

		toReturn.append(num)
		toReturn.append(totalFav)
		toReturn.append(totalRt)
		toReturn.append(Average(totalFav,num))
		toReturn.append(Average(totalRt,num))
		toReturn.append(Average(totalPol,num))
		toReturn.append(Average(totalSubj,num))

		return toReturn


# This is a Tweet class
# This class wil hold all relevant information for each specific Tweet
# These will be placed into Tweet lists for each candidate (and year, if applicable)

class Tweet:
	def _init_(self):
		self.author = ''
		self.content = ''
		self.favorites = 0
		self.retweets = 0
		self.nounPhrases = list()
		self.partsOfSpeech = list()

	def addNew(self, tweet, np, pOs, sentiment):
		self.author = tweet['user']['name']
		self.content = tweet['text']
		self.favorites = tweet['favorite_count']
		self.retweets = tweet['retweet_count']
		self.date = tweet['created_at']
		self.sentiment = sentiment
		self.addNP(np)
		self.addPoS(pOs)

	def addNP(self, NPs):
		self.nounPhrases = list()
		for np in NPs:
			self.nounPhrases.append(np)
			# print 'Adding item to NP list..'

	def addPoS(self, pos):
		self.partsOfSpeech = list()
		for p in pos:
			self.partsOfSpeech.append(p[0])
			# print 'Adding item to POS list..'

	def printTweet(self):
		print self.author,' tweeted: \n\n', self.content, '\n\n at: \n\t', self.date
		print '\n',self.author,' received: '
		print 'Retweets: ',self.retweets
		print 'Favorites: ',self.favorites
		print 'Noun Phrases: '
		printList(self.nounPhrases)
		print '\nParts of Speech: '
		printList(self.partsOfSpeech)
		print '\n',self.sentiment

