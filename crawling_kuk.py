import urllib.request
import json
import pandas as pd
import datetime

serviceKey = 'dfZE3xbEeRwk%2FuM8jwETwtbeq9PBoyGUt7PTx9Kp3h92vgyvrA6N7%2FOjdlpaki5ssQak9Zquvbgwl%2BKyUtkJ4A%3D%3D'

# code 1
def getRequestUrl(url):
    '''
    URL 접속 요청 후 응답함수
    ---------------------------------
    parameter : url -> OPENAPI 전체 URL
    '''
    req = urllib.request.Request(url)

    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200:
            print(f"[{datetime.datetime.now()} ] Url Request Success")
            return res.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f"[{datetime.datetime.now()}] Error for URL : {url}")
        return None

# code 2
def getInterSectionInfo(cnt):
    service_url = 'http://apis.data.go.kr/6260000/CrossCartypeTrafficeVolumeService/getCrossCartypeTrafficeVolumeList'
    params = f'?serviceKey={serviceKey}&numOfRows=150000&resultType=json&CLCT_DT=201809051205' # 인증키

    params += f'&pageNo={cnt}'

    url = service_url + params
    
    retData = getRequestUrl(url)        #code 1

    if retData == None:
        return None
    else:
        return json.loads(retData)

# def getInterSectionInfo():
#     service_url = 'http://apis.data.go.kr/6260000/CrossCartypeTrafficeVolumeService/getCrossCartypeTrafficeVolumeList'
#     params = f'?serviceKey={serviceKey}&numOfRows=200&resultType=json&CLCT_DT=201809051205' # 인증키

#     params += f'&pageNo=1'

#     url = service_url + params
    
#     retData = getRequestUrl(url)        #code 1

#     if retData == None:
#         return None
#     else:
#         return json.loads(retData)

def main():
    cnt = 0
    result = []
    jsonData = getInterSectionInfo(cnt) #code 2
    
    if jsonData['getCrossCartypeTrafficVolumeList']['header']['code'] == '00':
        if jsonData['getCrossCartypeTrafficVolumeList']['item'] == '':
            print('서비스 오류!!')
        else:
            
            while jsonData is None:
                cnt += 1
                jsonData = getInterSectionInfo(cnt)
                result.append(jsonData['getCrossCartypeTrafficVolumeList']['item'])

                for item in jsonData['getCrossCartypeTrafficVolumeList']['item']:
                    ISTL_LCTN = item['ISTL_LCTN']
                    CLCT_DT = item['CLCT_DT']
                    IXR_NM = item['IXR_NM']
                    SUM_LRGTFVL = item['SUM_LRGTFVL']
                    SUM_MDDLTFVL = item['SUM_MDDLTFVL']
                    SUM_SMALTFVL = item['SUM_SMALTFVL']
                    result.append([ISTL_LCTN, CLCT_DT, IXR_NM, SUM_LRGTFVL, SUM_MDDLTFVL, SUM_SMALTFVL])
                
            df = pd.DataFrame(result, columns=['ISTL_LCTN', 'CLCT_DT', 'IXR_NM', 'SUM_LRGTFVL', 'SUM_MDDLTFVL', 'SUM_SMALTFVL'])
            df.to_csv('intersection.csv', index=False, encoding='utf-8')
            print('intersection.csv 파일 생성 완료')







if __name__ == '__main__':
    main()
