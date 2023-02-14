
import json, os, time, sys
from threading import Thread
from device import Device
from resources import MongoServer

def getResources(filename):
    datastore = []
    try:
        path = os.path.join('../resources/', filename)
        with open(path) as f:
            datastore = json.load(f)
    except:
        return []

    result = []
    for i in range(len(datastore)):
        keys = datastore[i].keys()
        temp = {}
        for key in keys:
            temp[key.encode('utf-8')] = datastore[i][key].encode('utf-8')
        result.append(Device(ip=temp['ip'], name=temp['name'], interval=1000))

    return result

#    finally:
#        return datastore

if (__name__ == '__main__'):

    mongoSRV = MongoServer('localhost')
    mongoSRV.database('network-monitor')
    array = mongoSRV.retrive('test')
    threads = []

    for device in array:
        thread = Device(ip=device['ip'], name=device['name'], interval=1000)
        thread.bind(mongoSRV)
        thread.start()
        threads.append(thread)
#    time.sleep(2)
#    for thread in threads:
#        thread.stop()
