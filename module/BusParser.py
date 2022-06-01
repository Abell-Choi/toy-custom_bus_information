import requests
import bs4
import json
import os

class BusParser:
    def __init__ (self, strAppDataPath='./AppData/', strServiceKey = ''):
        if strServiceKey == '':
            return self._resultType('err', 'no serviceKey')
        self.strServiceKey = strServiceKey
        self.strAppDataPath = strAppDataPath
        self.objCityCode = self.getCityCodeFile()

        pass

    def _resultType(self, strRes, objValue):
        return {
            'res' : strRes,
            'value' : objValue,
            'type' : str(type(objValue))
        }

    def _getAPIData(self, strUrl, objParams ={}):
        if objParams == {}:
            objParams = {'serviceKey' : self.strServiceKey, '_type' : 'json'}
        
        if not 'serviceKey' in objParams:
            objParams['serviceKey'] = self.strServiceKey
        
        if not '_type' in objParams:
            objParams['_type'] = 'json'

        f = requests.get(strUrl, objParams)
        try:
            strApiData = f.content
        except Exception as e:
            return self._resultType('Text decode err -> {0}\n{1}'.format(e, strApiData))
        try:
            objReqData = json.loads(strApiData)
        except Exception as e:
            return self._resultType('err', 'JSON PARSE ERR -> {0}\n{1}'.format(e, strApiData))
        
        if objReqData['response']['body']['items'] == '':
            return self._resultType('err', 'no Data in Items')
        return self._resultType('ok', objReqData['response']['body']['items'])

    def getCityCodeFile(self):
        # check file location    
        if not os.path.isfile(self.strAppDataPath +'cityCode.json'):
            self.updateCityCode()
        
        f = open(self.strAppDataPath +'cityCode.json', 'r')
        try:
            objCityData = json.loads(f.read())
        except Exception as e:
            self.updateCityCode()
            return self._resultType('err', 'JSON PARSE ERR -> {0}\n{1}'.format(e, f.read()))
        
        return self._resultType('ok', objCityData)

    def updateCityCode(self):
        objApiReq = self._getAPIData(strUrl='http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getCtyCodeList', objParams={
            'serviceKey' : self.strServiceKey, '_type' : 'json'
        })

        if objApiReq['res'] == 'err' : return objApiReq

        f = open(self.strAppDataPath +'cityCode.json', 'w')
        f.write(json.dumps(objApiReq['value']['item'], indent=2, ensure_ascii= False))
        return self._resultType('ok', 'citycode updated')

obj = BusParser(strServiceKey='CUVA5IJchn3HKUbkeZvoDyJOnPeb1McJdicq6Ho830JRN9SpE8BpjadSGBQ/Dr6LhXgBiJLRVG2calIzDYLRqA==')