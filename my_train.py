from get_comments import my_tokenize
from get_comments import get_comments
import nltk
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import matplotlib.font_manager as fm
import numpy as np

def my_train(train_stock, test_stock, page):
    ''' 
    train_stock : 훈련용 데이터 주식종목
    test_stock : 테스트 데이터 주식종목
    page : 네이버 크롤링 페이지수
    '''

    '''한글 폰트 깨져서 굴림 설정'''
    Gulim = fm.FontProperties(fname='c:/windows/fonts/gulim.ttc').get_name()
    
    train_data = get_comments(train_stock, page)
    train_docs = [(my_tokenize(row[1]), row[2]) for row in train_data]
    
    test_data = get_comments(test_stock, page)
    test_docs = [(my_tokenize(row[1]), row[2]) for row in test_data]

    tokens = [t for d in train_docs for t in d[0]]
    
    '''전처리기 설정'''
    text = nltk.Text(tokens, name='NMSC')
    
    #Font
    Gulim = fm.FontProperties(fname='c:/windows/fonts/gulim.ttc').get_name()
    
    # 폰트 설정
    plt.rc('font', family=Gulim)
    
    plt.figure(figsize=(20,10))
    text.plot(50)
    
    return train_docs, test_docs
    
# 훈련모델 : 454910 두산로보틱스
# 테스트모델 : 451220 아이엠티
my_train('454910', '451220', 10)