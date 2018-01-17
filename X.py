# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 10:35:04 2018

@author: ziv_p
"""

import requests

# initalization parameters
GoogleKey = ENTER_YOUR_GOOGLE_KEY_HERE
MapQuestKey = 'ENTER_YOUR_MAPQUEST_KEY_HERE'

# GetAddress will use external web services to convert the "lat,lng" to address
# the function implements fail over (use a differnt service if the first fail)
def getAddress(latlng):
    
    # Get address from Google
    address = getAddressFromGoogle(latlng)
    
    # If failed then try to address from Map Quest
    if (address == ''):
        address = getAddressFromMapQuest(latlng)
    
    return address


# get Address using Google services
def getAddressFromGoogle(latlng)    :
    
    # Initialize 
    url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + latlng + '&key=' + GoogleKey
    
    # Call service and make sure we get a propr response
    try:
         r = requests.get(url)
         results = r.json()['results']
         returnString = results[0]['formatted_address']
    except ValueError:
       return ''
    
    # Return the address
    return returnString        


def getAddressFromMapQuest(latlng):
    
    # Initialize 
    url = 'http://www.mapquestapi.com/geocoding/v1/reverse?key=' + MapQuestKey + '&location=' + latlng    
    
    # Call service and make sure we get a propr response
    try:
        r = requests.get(url)
        results = r.json()['results'] 
        addressList = results[0]['locations']
    except ValueError:
       return ''    
    
    # Construct Address from response    
    returnString = addressList[0]['street'] + ', ' + addressList[0]['adminArea5'] 
    returnString += ', ' + addressList[0]['adminArea3'] + ' ' + addressList[0]['postalCode'] 
    returnString += ', ' + addressList[0]['adminArea1'] 
    
    # Return the address
    return returnString
    

# Create webserivce using Flask
from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

# setting up the web service
@app.route('/location/<lat>/<lng>')
def api_article(lat,lng):
    latlng = str(lat) + ',' + str(lng)
    address = str(getAddress(latlng))
    return 'Address is: ' + address

if __name__ == '__main__':
    app.run()
    
