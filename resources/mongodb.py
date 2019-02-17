from pymongo   import MongoClient
from threading import Thread
import time

def main():
    mongoSRV = MongoServer('localhost')
    mongoSecSRV = MongoServer('localhost')
    mongoSRV.database('network-monitor')
    r = mongoSecSRV.retrive('test')
    for obj in r:
        mongoSRV.write('test2', obj)
        time.sleep(1)
    print(mongoSecSRV.queue)


def removeUnicode(jsonObject):
    if (isinstance(jsonObject, list) == True):
        result = []
        for obj in jsonObject:
            result.append(removeUnicode(obj))
        return result

    result = {}
    for key in jsonObject:
        if key.encode('utf-8') == '_id':
            pass
        elif (isinstance(jsonObject[key], dict) == True):
                result[key.encode('utf-8')] = removeUnicode(jsonObject[key])
        elif (isinstance(jsonObject[key], list) == True):
            temp = []
            for obj in jsonObject[key]:
                temp.append(removeUnicode(obj))
            result[key.encode('utf-8')] = temp
        elif isinstance(jsonObject[key],float) == True:
            result[key.encode('utf-8')] = jsonObject[key].encode('utf-8')
        else:
            result[key.encode('utf-8')] = jsonObject[key].encode('utf-8')
    return result


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            print('Create New instance of DB')
        return cls._instances[cls]


class MongoServer():
    __metaclass__ = Singleton

    def __init__(self, hostname, port=27017, self_connect=True):
        self.server = None
        self.hostname = hostname
        self.port = port
        self.db = None

        self.queue = []
        self.work = False

        self.thread = Thread(target=self.worker)
        self.thread.start()

        if (self_connect):
            self.connect()

    def connect(self, hostname=None, port=None):
        '''
         Initlize the connection to the server
        '''
        if self.server != None:
            self.server.close()

        self.hostname = self.hostname if hostname == None else hostname
        self.port =     self.port     if port == None     else port

        try:
            self.server = MongoClient(self.hostname, self.port)
            print('Connection been opened to mongodb://{}:{}'.format(self.hostname, self.port))
        except ServerSelectionTimeoutError | ServerSelectionTimeoutError | ConnectionFailure:
            self.server = None

    def database(self, database):
        if (database != None):
            self.db = database

    def retrive(self, collection):
        ret = []
        response = self.server[self.db][collection].find({})
        if response.count() > 0:
            for j in response:
                ret.append(removeUnicode(j))
        return ret

    def write(self, collection, data):
        if (collection == None or data == None):
            return
        request = { 'collection': collection , 'data': data }
	self.queue.append(request)

    def worker(self):
        if (self.work):
            return
        self.work = True
        while self.work:
            print("Queue size = %d", len(self.queue))
            if (len(self.queue) > 0):
                data = self.queue.pop(0)
                self.server[self.db][data.collection].insertOne(data.data)
                print(data.collection)
            else:
                time.sleep(2)

    def __str__(self):
        output ='MongoServer:'
        output += "\n- Server = '" + self.hostname + "'"
        output += "\n- Port = " + str(self.port)
        output += "\n- Connection = " + ('Close' if self.server == None else 'Open')
        if self.db != None:
            output += "\n- Database = '" + self.db + "'"
        return output

if (__name__ == "__main__"):
    main()
