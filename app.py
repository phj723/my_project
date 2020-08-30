from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
import twitter
import jsonpickle
import requests

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.post('https://now.smtown.com/news/more',headers=headers,data={'pageSize': 50})
soup = BeautifulSoup(data.text, 'html.parser')

# import json
# class Object:
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__,
#             sort_keys=True, indent=4)
# def dumper(obj):
#     try:
#         return obj.toJSON()
#     except:
#         return obj.__dict__
twitter_consumer_key = "VbEurffmreTbhLXPby53czsqp"
twitter_consumer_secret = "sy693qyr17CyTKzVoYtTMkxurj2gp98OyqzUvJqe4XkBjKB3kB"
twitter_access_token = "1293456768001949701-BV8JFWtownCcl0KnCB1qQ2a3JHjKeF"
twitter_access_secret = "AbdDAtOIl1LeXIgkDk2gAKx6oXWjrxjqdYZSNIHJYp24W"
twitter_api = twitter.Api(consumer_key=twitter_consumer_key,
                          consumer_secret=twitter_consumer_secret,
                          access_token_key=twitter_access_token,
                          access_token_secret=twitter_access_secret)

#네이버
client_id = "h6vb0WM2BoawV1YltfbB" #1.에서 취득한 아이디 넣기
client_secret = "JPnVm0Q_D8"  #1. 에서 취득한 키 넣기

app = Flask(__name__)

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/onew')
def onew():
    return render_template('onew.html')

@app.route('/jonghyun')
def jonghyun():
    return render_template('jonghyun.html')

@app.route('/key')
def key():
    return render_template('key.html')

@app.route('/minho')
def minho():
    return render_template('minho.html')

@app.route('/taemin')
def taemin():
    return render_template('taemin.html')

@app.route('/bookmark')
def bookmark():
    return render_template('bookmark.html')

########## Home page
@app.route('/smtown', methods=['GET'])
def smtown():
    smtowns = soup.select('li.grid-item')
    for smtown in smtowns:
        headline = smtown.select_one('div > div.contentInfo > p.title.text_box > a').text.strip()
        content = smtown.select_one('div > div.contentInfo > p.subInfo.text_box > a').text.strip()
        time = smtown.select_one('div > div.contentInfo > ul > li').text
        img = smtown.select_one('div > div.thumb > a > img')
        if img is None:
            img = smtown.select_one('div > div.thumb > a')['style'].split("'")[1]
        else:
            img = img['src']
        url = smtown.select_one('div > div.contentInfo > p.title.text_box > a')['href']
        if 'youtube' not in url:
            url = 'https://now.smtown.com' + url
    return jsonify({'result': 'success', 'headlines': headline, 'contents': content, 'times': time, 'imgs': img, 'urls': url})

@app.route('/twitter', methods=['GET'])
def twitter():
    query = "샤이니"
    twitters = twitter_api.GetSearch(term=query, count=30, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews', methods=['GET'])
def navernews():
    search_word = '샤이니' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 20 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})

########## onew page
@app.route('/twitter_onew', methods=['GET'])
def twitter_onew():
    query = "온유"
    twitters = twitter_api.GetSearch(term=query, count=30, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_onew', methods=['GET'])
def navernews_onew():
    search_word = '온유' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 20 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})

########## jonghyun page
@app.route('/twitter_jonghyun', methods=['GET'])
def twitter_jonghyun():
    query = "샤이니 종현"
    twitters = twitter_api.GetSearch(term=query, count=30, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_jonghyun', methods=['GET'])
def navernews_jonghyun():
    search_word = '샤이니 종현' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 20 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})


########## key page
@app.route('/twitter_key', methods=['GET'])
def twitter_key():
    query = "샤이니 키"
    twitters = twitter_api.GetSearch(term=query, count=30, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_key', methods=['GET'])
def navernews_key():
    search_word = '샤이니 키' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 20 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})


########## minho page
@app.route('/twitter_minho', methods=['GET'])
def twitter_minho():
    query = "샤이니 민호"
    twitters = twitter_api.GetSearch(term=query, count=30, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_minho', methods=['GET'])
def navernews_minho():
    search_word = '샤이니 민호' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 20 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})


########## taemin page
@app.route('/twitter_taemin', methods=['GET'])
def twitter_taemin():
    query = "태민"
    twitters = twitter_api.GetSearch(term=query, count=30, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_taemin', methods=['GET'])
def navernews_taemin():
    search_word = '태민' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 20 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})


########## bookmark page




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)