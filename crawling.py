import urllib.request
import json
import pandas as pd
import datetime

serviceKey = 'vTfdXtGsny7xRerwunqDq1PezLyeNmoFmRIx2YwnlYV4sA8EZfBl%2BKsVcjjugqAkuFX1KCdo4lag3L91sHFX%2BQ%3D%3D'

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


def getInterSectionInfo():
    service_url = 'http://apis.data.go.kr/6260000/CrossCartypeTrafficeVolumeService/getCrossCartypeTrafficeVolumeList'
    params = f'?serviceKey={serviceKey}' # 인증키
    params += f'&numOfRows=10'
    params += f'&pageNo=1'
    params += f'&resultType=json'
    params += f'&CLCT_DT=201809051205'
    url = service_url + params
    
    retData = getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)


def getInterSectionService():
    result = []

    jsonData = getInterSectionInfo()
    
    if jsonData['getCrossCartypeTrafficVolumeList']['header']['code'] == '00':
        if jsonData['getCrossCartypeTrafficVolumeList']['item'] == '':
            print('서비스 오류!!')
        else:
            
            for item in jsonData['getCrossCartypeTrafficVolumeList']['item']:
                ISTL_LCTN = item['ISTL_LCTN']
                CLCT_DT = item['CLCT_DT']
                SUM_LRGTFVL = item['SUM_LRGTFVL']
                Y_CRDN = item['Y_CRDN']
                IXR_ID = item['IXR_ID']
                IXR_NM = item['IXR_NM']
                SUM_MDDLTFVL = item['SUM_MDDLTFVL']
                SUM_SMALTFVL = item['SUM_SMALTFVL']
                X_CRDN = item['X_CRDN']
                CMRA_ID = item['CMRA_ID']
                
                result.append([ISTL_LCTN,CLCT_DT,SUM_LRGTFVL,Y_CRDN,IXR_ID,IXR_NM,SUM_MDDLTFVL,SUM_SMALTFVL,X_CRDN,CMRA_ID])

    return result




def main():

    jsondata = getInterSectionService()

    print(jsondata)




if __name__ == '__main__':
    main()
