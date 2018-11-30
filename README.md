# candidate-twitter-analysis

# Congressional Candidate Twitter Scraping and NLP Analysis

This Python program was originally written to gather Twitter data from candidates running for office in each of 8 congressional districts in Minnesota to use as part of a statistical model for predicting voter turnout in the 2018 Midterm Election. While it was originally written for Minnesota (which has 8 congressional districts), it could easily be changed to accommodate different numbers of districts.

This works with Python 2.x versions currently (tested on 2.7).

# Important Notes:
- Code is annotated with many comments. Please read them.
- The program requires input files (there are examples provided)
- API keys will need to be filled in with your own

# How to Run (after required installations):

In a Terminal: 
	$ python2.7 twitter.py


# To use the program, you will need to have several things installed:

1. TwitterAPI: 
	- First, in order to use this package or any of the APIs, you must have a developer account with Twitter. You can request a developer account from their website. and 
	- Next, you will need to create a project in order to get API keys. They will also ask for justification when creating a developer account/project.
	- Install a package called TwitterAPI by geduldig (https://github.com/geduldig/TwitterAPI). This will allow you to send requests to the API of your choice and receive data. They give instructions on how to install it.
	- ** Important ** You will need to specify your consumer_key, consumer_secret, access_token_key, and access_token_secret in order to utilize the APIs

2. TextBlob: 
	- This is a Natural Language Processing package and is used for gathering important information from the body of the Tweet.
	- You can find installation instructions and documentation here: 
		https://textblob.readthedocs.io/en/dev/install.html#with-conda

	Note:
		- You may need to install other dependencies such as Anaconda for the installation process
		- An older version of Python is required -- I am using a version of Python 2.7


# Input: There are example files available of the necessary inputs

	1. Candidates.csv : 
		 - This CSV has three columns: This will be used to create Candidate objects
		 		1. FirstLastP (Candidate Name and party affiliation 
		 		2. (Congressional) District
		 		3. Year

	2. CandidateTwitters.csv : Will be used to create a dictionary of names and Twitter handles
		- This CSV has two columns:
				1. Name
				2. Twitter Handle




Last Updated: 11/29/2018
