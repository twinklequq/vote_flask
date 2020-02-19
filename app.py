from flask import Flask
from flask import render_template
from utils.vote import Mongo

app = Flask(__name__)
root_dir = "http://127.0.0.1:5000/"
mongo = Mongo('127.0.0.1', 27017, 'vote')


@app.route('/')
def index():
    vote_info = mongo.find('vote_stats')
    return render_template('vote.html', vote_info=vote_info)


@app.route('/today')
def today():
    ret = mongo.find_today('vote_stats')
    if ret.count > 0:
        dates, vote_number = mongo.generate_data(ret)
        name = mongo.generate_plot(dates, vote_number)
        image = root_dir + "static/image/" + name
        return render_template('pic.html', image=image)
    else:
        return render_template('error.html')


@app.route('/yesterday')
def yesterday():
    ret = mongo.find_yesterday('vote_stats')
    if ret.count() > 0:
        dates, vote_number = mongo.generate_data(ret)
        name = mongo.generate_plot(dates, vote_number)
        image = root_dir + "static/image/" + name
        return render_template('pic.html', image=image)
    else:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)