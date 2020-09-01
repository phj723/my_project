from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
import twitter
import jsonpickle
import requests
import json

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.post('https://now.smtown.com/news/more',headers=headers,data={'pageSize': 50})
# soup = BeautifulSoup(data.text, 'html.parser')

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

######### Home page
@app.route('/youtube', methods=['GET'])
def youtube():
    youtube_data = requests.get('https://www.youtube.com/playlist?list=UUyPwRgc3gQGqhk6RoGS50Ug', headers=headers)
    soup = BeautifulSoup(youtube_data.text, 'html.parser') #BeautifulSoup로 Response 값을 분석합니다.
    scripts = soup.find_all('script') # <script> 태그가 있는 부분만 찾아내어 Set으로 반환합니다.

    found_i = -1
    for (i, x) in enumerate(scripts):
        if 'window["ytInitialData"] = ' in str(x):  # ytInitialData가 담긴 객체를 검색합니다.
            found_i = i
            break
    if found_i < 0:
        print('Cannot find playlist')  # 만일 ytInitialData가 담긴 객체를 찾지 못했다면 그냥 종료합니다.
        exit()

    data = scripts[found_i]
    str1 = data.string.strip().split('window["ytInitialData"] = ')[1].split(';\n')[0]
    video = json.loads(str1, encoding='utf8', strict=False)  # String을 JSON Parsing하여 파이썬에서 사용할 수 있도록 해줍니다.
        # 이 때 strict를 false로 하지 않으면 인코딩 문제로 loads()가 제대로 실행되지 않을 수 있습니다.
    video_ids = \
    video['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer'][
        'contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']
    youtubes = []
    for video_id in video_ids:
        url = 'https://www.youtube.com/watch?v=' + video_id['playlistVideoRenderer']['videoId']
        img = video_id['playlistVideoRenderer']['thumbnail']['thumbnails'][0]['url']
        origin_img = img.split('?')[0]
        title = video_id['playlistVideoRenderer']['title']['simpleText']
        youtube = {'url': url, 'origin_img': origin_img, 'title': title}
        youtubes.append(youtube)
    return jsonify({'result': 'success', 'youtubes': youtubes})


@app.route('/smtown', methods=['GET'])
def smtown():
    smtown_data = requests.post('https://now.smtown.com/news/more', headers=headers, data={'pageSize': 20})
    soup = BeautifulSoup(smtown_data.text, 'html.parser')
    smtowns = soup.select('li.grid-item')
    smnews = []
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
        sm = {
            'headline': headline,
            'content': content,
            'time': time,
            'img': img,
            'url': url}
        smnews.append(sm)
    return jsonify({'result': 'success', 'smnews': smnews})

@app.route('/twitter', methods=['GET'])
def twitter():
    query = "샤이니"
    twitters = twitter_api.GetSearch(term=query, count=50, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews', methods=['GET'])
def navernews():
    search_word = '샤이니' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 40 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})

########## onew page
@app.route('/smtown_onew', methods=['GET'])
def smtown_onew():
    smtown_data = requests.post('https://now.smtown.com/news/more', headers=headers, data={'pageSize': 20})
    soup = BeautifulSoup(smtown_data.text, 'html.parser')
    smtowns = soup.select('li.grid-item')
    smnews = []
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
        sm = {
            'headline': headline,
            'content': content,
            'time': time,
            'img': img,
            'url': url}
        smnews.append(sm)
    return jsonify({'result': 'success', 'smnews': smnews})

@app.route('/twitter_onew', methods=['GET'])
def twitter_onew():
    query = "온유"
    twitters = twitter_api.GetSearch(term=query, count=50, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_onew', methods=['GET'])
def navernews_onew():
    search_word = '온유' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 40 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})

