import os
import time
import threading

from queue import Queue, Empty


def execption_handler(thread_name, exception):
    print(f'{thread_name}: {exception}')


class Worker(threading.Thread):

    def __init__(self, name, queue, result, wait_queue=False, callback=None,
        execption_handler=execption_handler):

        threading.Thread.__init__(self)
        self.name = name
        self.queue = queue
        self.result = result
        self._abort = threading.Event()
        self._idle = threading.Event()
        self._pause = threading.Event()
        self.callback = callback
        self.execption_handler = execption_handler
        self.wait_queue = wait_queue


    def abort(self, block=True):
        self._abort.set()
        # print(f'{self.name} is stopping...')
        self.block(block)
        print(f'{self.name} is stopped')

    def aborted(self):
        return self._abort.is_set()

    def pause(self):
        self._pause.set()
        self._idle.set()

    def resume(self):
        self._pause.clear()
        self._idle.clear()

    def paused(self):
        return self._pause.is_set()

    def __del__(self):
        if not self.aborted():
            self.abort()
        # print(f'{self.name} is deleted')

    def _pause_now(self):
        """ block the code for a while """
        while self.paused():
            print(f'{self.name} paused for 0.5s...')
            time.sleep(0.5)

    def block(self, block=True):
        while block and self.is_alive():
            time.sleep(0.5)

    def run(self):
        while not self.aborted():
            try:
                func, args, kwargs = self.queue.get(timeout=0.5)
                # func = self.queue.get(timeout=0.5)
                self._idle.clear()
            except Empty:
                # the queue is empty.
                print(f'{self.name}: The Queue is empty.')
                self._idle.set()
                # abort the thread if the queue is empty.
                if not self.wait_queue:
                    break
                continue
            except Exception as e:
                pass

            # the task is available to work with.
            try:
                print(f'{self.name} processing...')
                r = func(*args, **kwargs)
                self.result.put(r)
                if self.callback:
                    self.callback(r)

            except Exception as e:
                print('Exception has occured')
                self.execption_handler(self.name, e)
            finally:
                self.queue.task_done()
                # self._abort.wait(1)

            # pause the thread is _pause flag is set
            self._pause_now()



class Pool:
    def __init__(self, max_workers=os.cpu_count() + 4, name=None, queue=None, wait_queue=True,
        result_queue=None, callback=None, execption_handler=execption_handler):
        self.name = name
        self.max_worker = max_workers
        self.callback = callback
        self.execption_handler = execption_handler

        self.queue = queue if isinstance(queue, Queue) else Queue()
        self.result_queue = result_queue if isinstance(result_queue, Queue) else Queue()
        self.wait_queue = wait_queue

        # self.idles = []
        # self.aborts = []
        self.threads = []


    def start(self):
        # reinitialize values
        # self.idles = []
        # self.aborts = []
        self.threads = []
        # self.result_queue = self.result_queue if isinstance(result_queue, Queue) else Queue()

        # create all threads
        for i in range(self.max_worker):
            self.threads.append(Worker(f'Worker_{i}_({self.name})', self.queue, self.result_queue, wait_queue=self.wait_queue, callback=self.callback))

        # start all threads
        for t in self.threads:
            t.start()

        return True

    def is_alive(self):
        return any((t.is_alive() for t in self.threads))

    def is_idle(self):
        return False not in (t.idle() for t in self.threads)

    def is_done(self):
        return self.queue.empty()

    def shutdown(self, block=False):
        """ Abort all threads in the pool """
        for t in self.threads:
            t.resume() # the thread should be working to abort it.
            t.abort()
        self.block(block)

        # clearing resources
        # self.threads = [] # I should do this after all threads are shutted down.
        self.result_queue = None
        print(f'{self.name} is shutted down')

    def join(self, timeout=None):
        """ wait until all the queue tasks be completed """
        if timeout and self.is_alive():
            time.sleep(timeout)
        else:
            self.queue.join()

    def result(self, block=False):
        """ return result as generator """
        result = []
        if block and self.is_alive():
            self.join()
        try:
            while True:
                result.append(self.result_queue.get(False))
                self.result_queue.task_done()
        except:
            # the result_queue is emply
            pass

        return result

    def __del__(self):
        self.shutdown()

    def is_paused(self):
        return False not in ( t.paused() for t in self.threads )

    def pause(self, timeout=0, block=False):
        """ after_abort: pause an amount of time (timeout) after all threads of the pool has stopped/aborted """
        print(f'>>>>>>>>>> {self.name} is paused <<<<<<<<<<<<')
        for t in self.threads:
            t.pause()
        if timeout:
            # if block:
            #     # to make sure start counting after all threads are paused.
            #     while self.is_paused():
            #         print(f'{self.name} sleeping 0.2s...({self.is_paused()})')
            #         time.sleep(0.2)
            # print('>>>> Loop is finished')
            time.sleep(timeout)
            self.resume()
        return True

    def resume(self, block=False):
        print(f'>>>>>>>>>> {self.name} is resumed <<<<<<<<<<<<')
        for t in self.threads:
            t.resume()
        return True

    def block(self, block=True):
        while block and self.is_alive():
            time.sleep(0.5)

    def count(self):
        return len(self.threads)


    def update(self, n, block=False):

        # create necissary threads
        need = n - self.count()
        if need > 0:
            # TODO: create more threads
            for _ in range(need):
                t = Worker(f'Worker_{(self.count())} ({self.name})', self.queue, self.result_queue, wait_queue=self.wait_queue, callback=self.callback)               
                t.start()
                self.threads.append(t)

        elif need < 0:
            need = abs(need)
            # TODO: delete some threads
            threads = []
            for _ in range(need):
                t = self.threads.pop()
                t.resume() # the thread should be working to abort it.
                t.abort()
                threads.append(t)

            # block until the extra threads dead.
            while block and any(( t.is_alive() for t in threads )):
                time.sleep(0.5)




