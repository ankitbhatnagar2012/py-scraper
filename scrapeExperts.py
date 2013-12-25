# Scrape script to extract all authors from Lonely Planet

import urllib
from bs4 import BeautifulSoup
import string
import io

allAuthorsList = []

# allAuthorsFile = io.open("allAuthorsFile7.txt", "w", encoding='utf8')

urlToParse = 'http://shop.lonelyplanet.com/page-1/?class=pgn-next&sortBy=DEFAULT_RANKING';

soup = BeautifulSoup(urllib.urlopen(urlToParse).read())

allProductLinks = soup.findAll('a',attrs={'class':'product-list-image'})

# scrape all book links to fetch their authors
for link in allProductLinks:
	bookLink = link['href']
	bookLinkToParse = 'http://shop.lonelyplanet.com' + bookLink

	# fetch HTML from bookLink to parse and find author/s
	specificBookSoup = BeautifulSoup(urllib.urlopen(bookLinkToParse).read())

	specificBookAuthorsDiv = specificBookSoup.findAll('div',attrs={'class':'details'})

	for div in specificBookAuthorsDiv:
		pTags = div.findAll('p')
		authorTag = pTags[1]

		allAuthors = authorTag.split(',')

		print allAuthors

		# process the first author where the word : author comes along
		firstAuthor = allAuthors[0]
		firstAuthor = firstAuthor.strip().split('\n')
		firstAuthor = firstAuthor[1].strip()
		print firstAuthor
		# allAuthorsList.append(firstAuthor)
		# allAuthorsFile.write(firstAuthor+',')

		# process the rest authors normally	
		for author in allAuthors[1:]:
			author = author.strip()
			print author
			# allAuthorsList.append(author)
			# allAuthorsFile.write(author+',')

# allAuthorsFile.close()

# print allAuthorsList


