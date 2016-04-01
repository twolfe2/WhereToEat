from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from yelpapi import YelpAPI as yelpApi


app = Flask(__name__)
yelp = {}
tripAdvisor = {}




@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/welcome')
def welcome():
    return render_template('index.html')

@app.route('/cityInfo', methods=['POST'])
def get_city_name():
    name = request.form['text']

    yelp = get_yelp(name)
    return render_template('city.html', name = name, yelp = yelp)

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

def get_trip(name):
    return 'working'

def compare():
    return 'test'

def get_tokens():
    tokens = []
    # Order: Consumer Key, Consumer Secret, Token, Token Secret
    with open("static/yelp.cred", 'r') as fin:
        for line in fin:
            if line[0] != '#': # Not a comment line
                tokens.append(line.rstrip('\n'))
        return tokens

if __name__ == '__main__':
    app.run()
