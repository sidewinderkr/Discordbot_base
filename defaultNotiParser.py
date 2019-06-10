# defaultNotiParser.py
# 특정 사이트의 특정 부분을 확인하여, 기존 확인값에서 바뀐 내용이 있다면 발췌
# 기본 실행: 새 업데이트가 있는지만 체크
# get_latest() 를 호출: 새로 바뀐 내용을 리턴

import requests
from bs4 import BeautifulSoup
import os

requesturl = 'http://granbluefantasy.jp/news/index.php'
checkfile = latest.txt

def get_latest():
    # 확인용 웹사이트의 공지 최근 타이틀을 확인, 옛날 자료와 비교,
    # 만약 변경사항이 있으면 변경된 타이틀과 링크를 리턴(string) 'title1,http://~'
    # 변경사항이 없으면 0을 리턴

    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 현재파일의 base path

    req = requests.get(requesturl)
    req.encoding = 'utf-8'

    html = req.text
    soup = BeautifulSoup(html, 'html.parser') #Beautiful soup로 html 양식으로 변환
    
    # 사이트 별로 달라져야 하는 부분! ##############
    # 찾는 방법: 노가다
    link_phrase = soup.find("a", {"class" : "change_news_trigger"})
    post = link_phrase.contents[0]
    link = link_phrase.get('href')
    #########################################

    latest = post + "," + link

    with open(os.path.join(BASE_DIR, checkfile), 'r+') as f_read:
        before = f_read.readline()
        if before != latest:
           print("new post: ", latest)
        f_read.close()

    with open(os.path.join(BASE_DIR, checkfile), 'w+') as f_write:
        f_write.write(latest)
        f_write.close()

    if before != latest:
        return latest
    else:
        return 0

if __name__ == "__main__":
    get_latest()

