#!/usr/bin/python
import MySQLdb
from bs4 import BeautifulSoup
import urllib
import time

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="", # your password
                      db="lonleyplanetData",
                      unix_socket="/opt/lampp/var/mysql/mysql.sock"
                     ) # name of the data base

# you must create a Cursor object. It will let
#  you execute all the query you need

seasons = ['hot', 'rain', 'wet', 'rainy', 'monsoon', 'spring', 'summer', 'winter', 'dry']
cur = db.cursor()

cur.execute('SELECT id,country,weather,wheretogo FROM weatherinfo where id > 1')

k = 0

for i in cur.fetchall():
    text = i[2] + i[3]
    text = text.lower()

    cseasons = ''

    for season in seasons:
        if season in text:
            cseasons += season + ','

    Query = 'UPDATE weatherinfo SET seasons = %s where id = %s'; 

    try:
        cur.execute(Query, (cseasons, i[0]))
        db.commit()
    except:
        db.rollback()
        print 'rollback'
    k += 1
    


'''
for i in cur.fetchall():
    if i[1] == '':
        continue
    
    country = i[0]
    
    if country == 'United States': country = 'usa'

    country = i[0].replace(" ","-")

    print country +' : '+i[1]
    
    
    url = 'http://www.lonelyplanet.com/' + i[1] + '/weather'


    file_pointer = urllib.urlopen(url)

    if file_pointer.getcode() == 404:
        continue

        

    
    soup = BeautifulSoup(file_pointer)
    h3 = soup.select('#contentBody h3:nth-of-type(1)')

    if len(h3)>0:
        h3 =  h3[0].contents[0].encode('utf8')
    else:
        h3 = 'no'
    
    h2 = soup.select('#contentBody h2:nth-of-type(1)')
    if h2 != None and len(h2)>0:
        h2 = h2[0].contents[0].encode('utf8')
    else:
        h2 = 'no'
        
    p = soup.select('#contentBody p')
    
    info = {}
    info[h2] = 'Nothing'
    s = 0
    if h2 != 'no':
        info[h2] = p[0].contents[0].encode('utf8')
        s = 1
        
    info[h3] = ''
    if h3 != 'no':
        for j in range(s, len(p)):
            if len(p[j].contents) > 0:
                info[h3] = info[h3] + ' ' + p[j].contents[0].encode('utf8')
    else:
        for j in range(s, len(p)):
            if len(p[j].contents) > 0:
                info[h2] = info[h2] + ' ' + p[j].contents[0].encode('utf8')

    Query = '';
    Query = 'INSERT INTO weatherinfo (country, weather, wheretogo)'
    Query += " VALUES(%s,%s,%s)"

    try:
        cur.execute(Query, (i[0], info[h2], info[h3]))
        db.commit()
    except:
        db.rollback()
        print 'rollback'
        
    time.sleep(3)
'''
