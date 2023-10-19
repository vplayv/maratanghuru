"""기본 라이브러리"""
import json
import os
import requests
from bs4 import BeautifulSoup
from konlpy.tag import Kkma
from konlpy.utils import pprint
from konlpy.tag import Okt
from pprint import pprint

'''크롤링 부분 상수'''
DATE = 0
TITLE = 1
VIEWS = 2
POS = 3
NEG = 4


def get_comments(stock, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    url = f"https://finance.naver.com/item/board.naver?code={stock}&page="
    # 삼성전자 예시) https://finance.naver.com/item/board.naver?code=005930&page=1

    comments = list()

    for page in range(1, page + 1):
        data = requests.get(url + str(page), headers=headers)
        soup = BeautifulSoup(data.content.decode("euc-kr", "replace"), "html.parser")
        lis = soup.find("table", {"class": "type2"}).select(
            "tbody > tr"
        )  # 종토방 종목 게시글 테이블 리스트

        for i in range(2, len(lis)):  # 첫번째는 의미 없는 데이터라서 제외
            review = list()
            if len(lis[i].select("td > span")) > 0:  # 댓글 5개 마다 있는 구분선 제외
                date = lis[i].select("td > span")[0].text  # 날짜
                title = lis[i].select("td.title > a")[0]["title"]  # 제목
                views = lis[i].select("td > span")[1].text  # 조회
                pos = lis[i].select("td > strong")[0].text  # 공감
                neg = lis[i].select("td > strong")[1].text  # 비공감

                # print(date, title, views, pos, neg)
                comment = [date, title, views, pos, neg]
                # print(review)
                comments.append([date, title, views, pos, neg])

    return comments

def my_tokenize(doc):
    # norm은 정규화, stem은 근어로 표시하기를 나타냄
    okt = Okt()
    return ['/'.join(t) for t in okt.pos(doc, norm=True, stem=True)] 
