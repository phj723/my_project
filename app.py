from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

twitter_consumer_key = "VbEurffmreTbhLXPby53czsqp"
twitter_consumer_secret = "sy693qyr17CyTKzVoYtTMkxurj2gp98OyqzUvJqe4XkBjKB3kB"
twitter_access_token = "1293456768001949701-rMKG1gBCNCe77qOVfH6fhSJIVrvBMX"
twitter_access_secret = "A4UbW1D3DxwfAXND0xAf7X4WNuu9Soh0f5oLDRp7RmewJ"

import twitter
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret,
                          access_token_key=twitter_access_token,
                          access_token_secret=twitter_access_secret)

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/twitter', methods=['GET'])
def twitter():
    query = "#샤이니"
    twitters = twitter_api.GetSearch(term=query, count=50)
    return jsonify({'result': 'success', 'twitters': twitters})

@app.route('/navernews', methods=['GET'])
def navernews():
    search_keyword = '샤이니'
    url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={search_keyword}'

    soup = BeautifulSoup(request.get(url).text, 'html.parser')
    titles = soup.select('.news .type01 li dt a[title]')
    images = soup.select('.news .type01 li>div a img[src]')

    return jsonify({'result': 'success', 'navernewstitle': titles, 'navernewsimage':images})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)