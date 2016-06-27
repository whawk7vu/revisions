# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 20:40:50 2016

@author: WHawk
"""

from itertools import count
import requests
import urllib.request

with urllib.request.urlopen('http://www.bea.gov/histdata/histChildLevels.cfm?HMI=7') as response:
   html = response.read()
   
html



url = "http://www.bea.gov/histdata/histChildLevels.cfm?HMI=7"

urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)



file("my_file.txt", "w").write(urllib2.urlopen("http://www.bea.gov/histdata/histChildLevels.cfm?HMI=7").read())


#HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
URL = "http://www.bea.gov/histdata/histChildLevels.cfm?HMI=7"

# with a session, we get keep alive
session = requests.session()

for n in count():
    full_url = URL % n
    ignored, filename = URL.rsplit('/', 1)

    with file(filename, 'wb') as outfile:
        response = session.get(full_url)
        if not response.ok:
            break
        outfile.write(response.content)

