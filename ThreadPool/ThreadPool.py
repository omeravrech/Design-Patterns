from threading import Thread
from queue import Queue
from time import sleep, time

BUF_SIZE = 1024
SLEEP = 1

class iConsumer(Thread):
    """
        Consumer - A thread whom responsible to handle the tasks outputs
        comes from the producers
    """
    def __init__(self, output_queue:Queue):
        super().__init__()
        self.output = output_queue
        self.running_status = True
    """
        Define a Thread that will run by the Producers
    """
    def run(self):
        raise "NO_FUNCTION_IMPLIMENTED"

    def stop(self):
        raise "NO_FUNCTION_IMPLIMENTED"


class EmptyConsumer(iConsumer):
    """
        dummy consumer - print all to screen
    """
    def __init__(self, output_queue:Queue):
        super().__init__(output_queue)
        self.__write = print

    def run(self) -> None:
        self.__write("Start Consumer")
        while(self.running_status or not self.output.empty()):
            if not self.output.empty():
                try:
                    err, output = self.output.get()
                    if (err):
                        self.__write(err)
                    else:
                        self.__write(output)
                except Exception as err:
                    pass

    def stop(self) -> None:
        self.running_status = False
        self.__write("Consumer Stopped")

class Producer(Thread):
    """
        Producer - A thread whom responsible for execute a task    
    """
    def __init__(self, task_queue:Queue, output_queue:Queue):
        Thread.__init__(self)
        self.__task_queue = task_queue
        self.__output_queue = output_queue
        self.__running_status = True
        self.__free = True
        self.__start_time = time()

    def run(self) -> None:
        while(self.__running_status):
            if not self.__task_queue.empty() and not self.__output_queue.full():
                reuse, func, args, kwargs = self.__task_queue.get()
                self.__free = False
                try:
                    result = (False, func(*args, **kwargs))
                    if (reuse):
                        self.__task_queue.put((True, func, args, kwargs))
                except Exception as e:
                    result = (e, None)

                self.__output_queue.put(result)
                self.__free = True
            else:
                sleep(SLEEP)

    def stop(self) -> None:
        self.__running_status = False
        self.__free = True

    @property
    def is_free(self) -> bool:
        return self.__free

    @property
    def is_run(self) -> bool:
        return self.__running_status

    @property
    def runtime(self):
        return round(time() - self.__start_time,0)

class ThreadPool (object):
    """
        This class define a Thread Pool class which able to receive large amount of
        tasks and execute them in parallel. 
    """
    def __init__(self, consumer:iConsumer = EmptyConsumer, workers:int = 25):
        self.__tasks   = Queue(BUF_SIZE)
        self.__outputs = Queue(BUF_SIZE)
        self.__workers = [Producer(self.__tasks, self.__outputs) for i in range(workers)]

        if issubclass(consumer, iConsumer):
            self.__consumer = consumer(self.__outputs)
        else:
            raise ValueError("Consumer must implement iConsumer interface")

    def add_task(self, reuse:bool=False, func=None, *args, **kwargs):

        if not hasattr(func, '__call__'):
            raise "NO_FUNCTION_ENTERED"

        if self.__tasks.full():
            raise "FULL_TASK_QUEUE"

        self.__tasks.put((True, func, args, kwargs))
        return self # For concat commands
    
    def start(self) -> None:
        self.__consumer.start()  # Starting the output handler first

        for worker in self.__workers:
            try:
                worker.start()
            except:
                pass

    def stop(self) -> None:
        for worker in self.__workers:
            worker.stop()
        self.__consumer.stop()   # Stop the output handler last
        self.__consumer.join()

    
    def __str__(self) -> str:
        message = []
        message.append("Thread Pool Statistics:")
        message.append(f"   There are { len(self.__workers) } workers in the pool.")
        message.append(f"   Thread Status:")
        for index, thread in enumerate(self.__workers, start=1):
            message.append(f"      Thread-{index} status: {'Stopped' if not thread.is_run else 'Free' if thread.is_free else 'Occupied'}.")
        message.append(f"   { self.__tasks.qsize() } tasks waiting for executed.")
        message.append(f"   { self.__outputs.qsize() } results waiting for handled.")
        message.append("")
        return "\n".join(message)
