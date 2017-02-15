import SocketServer
import json
import modelHolder
import pprint

HOST = '127.0.0.1'
PORT = 13373


#useful advice obtained from
#http://thomasfischer.biz/python-simple-json-tcp-server-and-client/



def main():
    
    print "Running server..."
    
    #start the server
    
    server = MyTCPServer((HOST, PORT), MyTCPServerHandler)
    server.serve_forever()


def convertData_knn2(forecast):
    """ return the data ready for the model """
    
    #features_dummy = ['Humidity','Temp','Rain ','DewPoint','UserFrizzSet_0.0','UserFrizzSet_1.0','UserFrizzSet_2.0']
    
    #performs 0-1 scaling as well
    #dewpoint max min 17.81211342 -1.090463856
    #temp max min 25 2
    tempVal = {"max":25,"min":2}
    dewPointVal = {"max":17.81211342,"min":-1.090463856}
    
    temp = (float(forecast['fcTemp']) - tempVal["min"]) / (tempVal["max"] - tempVal["min"])
    humidity = float(forecast['fcHumidity']) /100
    rain = float(forecast['fcRainPC']) /100
    dewPoint = (float(forecast['fcDewPoint']) - dewPointVal["min"]) / (dewPointVal["max"] - dewPointVal["min"])
    
   
    data = (humidity,temp,rain,dewPoint)

    return data


def processData(results):
    """ pass the forecast data through the predicition model """
    
    returnList= []
    
    
    for daySet in results:
        
        newResults = {}
        
        newResults['fcDate'] = daySet['fcDate']
        
        forecastList = []
        
        for forecast in daySet['forecasts']:
            
            newForecast = forecast

            #convert each forecast data entry to the correct format for the prediction model
            entry = convertData_knn2(forecast)
            
            entry_UFS_0 = entry + (1,0,0)
            entry_UFS_1 = entry + (0,1,0)
            entry_UFS_2 = entry + (0,0,1)
            
            predResult_UFS_0 = modelHolder.model.predict(entry_UFS_0)
            predResult_UFS_1 = modelHolder.model.predict(entry_UFS_1)
            predResult_UFS_2 = modelHolder.model.predict(entry_UFS_2)


            newForecast['pred0'] = predResult_UFS_0[0]
            newForecast['pred1'] = predResult_UFS_1[0]
            newForecast['pred2'] = predResult_UFS_2[0]

            
            forecastList.append(newForecast)

        newResults['forecasts']=forecastList
        newResults['modelName'] = modelHolder.modelName
        returnList.append(newResults)

    return returnList

class MyTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True

class MyTCPServerHandler(SocketServer.BaseRequestHandler):
    
    
    def handle(self):
        try:
            data = json.loads(self.request.recv(8192).strip())
            # process the data, i.e. print it:
            #print data
            
            resultData = processData(data)
            
            
            # send some 'ok' back
            self.request.sendall(json.dumps(resultData))
        
        
        except Exception, e:
            print "Exception while receiving message: ", e

def testSystem():
    """ tests the conversion and prediction parts of this script """

    data = json.loads(testMessage())
    #data = testMessage()
    tests = processData(data)

    pp = pprint.PrettyPrinter(4)
    pp.pprint(tests)


