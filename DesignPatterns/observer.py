class Update(object):
    def _init__(self, title, value):
        self.title = title
        self.value = value

    def Title(self):
        return self.title
    
    def Value (self):
        return self.value

class ObserableAbstruct(object):
    def __init__(self):
        self._observers = []
        self.event = None
    
    def subscribe(self, observer):
        raise NotImplementedError()

    def unsubscribe(self, observer):
        raise NotImplementedError()

    def notify(self, event):
        raise NotImplementedError()

    def getEvent(self):
        raise NotImplementedError()

class ObserverAbstruct(object):
    def __init__(self):
        self._changed = 0
        self._updates = []

    def update(self, observable):
        raise NotImplementedError()

class Observable(ObserableAbstruct):
    def __init__(self):
        super().__init__()

    def subscribe(self, observer):
        if (isinstance(observer, ObserverAbstruct) == True):
            if observer not in self._observers:
                self._observers.append(observer)
                return True
        return False

    def unsubscribe(self, observer):
        if (isinstance(observer, ObserverAbstruct) == True):
            if observer in self._observers:
                self._observers.remove(observer)
                return True
        return False

    def notify(self, event):
        if (isinstance(event, Update) == True):
            for o in self._observers:
                o.update(self)
        else:
            raise AttributeError()
    
    def getEvent(self):
        while (self.event == None):
            continue
        temp = self.event
        self.event = None
        return temp

class Observer(ObserverAbstruct):
    def __init__(self):
        super().__init__()
    
    def update(self, observable):
        self._changed = 1
        self._updates.append(observable)

    def getUpdates(self):
        for update in self._updates:
            yield update.getEvent()
        self._changed = 0
        self._updates = []


if __name__ == "__main__":
    oable1 = Observable()
    oable2 = Observable()

    oer1 = Observer()
    oer2 = Observer()

    oable1.subscribe(oer2)
    oable1.subscribe(oer1)

    u = Update("Test1", "GOOGLE")
    oable1.notify()
    oable2.notify(Update("TEST2", "WALLA"))

    updateList = oer1.getEvent()

    print(next(updatelist))
    print(next(updatelist))
    print(next(updatelist))
    