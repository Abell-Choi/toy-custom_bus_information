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
        self.lstCityCode = self.getCityCodeFile()['value']

        pass

    def _resultType(self, strRes, objValue):
        return {
            'res' : strRes,
            'value' : objValue,
            'type' : str(type(objValue))
        }

    def _checkCityCode(self, nCityCode):
        for i in self.lstCityCode:
            if i['citycode'] == nCityCode:
                res = True
                return self._resultType('ok', i['cityname'])
                
        return self._resultType('err', 'no Match code')

    def _getAPIData(self, strUrl, objParams ={}):
        if objParams == {}:
            objParams = {'serviceKey' : self.strServiceKey, '_type' : 'json'}
        
        if not 'serviceKey' in objParams:
            print("can't find servicekey in params")
            objParams['serviceKey'] = self.strServiceKey
        
        if not '_type' in objParams:
            print("can't find _type in params")
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
            return self._resultType('err', 'no Data in Items -> {0}'.format(objReqData))
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

    def getRouteInfo(self, nCityCode:int=0, nBusNum:int=0) -> dict:
        if nCityCode == 0:
            return self._resultType('err', 'need city code')
        if self._checkCityCode(nCityCode)['res'] == 'err':
            return self._resultType('err', 'no match citycode')
        
        if nBusNum == 0:
            return self._resultType('err', 'need bus number')
        strUrl = 'http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteNoList'
        objParam = {
            '_type' : 'json',
            'cityCode' : str(nCityCode),
            'routeNo' : str(nBusNum),
            'numOfRows' : str(1000)
        }

        objRes = self._getAPIData(strUrl, objParam)
        if objRes['res'] == 'err' : return objRes

        return self._resultType('ok', objRes['value']['item'])
    
    def getBusStateInfo(self, nCityCode:int=0, strRouteId:str=''):
        if nCityCode == 0: return self._resultType('err', 'need nCityCode')
        if strRouteId == '': return self._resultType('err', 'need strRouteId')
        if self._checkCityCode(nCityCode)['res'] == 'err':
            return self._checkCityCode(nCityCode)
        
        strUrl = 'http://apis.data.go.kr/1613000/BusLcInfoInqireService/getRouteAcctoBusLcList'
        objParam = {
            '_type' : 'json',
            'numOfRows' : str(1000),
            'cityCode' : str(nCityCode),
            'routeId' : strRouteId
        }
        return self._getAPIData(strUrl, objParam)