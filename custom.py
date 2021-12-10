#!/usr/bin/env python3

import re
import random
import hashlib
import requests
import time
import os
from requests import sessions as rs
sreq = rs.Session()

#vars
RIP = "192.168.1.1"
USR = "user"
PWD = "user"

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
	'Accept-Encoding': 'gzip, deflate, identity',
	'Accept-Language': 'en-US,en;q=0.8'
}


def reboot() :
    response = sreq.get("http://" + RIP, headers=headers, cookies=cookies)
    r = re.findall("Frm_Logintoken.*", response.text)
    r2 = re.findall("[0-9]+", str(r))
    token = r2[0]
    rand = random.randint(10000000, 10032767)
    pre = (PWD + str(rand)).encode()
    hash = hashlib.sha256(pre)
    pdata = ("action=login&Username=" + str(USR) + "&Password=" + hash.hexdigest() + "&Frm_Logintoken=" + token + "&UserRandomNum=" + str(rand))
    sreq.post('http://' + RIP, headers=headers, cookies=cookies, data=pdata)
    stoken = sreq.get('http://' + RIP + '/getpage.gch?pid=1002&nextpage=IPv46_status_wan2_if_t.gch', headers=headers, cookies=cookies)
    a1 = re.findall("var session_token.*", stoken.text)
    b1 = re.findall("=.*[0-9]", str(a1))
    c1 = re.findall("[0-9]+", str(b1))
    d1 = c1[0]
    rpdata = ("IF_ACTION=devrestart&IF_ERRORSTR=SUCC&IF_ERRORPARAM=SUCC&IF_ERRORTYPE=-1&flag=1&_SESSION_TOKEN=" + d1)
    sreq.post("http://" + RIP + "/getpage.gch?pid=1002&nextpage=manager_dev_conf_t.gch", headers=headers, cookies=cookies, data=rpdata)

def ip() :
    response = sreq.get("http://"+RIP, headers=headers, cookies=cookies)
    r = re.findall("Frm_Logintoken.*", response.text)
    r2 = re.findall("[0-9]+", str(r))
    token = r2[0]
    rand = random.randint(10000000,10032767)
    pre = (PWD + str(rand)).encode()
    hash = hashlib.sha256(pre)
    pdata = ("action=login&Username=" + str(USR) + "&Password=" + hash.hexdigest() + "&Frm_Logintoken=" + token + "&UserRandomNum=" + str(rand))
    sreq.post('http://' + RIP, headers=headers, cookies=cookies, data=pdata)
    ipr = sreq.get('http://' + RIP + '/getpage.gch?pid=1002&nextpage=IPv46_status_wan2_if_t.gch').text
    a = re.findall("TextPPPIPAddress0.*", ipr)
    b = re.findall("value=.*[0-9]", str(a))
    c = re.findall("[0-9]+", str(b))
    print(".".join(c))

pi = requests.get("http://ipv4.icanhazip.com").text

w = 1
while w < 2 :
    print("\nPlease noted if this is not always work\nand if this have same ip but not still not cannot be accessed plz reboot again without this script\nor just use reboot.py\n\n")
    time.sleep(15)
    print("ping to router")
    if os.system("ping -q -c 1 " + RIP + " 2>&1") == 0 :
        print("Connection reached")
        if os.system("ping -q -c 1 google.com" + " 2>&1") == 0 :
            if not ip() == print(pi) :
                print("Ip is not same")
                reboot()
                continue
            else:
                print("Ip is same")
                break
        else :
            print("no connection")
            continue