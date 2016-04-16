import time
import requests
import requests_cache

from flask import Flask, render_template, request, jsonify
from yelpapi import YelpAPI as yelpApi
app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        #user input
        city = request.form.get('city')
        #get yelp info
        cityInfo = get_yelp(city)

        print(cityInfo)
        return jsonify(cityInfo)
    return render_template("index.html")





def get_yelp(name):
    tokens = get_tokens()
    #setup api access
    yelp_api = yelpApi(tokens[0], tokens[1],tokens[2],tokens[3])

    places = yelp_api.search_query(category_filter='restaurants', location = name, limit = 2, sort = 2)
    #places['businesses'][0]['name'] gets the first business name
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
            if line[0] != '#': # Not a comment line
                tokens.append(line.rstrip('\n'))
        return tokens

if __name__ == '__main__':
    app.run(debug=True)
