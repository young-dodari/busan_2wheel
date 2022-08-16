import urllib.request
import json
import pandas as pd
import datetime

serviceKey = 'vTfdXtGsny7xRerwunqDq1PezLyeNmoFmRIx2YwnlYV4sA8EZfBl%2BKsVcjjugqAkuFX1KCdo4lag3L91sHFX%2BQ%3D%3D'

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
def getInterSectionInfo():
    service_url = 'http://apis.data.go.kr/6260000/CrossCartypeTrafficeVolumeService/getCrossCartypeTrafficeVolumeList'
    params = f'?serviceKey={serviceKey}&numOfRows=200&resultType=json&CLCT_DT=201809051205' # 인증키

    params += f'&pageNo=1'

    url = service_url + params
    
    retData = getRequestUrl(url)        #code 1

    if retData == None:
        return None
    else:
        return json.loads(retData)


# code 3
def getInterSectionService(item, result):
    result = []

    jsonData = getInterSectionInfo()
    
    if jsonData['getCrossCartypeTrafficVolumeList']['header']['code'] == '00':
        if jsonData['getCrossCartypeTrafficVolumeList']['item'] == '':
            print('서비스 오류!!')
        else:
            
            for item in jsonData['getCrossCartypeTrafficVolumeList']['item']:
                ISTL_LCTN = item['ISTL_LCTN']
                CLCT_DT = item['CLCT_DT']
                IXR_NM = item['IXR_NM']
                SUM_LRGTFVL = item['SUM_LRGTFVL']
                SUM_MDDLTFVL = item['SUM_MDDLTFVL']
                SUM_SMALTFVL = item['SUM_SMALTFVL']
                X_CRDN = item['X_CRDN']
                Y_CRDN = item['Y_CRDN']
                
                result.append({'방면':ISTL_LCTN,'수집일시':CLCT_DT,'교차로명':IXR_NM,'대형':SUM_LRGTFVL,'중형':SUM_MDDLTFVL,'소형':SUM_SMALTFVL,'경도':X_CRDN,'위도':Y_CRDN})

    return result




def main():
    result=[]
    # jsonResult=[]
    jsonRes = getInterSectionInfo()         #code 2


    print(jsonRes)
    for item in jsonRes['getCrossCartypeTrafficVolumeList']['item']:
        getInterSectionService(item, result)     #code 3

    

    with open(f'./교차로통행량정보테스트.json', mode='w', encoding='utf-8') as outfile:
        jsonFile = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)
    


# def main():
#     result=[]
#     # jsonResult=[]
#     jsonRes = getInterSectionInfo()         #code 2


#     # print(jsonRes)
#     for item in jsonRes['getCrossCartypeTrafficVolumeList']['item']:
#         getInterSectionService(item, result)     #code 3

#     # print(result)
#     df = pd.DataFrame(result)
#     df.to_csv('cross.csv', encoding='utf-8', index=False)
#     print(df)




if __name__ == '__main__':
    main()
