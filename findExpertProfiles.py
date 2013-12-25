# Scrape script to extract all authors from Lonely Planet

import urllib
from bs4 import BeautifulSoup
import string
import io

AuthorProfileFile = io.open("authorProfileFile8.txt", "w", encoding='utf8')

urlToParse = 'http://shop.lonelyplanet.com/page-8/?class=pgn-next&sortBy=DEFAULT_RANKING';

print 'Parsing page : '+urlToParse

soup = BeautifulSoup(urllib.urlopen(urlToParse).read())

allProductLinks = soup.findAll('a',attrs={'class':'product-list-image'})

# scrape all book links to fetch their authors
for link in allProductLinks:
	bookLink = link['href']
	bookLinkToParse = 'http://shop.lonelyplanet.com' + bookLink

	# fetch HTML from bookLink to parse and find author/s
	specificBookSoup = BeautifulSoup(urllib.urlopen(bookLinkToParse).read())

	specificBookAuthorsDiv = specificBookSoup.findAll('span',attrs={'property':'dc:creator'})

	temp = {}
	writeFlag = 0

	for div in specificBookAuthorsDiv:
		aTags = div.findAll('a')
		for aTag in aTags:

			writeFlag = 0

			authorName = aTag.getText()
			temp['name'] = authorName

			# author profile page 
			authorProfile = aTag['href']

			# scrape author's profile page to fetch information
			specificAuthorSoup = BeautifulSoup(urllib.urlopen(authorProfile).read())

			authorDetails = specificAuthorSoup.findAll('ul',attrs={'class':'memberDetail'})

			temp['website'] = '[Not Found]'
			temp['twitter'] = '[Not Found]'

			for authorDetail in authorDetails:
				liTags = authorDetail.findAll('li')
				for li in liTags:
					liText = li.getText()
					liText = liText.split(' ')
					if liText[0] == 'Website':
						# print 'Website : ' + liText[1]
						temp['website'] = liText[1]
						writeFlag = 1
					if liText[0] == 'Twitter':
						# print 'Twitter : ' + liText[1]
						temp['twitter'] = liText[1]	
						writeFlag = 1

			# write to file if all details found
			if writeFlag == 1:
				# print 'writing entry...'
				stringToWrite = temp['name'] + ',' + temp['website'] + ',' + temp['twitter'] + '\n'
				print stringToWrite
				AuthorProfileFile.write(stringToWrite)			


AuthorProfileFile.close()

print 'Parsing complete!'

