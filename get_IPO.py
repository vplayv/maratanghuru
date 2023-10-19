# pyright: reportUnusedImport=false
import requests
from bs4 import BeautifulSoup 
import pandas as pd 
from pandas.tseries.offsets import BDay

from datetime import datetime, timedelta

# 공모주 청약일정 크롤링하는 함수 정의 ( 38커뮤니케이션 )
def IPO():
    
    # 1. 공모주 청약 일정 크롤링 
    url = "http://www.38.co.kr/html/fund/index.htm?o=k" # 공모주 청약 일정 url 가져오기
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) 
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('table', {'summary': '공모주 청약일정'})

    company_list = []
    IPO_date_list = []
    price_list = []
    expected_price_list = []
    competition_list = []
    underwriter_list = []

    data = data.find_all('tr')[1:]

    for row in range(0, len(data)):
        data_list = data[row].text.replace('\xa0\xa0', '').split('\n')[1:-1]
        if len(data_list) < 6:
            continue
            
        if '한국투자증권' in data_list[5] : # 한국투자증권에서 진행하는 종목만 골라내기 
            company_list.append(data_list[0].strip())
            IPO_date_list.append(data_list[1].strip())
            price_list.append(data_list[2].strip())
            expected_price_list.append(data_list[3].strip())
            # competition_list.append(data_list[4].strip())
            underwriter_list.append(data_list[5].strip())

    result = pd.DataFrame({'종목명': company_list,
                        '공모주일정': IPO_date_list,
                        '확정공모가': price_list,
                        '희망공모가': expected_price_list,
                        # '청약경쟁률': competition_list,
                        '주간사': underwriter_list})
    
    result = result.sort_values(by='공모주일정',ignore_index=True)

    
    # 2. 수요예측 일정 추가 
    url = "http://www.38.co.kr/html/fund/index.htm?o=r" # 수요예측 일정 url 가져오기
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) 
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('table', {'summary': '수요예측일정'})
    
    company_list = []
    IPO_demand_list = [] 
    
    data = data.find_all('tr')[1:]

    for row in range(0, len(data)):
        data_list = data[row].text.replace('\xa0\xa0', '').split('\n')[1:-1]
        if len(data_list) < 6:
            continue
        
        if '한국투자증권' in data_list[5].strip(): # 한국투자증권에서 진행하는 일정만 골라내기 
            company_list.append(data_list[0].strip())
            IPO_demand_list.append(data_list[1].strip())

    IPO_demand_df = pd.DataFrame({'종목명': company_list, '수요예측일정': IPO_demand_list}).sort_values(by='수요예측일정',ignore_index=True)
    
    result = pd.merge(result,IPO_demand_df, how='outer',on='종목명')
    
    result = result[['종목명','수요예측일정','공모주일정','확정공모가','희망공모가','주간사']]
    
    return result


# 공모주 배정/환불 스케쥴 추가하기 
def IPO_refund(data): 

    # 배정일은 청약 시작일 + 2영업일 
    # 환불일은 청약 시작일 + 3영업일 
    
    s_date = data['공모주일정'].values.tolist() # 청약 시작일 
    assign_date = [] 
    refund_date = [] 
    
    # datetime 적용을 위해 데이터 전처리 
    for date in s_date:
        date = datetime.strptime(date.split('~')[0].replace('.','-'), '%Y-%m-%d')
        assign_date.append( str(date + BDay(2)).split(' ')[0] )
        refund_date.append( str(date + BDay(3)).split(' ')[0] )
        
    
    assign_df = pd.DataFrame(assign_date)
    refund_df = pd.DataFrame(refund_date)
    
    data.insert(3,"배정일정",assign_df)
    data.insert(4,"환불일정",refund_df)
    
    return data 


def IPO_date():
    hantu_IPO_data = IPO() 
    result = []
    for data in IPO_refund(hantu_IPO_data).values.tolist() :
        # 청약마감일 
        end = datetime.strptime(data[2].split('~')[0][:4]+'-'+data[2].split('~')[1].replace('.','-'), '%Y-%m-%d')
        
        if end.weekday() == 4 : end = str(end + timedelta(days=1)).split(' ')[0]  # 청약마감일이 금요일 일 때, 
        else: end = str(end+BDay(1)).split(' ')[0] # 청약마감일이 금요일이 아닐 때 
          
        result.append({'종목명':data[0], '수요예측일':str(data[1]).split('~')[0].replace('.','-'), '청약일':data[2].split('~')[0].replace('.','-'), '배정일':data[3].replace('-','.').replace('.','-'),'환불일':data[4].replace('-','.').replace('.','-'),'희망공모가':data[6],'주간사':data[7], '청약마감일': end})

    return result 

result = IPO_date()
print(result)