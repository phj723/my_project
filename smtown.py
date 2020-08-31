import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.post('https://now.smtown.com/news/more', headers=headers, data={'pageSize': 50})
# print(data)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)

#############################
# (입맛에 맞게 코딩)
#############################

# select를 이용해서, tr들을 불러오기
smtowns = soup.select('li.grid-item')
print(smtowns.__len__())

# movies (tr들) 의 반복문을 돌리기
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

    print(headline)
    print(content)
    print(time)
    print(img)
    print(url)