########## jonghyun page
@app.route('/smtown_jonghyun', methods=['GET'])
def smtown_jonghyun():
    smtown_data = requests.post('https://now.smtown.com/news/more', headers=headers, data={'pageSize': 20})
    soup = BeautifulSoup(smtown_data.text, 'html.parser')
    smtowns = soup.select('li.grid-item')
    smnews = []
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
        sm = {
            'headline': headline,
            'content': content,
            'time': time,
            'img': img,
            'url': url}
        smnews.append(sm)
    return jsonify({'result': 'success', 'smnews': smnews})

@app.route('/twitter_jonghyun', methods=['GET'])
def twitter_jonghyun():
    query = "샤이니 종현"
    twitters = twitter_api.GetSearch(term=query, count=50, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_jonghyun', methods=['GET'])
def navernews_jonghyun():
    search_word = '샤이니 종현' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 40 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})


########## key page
@app.route('/smtown_key', methods=['GET'])
def smtown_key():
    smtown_data = requests.post('https://now.smtown.com/news/more', headers=headers, data={'pageSize': 20})
    soup = BeautifulSoup(smtown_data.text, 'html.parser')
    smtowns = soup.select('li.grid-item')
    smnews = []
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
        sm = {
            'headline': headline,
            'content': content,
            'time': time,
            'img': img,
            'url': url}
        smnews.append(sm)
    return jsonify({'result': 'success', 'smnews': smnews})

@app.route('/twitter_key', methods=['GET'])
def twitter_key():
    query = "샤이니 키"
    twitters = twitter_api.GetSearch(term=query, count=50, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_key', methods=['GET'])
def navernews_key():
    search_word = '샤이니 키' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 40 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})


########## minho page
@app.route('/smtown_minho', methods=['GET'])
def smtown_minho():
    smtown_data = requests.post('https://now.smtown.com/news/more', headers=headers, data={'pageSize': 20})
    soup = BeautifulSoup(smtown_data.text, 'html.parser')
    smtowns = soup.select('li.grid-item')
    smnews = []
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
        sm = {
            'headline': headline,
            'content': content,
            'time': time,
            'img': img,
            'url': url}
        smnews.append(sm)
    return jsonify({'result': 'success', 'smnews': smnews})

@app.route('/twitter_minho', methods=['GET'])
def twitter_minho():
    query = "샤이니 민호"
    twitters = twitter_api.GetSearch(term=query, count=50, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_minho', methods=['GET'])
def navernews_minho():
    search_word = '샤이니 민호' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 40 #출력 뉴스 수
    sort = 'sim' #결과값의 정렬기준 시간순 date, 관련도 순 sim
    start = 1 # 출력 위치
    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {'X-Naver-Client-Id': client_id,
           'X-Naver-Client-Secret': client_secret
           }
    navernews = requests.get(url, headers=headers).json()
    return jsonpickle.encode({'result': 'success', 'navernews': navernews})


########## taemin page
@app.route('/smtown_taemin', methods=['GET'])
def smtown_taemin():
    smtown_data = requests.post('https://now.smtown.com/news/more', headers=headers, data={'pageSize': 20})
    soup = BeautifulSoup(smtown_data.text, 'html.parser')
    smtowns = soup.select('li.grid-item')
    smnews = []
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
        sm = {
            'headline': headline,
            'content': content,
            'time': time,
            'img': img,
            'url': url}
        smnews.append(sm)
    return jsonify({'result': 'success', 'smnews': smnews})

@app.route('/twitter_taemin', methods=['GET'])
def twitter_taemin():
    query = "태민"
    twitters = twitter_api.GetSearch(term=query, count=50, lang='ko')
    # return json.dumps({'result': 'success', 'twitters': twitters}, default=dumper, indent=2)
    return jsonpickle.encode({'result': 'success', 'twitters': twitters})

@app.route('/navernews_taemin', methods=['GET'])
def navernews_taemin():
    search_word = '태민' #검색어
    encode_type = 'json' #출력 방식 json 또는 xml
    max_display = 40 #출력 뉴스 수
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