def testMessage():
    
    #needed to provide string before it is pythonised ie made unicode

    return """[{"fcDate":"2014-7-28Z","forecasts":[{"fcDateTime":"2014-07-28T14:00:00.000Z","fcDate":"2014-7-28Z","fcTime":"900","fcHumidity":"50","fcTemp":"21","fcRainPC":"8","fcTempFeel":"18","fcAbHumidity":9.15798944424662,"fcDewPoint":10.190160504755106,"fcWindSpeed":"13"},{"fcDateTime":"2014-07-28T17:00:00.000Z","fcDate":"2014-7-28Z","fcTime":"1080","fcHumidity":"60","fcTemp":"20","fcRainPC":"42","fcTempFeel":"18","fcAbHumidity":10.366909490577095,"fcDewPoint":12.006807823728433,"fcWindSpeed":"11"},{"fcDateTime":"2014-07-28T20:00:00.000Z","fcDate":"2014-7-28Z","fcTime":"1260","fcHumidity":"63","fcTemp":"19","fcRainPC":"51","fcTempFeel":"18","fcAbHumidity":10.263779357370478,"fcDewPoint":11.803426847437237,"fcWindSpeed":"9"},{"fcDateTime":"2014-07-28T22:59:00.000Z","fcDate":"2014-7-28Z","fcTime":"1439","fcHumidity":"73","fcTemp":"18","fcRainPC":"49","fcTempFeel":"16","fcAbHumidity":11.208739855270547,"fcDewPoint":13.09215184157174,"fcWindSpeed":"9"}]},{"fcDate":"2014-7-29Z","forecasts":[{"fcDateTime":"2014-07-29T05:00:00.000Z","fcDate":"2014-7-29Z","fcTime":"360","fcHumidity":"81","fcTemp":"17","fcRainPC":"4","fcTempFeel":"16","fcAbHumidity":11.71607777446004,"fcDewPoint":13.718426224255458,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-29T08:00:00.000Z","fcDate":"2014-7-29Z","fcTime":"540","fcHumidity":"63","fcTemp":"19","fcRainPC":"5","fcTempFeel":"18","fcAbHumidity":10.263779357370478,"fcDewPoint":11.803426847437237,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-29T11:00:00.000Z","fcDate":"2014-7-29Z","fcTime":"720","fcHumidity":"41","fcTemp":"23","fcRainPC":"1","fcTempFeel":"22","fcAbHumidity":8.427321164980812,"fcDewPoint":9.052921698930929,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-29T14:00:00.000Z","fcDate":"2014-7-29Z","fcTime":"900","fcHumidity":"37","fcTemp":"26","fcRainPC":"0","fcTempFeel":"25","fcAbHumidity":9.01119386792014,"fcDewPoint":10.200574417231195,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-29T17:00:00.000Z","fcDate":"2014-7-29Z","fcTime":"1080","fcHumidity":"32","fcTemp":"26","fcRainPC":"0","fcTempFeel":"25","fcAbHumidity":7.793464966849852,"fcDewPoint":8.047206498731521,"fcWindSpeed":"9"},{"fcDateTime":"2014-07-29T20:00:00.000Z","fcDate":"2014-7-29Z","fcTime":"1260","fcHumidity":"52","fcTemp":"23","fcRainPC":"3","fcTempFeel":"22","fcAbHumidity":10.688309770219567,"fcDewPoint":12.62604505797753,"fcWindSpeed":"9"},{"fcDateTime":"2014-07-29T22:59:00.000Z","fcDate":"2014-7-29Z","fcTime":"1439","fcHumidity":"64","fcTemp":"20","fcRainPC":"4","fcTempFeel":"19","fcAbHumidity":11.0580367899489,"fcDewPoint":12.989813651781178,"fcWindSpeed":"9"}]},{"fcDate":"2014-7-30Z","forecasts":[{"fcDateTime":"2014-07-30T05:00:00.000Z","fcDate":"2014-7-30Z","fcTime":"360","fcHumidity":"73","fcTemp":"16","fcRainPC":"0","fcTempFeel":"15","fcAbHumidity":9.942077170389707,"fcDewPoint":11.166243160472122,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-30T08:00:00.000Z","fcDate":"2014-7-30Z","fcTime":"540","fcHumidity":"64","fcTemp":"18","fcRainPC":"3","fcTempFeel":"17","fcAbHumidity":9.82684042105911,"fcDewPoint":11.09443185191891,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-30T11:00:00.000Z","fcDate":"2014-7-30Z","fcTime":"720","fcHumidity":"50","fcTemp":"21","fcRainPC":"4","fcTempFeel":"20","fcAbHumidity":9.15798944424662,"fcDewPoint":10.190160504755106,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-30T14:00:00.000Z","fcDate":"2014-7-30Z","fcTime":"900","fcHumidity":"44","fcTemp":"24","fcRainPC":"3","fcTempFeel":"22","fcAbHumidity":9.574283585110734,"fcDewPoint":11.009520741068439,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-30T17:00:00.000Z","fcDate":"2014-7-30Z","fcTime":"1080","fcHumidity":"42","fcTemp":"24","fcRainPC":"0","fcTempFeel":"23","fcAbHumidity":9.13908887669661,"fcDewPoint":10.311097027833883,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-30T20:00:00.000Z","fcDate":"2014-7-30Z","fcTime":"1260","fcHumidity":"49","fcTemp":"23","fcRainPC":"3","fcTempFeel":"22","fcAbHumidity":10.071676514245361,"fcDewPoint":11.72323563112987,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-30T22:59:00.000Z","fcDate":"2014-7-30Z","fcTime":"1439","fcHumidity":"65","fcTemp":"20","fcRainPC":"1","fcTempFeel":"20","fcAbHumidity":11.230818614791852,"fcDewPoint":13.227090459465341,"fcWindSpeed":"7"}]},{"fcDate":"2014-7-31Z","forecasts":[{"fcDateTime":"2014-07-31T05:00:00.000Z","fcDate":"2014-7-31Z","fcTime":"360","fcHumidity":"77","fcTemp":"17","fcRainPC":"0","fcTempFeel":"17","fcAbHumidity":11.137506032511396,"fcDewPoint":12.942033454155258,"fcWindSpeed":"4"},{"fcDateTime":"2014-07-31T08:00:00.000Z","fcDate":"2014-7-31Z","fcTime":"540","fcHumidity":"66","fcTemp":"19","fcRainPC":"0","fcTempFeel":"18","fcAbHumidity":10.7525307553405,"fcDewPoint":12.510099164940982,"fcWindSpeed":"7"},{"fcDateTime":"2014-07-31T11:00:00.000Z","fcDate":"2014-7-31Z","fcTime":"720","fcHumidity":"53","fcTemp":"22","fcRainPC":"4","fcTempFeel":"20","fcAbHumidity":10.28587245278751,"fcDewPoint":11.990902602628944,"fcWindSpeed":"9"},{"fcDateTime":"2014-07-31T14:00:00.000Z","fcDate":"2014-7-31Z","fcTime":"900","fcHumidity":"46","fcTemp":"23","fcRainPC":"7","fcTempFeel":"22","fcAbHumidity":9.455043258271154,"fcDewPoint":10.770324404435927,"fcWindSpeed":"9"},{"fcDateTime":"2014-07-31T17:00:00.000Z","fcDate":"2014-7-31Z","fcTime":"1080","fcHumidity":"48","fcTemp":"23","fcRainPC":"8","fcTempFeel":"21","fcAbHumidity":9.866132095587291,"fcDewPoint":11.41145603031767,"fcWindSpeed":"9"},{"fcDateTime":"2014-07-31T20:00:00.000Z","fcDate":"2014-7-31Z","fcTime":"1260","fcHumidity":"62","fcTemp":"21","fcRainPC":"9","fcTempFeel":"20","fcAbHumidity":11.35590691086581,"fcDewPoint":13.449117459041737,"fcWindSpeed":"9"},{"fcDateTime":"2014-07-31T22:59:00.000Z","fcDate":"2014-7-31Z","fcTime":"1439","fcHumidity":"72","fcTemp":"19","fcRainPC":"5","fcTempFeel":"18","fcAbHumidity":11.730033551280545,"fcDewPoint":13.842420572085535,"fcWindSpeed":"7"}]},{"fcDate":"2014-8-1Z","forecasts":[{"fcDateTime":"2014-08-01T05:00:00.000Z","fcDate":"2014-8-1Z","fcTime":"360","fcHumidity":"84","fcTemp":"17","fcRainPC":"4","fcTempFeel":"17","fcAbHumidity":12.150006580921524,"fcDewPoint":14.278866115142034,"fcWindSpeed":"4"},{"fcDateTime":"2014-08-01T08:00:00.000Z","fcDate":"2014-8-1Z","fcTime":"540","fcHumidity":"76","fcTemp":"19","fcRainPC":"7","fcTempFeel":"18","fcAbHumidity":12.381702081907243,"fcDewPoint":14.677308122300445,"fcWindSpeed":"7"},{"fcDateTime":"2014-08-01T11:00:00.000Z","fcDate":"2014-8-1Z","fcTime":"720","fcHumidity":"64","fcTemp":"21","fcRainPC":"29","fcTempFeel":"19","fcAbHumidity":11.722226488635675,"fcDewPoint":13.937217531525555,"fcWindSpeed":"9"},{"fcDateTime":"2014-08-01T14:00:00.000Z","fcDate":"2014-8-1Z","fcTime":"900","fcHumidity":"59","fcTemp":"22","fcRainPC":"16","fcTempFeel":"20","fcAbHumidity":11.450310843669115,"fcDewPoint":13.628356573882089,"fcWindSpeed":"9"},{"fcDateTime":"2014-08-01T17:00:00.000Z","fcDate":"2014-8-1Z","fcTime":"1080","fcHumidity":"70","fcTemp":"20","fcRainPC":"37","fcTempFeel":"19","fcAbHumidity":12.094727739006611,"fcDewPoint":14.367333533489349,"fcWindSpeed":"9"},{"fcDateTime":"2014-08-01T20:00:00.000Z","fcDate":"2014-8-1Z","fcTime":"1260","fcHumidity":"77","fcTemp":"19","fcRainPC":"35","fcTempFeel":"18","fcAbHumidity":12.544619214563916,"fcDewPoint":14.879976577375118,"fcWindSpeed":"7"}]}]"""


if __name__ == '__main__':
    main()

    #comment out main to run the test routine
    #testSystem()