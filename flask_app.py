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


def get_yelp(name, cityName):
    tokens = get_tokens()
    # setup api access
    yelp_api = yelpApi(tokens[0], tokens[1], tokens[2], tokens[3])

    places = yelp_api.search_query(term=name, location=cityName, limit=1)
    # print(places)
    # places['businesses'][0]['name'] gets the first business name
    results = {
        'name': places['businesses'][0]['name'],
        'url': places['businesses'][0]['url'],
        'image': places['businesses'][0]['image_url'],
        'rating': places['businesses'][0]['rating'],

    }
    # if no phone number set to false
    try:
        places['businesses'][0]['display_phone']
    except KeyError:
        results['phone'] = "false"
    else:
        results['phone'] = places['businesses'][0]['display_phone']
    return results


# this is used if tripadvisor returns no results
def get_yelp_back(city):
    tokens = get_tokens()  # setup api access
    yelp_api = yelpApi(tokens[0], tokens[1], tokens[2], tokens[3])

    places = yelp_api.search_query(category_filter='restaurants', location=city, limit=2, sort=2)
    # places['businesses'][0]['name'] gets the first business name
    results = {
        'name': places['businesses'][0]['name'],
        'url': places['businesses'][0]['url'],
        'image': places['businesses'][0]['rating_img_url_large']
    }
    return results


def get_tokens():
    tokens = []
    # Order: Consumer Key, Consumer Secret, Token, Token Secret
    with open("static/yelp.cred", 'r') as fin:
        for line in fin:
            if line[0] != '#':  # Not a comment line
                tokens.append(line.rstrip('\n'))
        return tokens


def get_trip(cityName):
    # https://www.tripadvisor.com/St.%20Louis,%20MO,%20United%20States
    cityName = cityName.replace(" ", "%20")
    restaurantList = []
    base = 'https://www.tripadvisor.com/'

    # get the webpage
    cityR = urllib.request.urlopen(base + cityName).read()

    # soupify webpage
    citySoup = BeautifulSoup(cityR)
    # navigate to tourist page
    info = citySoup.find_all("a", class_="subLink")

    cityLink = info[0].get('href')

    # get the tourist page
    cityR = urllib.request.urlopen(base + cityLink).read()
    citySoup = BeautifulSoup(cityR)
    # get the restaurants
    restaurants = citySoup.find_all("div", class_="col restaurants")
    restaurants = restaurants[0].find_all("div", class_="name")
    # check again to make sure restaurants is not empty
    if (not restaurants):
        return

        # get the top 3 restaurants names
    for i in range(0, 3):
        restaurantList.append(restaurants[i].get_text().replace('\n', ''))

    return restaurantList


def get_best(city):
    # print(city)
    tripList = get_trip(city)
    # print(tripList)
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

        if (place['rating'] > tempMax):
            bestRest = place
            tempMax = place['rating']

    return bestRest


if __name__ == '__main__':
    app.run(debug=True)
