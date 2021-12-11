#!/usr/bin/env python3

import re
import random
import hashlib
from requests import sessions as rs
sreq = rs.Session()

#vars
RIP = "192.168.1.1"
USR = "user"
PWD = "user"


#Header and smth
cookies = {'_TESTCOOKIESUPPORT': '1'}

headers = {
	'Host': RIP,
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Upgrade-Insecure-Requests': '1',
	'Origin': 'http://' + RIP,
	'Content-Type': 'application/x-www-form-urlencoded',
	'Username-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Referer': 'http://' + RIP,
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Encoding': 'identity',
	'Accept-Language': 'en-US,en;q=0.8',
}

#Get token
response = sreq.get("http://"+RIP, headers=headers, cookies=cookies)
r = re.findall("Frm_Logintoken.*", response.text)
r2 = re.findall("[0-9]+", str(r))
token = r2[0]
#print("Tokennum found : " + token) #Enable for debug

#Gen random number for hash
rand = random.randint(10000000,10032767)

#Gen hash passwd sha256
pre = (PWD + str(rand)).encode()
hash = hashlib.sha256(pre)
#print("Hash generated : " + hash.hexdigest()) #Enable for debug

#Building post data for capture SID cookie
pdata = ("action=login&Username=" + str(USR) + "&Password=" + hash.hexdigest() + "&Frm_Logintoken=" + token + "&UserRandomNum=" + str(rand))
#print("Post data : " + pdata) #Enable for debug

#Processing to capture SID cookie
sreq.post('http://' + RIP, headers=headers, cookies=cookies, data=pdata)

#Go to ip info page
ipr = sreq.get('http://' + RIP + '/getpage.gch?pid=1002&nextpage=IPv46_status_wan2_if_t.gch')
if ipr.ok:
    print('\nSuccess Login !')
else:
    print('Hmm There Must Be Bug ... !')
#with open("raw.txt", "w") as file: #Enable for debug
#	file.write(ipr.text) #Enable for debug
#	file.close #Enable for debug

#Print the ip
a = re.findall("TextPPPIPAddress0.*", ipr.text)
b = re.findall("value=.*[0-9]", str(a))
c = re.findall("[0-9]+", str(b))
print("Your Ip Right Now is : " + '.'.join(c))