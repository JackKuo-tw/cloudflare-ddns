#!/bin/env python3
'''This program will get record from Cloudflare and compare your current IP address'''

import json, requests
from os import popen, system

ZONE = 'YOUR_ZONE'
API_KEY = 'YOUR_KEY'
EMAIL = 'YOUR_EMAIL'
DN = 'YOUR_DOMAIN_NAME'
TYPE = 'YOUR_DNS_TYPE'
TTL = 120 # TTL you want to set
PROXIED = False

#The default http request header to send
MyHead = { 
    "X-Auth-Email" : EMAIL,
    "X-AUth-Key" : API_KEY,
    "Content-Type" : "application/json"
}


def GetRecordIP(): 
    """Get the IP address recorded in your Cloudflare """
    GetPayload = {  
        "type" : TYPE,
        "name" : DN
    }
    Cloudflare_current = requests.get( 
        "https://api.cloudflare.com/client/v4/zones/" + ZONE + "/dns_records",
        headers=MyHead,
        params=GetPayload
    ).text
    OldIP = json.loads(Cloudflare_current)['result'][0]['content']
    Identifier = json.loads(Cloudflare_current)['result'][0]['id']
    print('oldIP: ' + OldIP)
    return OldIP, Identifier

def GetCurrentIP():
    """Get the current IP address of your computer
    You can change the way getting your IP address"""
    CurrentIP = requests.get("http://icanhazip.com/").text[:-1]
    print('currentIP: ' + CurrentIP)
    return CurrentIP

def CompareAndUpdate(OldIP, Identifier, CurrentIP):
    """If your current IP address isn't match the record in Cloudflare, then update it!"""
    if CurrentIP != OldIP:
        PutPayload = { 
            "type" : TYPE,
            "name" : DN,
            "content" : CurrentIP,
            "ttl" : TTL,
            "proxied" : PROXIED
        }
        PutPayload = json.dumps(PutPayload, ensure_ascii=False)
        response = requests.put("https://api.cloudflare.com/client/v4/zones/"+ ZONE +"/dns_records/" + Identifier,
                headers = MyHead,
                data = PutPayload
        )
        response = json.loads(response.text)
        if response['success'] == True:
            print("Update successfully")
        else:
            print("Update failed")
            print(response["errors"])
            print(response["messages"])
    else:
        print("No need to update")

def main():
    OldIP, Identifier = GetRecordIP()
    CurrentIP = GetCurrentIP()
    CompareAndUpdate(OldIP, Identifier, CurrentIP)


if __name__ == "__main__":
    main()

