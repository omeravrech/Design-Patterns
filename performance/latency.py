
import json, os, time, sys
from threading import Thread
from device import Device

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
    db = MongoServer('localhost')
    threads = getResources('firewalls.json')
    for thread in threads:
        thread.start()
    time.sleep(2)
    for thread in threads:
        thread.stop()
