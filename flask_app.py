from flask import Flask, render_template, request, jsonify
from yelpapi import YelpAPI as yelpApi

app = Flask(__name__)
import urllib.request

import requests
from bs4 import BeautifulSoup


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # user input
        city = request.form.get('city')

        # get yelp info
        bestRest = get_best(city)
        # cityInfo = get_yelp(city)

        # print(bestRest)
        return jsonify(bestRest)
    return render_template("index.html")



#get the best restaurant for the city
def get_best(city):

    tripList = get_trip(city)
    #print(not tripList)
    yelpInfo = []
    bestRest = ''
    tempMax = 0.0
    if (not tripList):
        return get_yelp_back(city)
    # get yelp info about restaurants
    for place in tripList:
        yelpInfo.append(get_yelp(place, city))

    # compare the restaurants
    for place in yelpInfo:

        if ((place['rating'] > tempMax and place['numReviews'] > 10) or
                ((place['rating']+1)>tempMax and place['numReviews'] > bestRest['numReviews'])):
            bestRest = place
            tempMax = place['rating']

    return bestRest


#tripadvisor scraper
def get_trip(cityName):
    # https://www.tripadvisor.com/St.%20Louis,%20MO,%20United%20States
    cityName = cityName.replace(" ", "%20")
    restaurantList = []
    base = 'https://www.tripadvisor.com/'

    # get the webpage
    try:
        cityR = urllib.request.urlopen(base + cityName).read()
    #if fails return an empty list
    except urllib.error.HTTPError:
        return []


    # soupify webpage
    citySoup = BeautifulSoup(cityR)
    # navigate to tourist page
    info = citySoup.find_all("a", class_="subLink")

    cityLink = info[0].get('href')

    # get the tourist page
    try:
        cityR = urllib.request.urlopen(base + cityLink).read()
    except urllib.error.HTTPError:
        return []

    citySoup = BeautifulSoup(cityR)
    # get the restaurants
    restaurants = citySoup.find_all("div", class_="col restaurants")
    restaurants = restaurants[0].find_all("div", class_="name")
    # check again to make sure restaurants is not empty
    #print(not restaurants)
    if (not restaurants):
        return []

        # get the top 3 restaurants names
    for i in range(0, 3):
        restaurantList.append(restaurants[i].get_text().replace('\n', ''))

    return restaurantList

#get the yelp info for each restaurant
def get_yelp(name, cityName):
    tokens = get_tokens()
    # setup api access
    yelp_api = yelpApi(tokens[0], tokens[1], tokens[2], tokens[3])
    places = yelp_api.search_query(term=name, location=cityName, limit=1)

    results = {
        'name': places['businesses'][0]['name'],
        'url': places['businesses'][0]['url'],
        'image': places['businesses'][0]['image_url'],
        'rating': places['businesses'][0]['rating'],
        'numReviews': places['businesses'][0]['review_count']
    }
    # if no phone number set to false
    try:
        places['businesses'][0]['display_phone']
    except KeyError:
        results['phone'] = "false"
    else:
        results['phone'] = places['businesses'][0]['display_phone']
    return results


# this is used if get_trip() returns no results
def get_yelp_back(city):
    tokens = get_tokens()  # setup api access
    yelp_api = yelpApi(tokens[0], tokens[1], tokens[2], tokens[3])

    places = yelp_api.search_query(category_filter='restaurants', location=city, limit=2, sort=2)

    results = {
        'name': places['businesses'][0]['name'],
        'url': places['businesses'][0]['url'],
        'image': places['businesses'][0]['image_url']
    }
    try:
        places['businesses'][0]['display_phone']
    except KeyError:
        results['phone'] = "false"
    else:
        results['phone'] = places['businesses'][0]['display_phone']
    return results

#used for yelp api
def get_tokens():
    tokens = []
    # Order: Consumer Key, Consumer Secret, Token, Token Secret
    with open("static/yelp.cred", 'r') as fin:
        for line in fin:
            if line[0] != '#':  # Not a comment line
                tokens.append(line.rstrip('\n'))
        return tokens






if __name__ == '__main__':
    app.run(debug=True)
