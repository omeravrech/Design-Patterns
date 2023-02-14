import DesignPatterns
from threading import Thread

class Test(Observable, Thread):
    def __init__(self):
        Observable.__init__(self)
        Thread.__init__(self)

#    def run(self):
#        for i in range(1,5):
#            self