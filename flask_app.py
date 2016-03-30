from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap


app = Flask(__name__)




@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/welcome')
def welcome():
    return render_template('index.html')

@app.route('/cityInfo/', methods=['POST'])
def get_city_name():
    name = request.form['text']
    return render_template('city.html', name = name)




if __name__ == '__main__':
    app.run()
