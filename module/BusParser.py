import requests
import bs4
import json
import os

class BusParser:
    def __init__ (self, strAppDataPath='./AppData/', strServiceKey = ''):
        if strServiceKey == '':
            return self._resultType('err', 'no serviceKey')
        
        self.strAppDataPath = strAppDataPath
        self.objCityCode = self.getCityCodeFile()

        pass

    def _resultType(strRes, objValue):
        return {
            'res' : strRes,
            'value' : objValue,
            'type' : str(type(objValue))
        }
    def getCityCodeFile(self):
        # check file location    
        if not os.path.isfile(self.strAppDataPath +'cityCode.json'):
            self.updateCityCode()
        
        f = open(self.strAppDataPath +'cityCode.json', 'r')
        try:
            objCityData = json.loads(f.read())
        except Exception as e:
            return self._resultType('err', 'JSON PARSE ERR -> {0}'.format(e))
        
        return self._resultType('ok', objCityData)

    def updateCityCode(self):
        return self._resultType('err', 'wip')